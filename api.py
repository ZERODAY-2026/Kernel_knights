"""
Local web server for the private legal triage demo.

    python api.py   ->   open http://127.0.0.1:8000

Bound to 127.0.0.1 only. Uploaded files go to a temp file that is deleted as
soon as processing ends; analysis results live in memory until you press
"Clear document" or stop the server. Every response carries a strict
Content-Security-Policy so the browser itself refuses to load anything from
the internet (defense in depth; the real proof is your network monitor).
"""
import os
import re
import tempfile
import threading
import time
import uuid

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from pipeline import (DISCLAIMER, EXPECTED, MODEL, analyze_chunk, ask,
                      chunk_text, read_document)

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 20 * 1024 * 1024

app = FastAPI(title="Private Legal Triage (local)")
STATE = {"chunks": []}   # kept in memory only, for follow-up questions
JOBS = {}
LOCK = threading.Lock()

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; "
       "style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "connect-src 'self'; frame-ancestors 'none'")


@app.middleware("http")
async def security_headers(request, call_next):
    resp = await call_next(request)
    resp.headers["Content-Security-Policy"] = CSP
    resp.headers["Cache-Control"] = "no-store"
    return resp


AMOUNT = re.compile(r"(?:[$\u20b9]|Rs\.?|INR)\s?[\d,]+(?:\.\d+)?")
DATE = re.compile(
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
    r"|\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}\b")


class Question(BaseModel):
    question: str


def _run(job_id: str, path: str):
    job = JOBS[job_id]
    try:
        text = read_document(path)
        chunks = chunk_text(text)
        job["total"] = len(chunks)
        for i, c in enumerate(chunks, 1):
            if job["cancelled"]:
                job["status"] = "cancelled"
                return
            try:
                a = analyze_chunk(c)
            except Exception as e:
                a = {"clause_topic": "Analysis failed for this section",
                     "warnings": f"The model output could not be processed: {e}",
                     "grounded": False, "source_text": c}
            job["clauses"].append(a)
            job["done"] = i
        job["elapsed"] = round(time.time() - job["t0"], 1)
        job["result"] = {
            "disclaimer": DISCLAIMER,
            "model": MODEL,
            "seconds": job["elapsed"],
            "chunks": len(chunks),
            "amounts_found": sorted(set(AMOUNT.findall(text))),
            "dates_found": sorted(set(DATE.findall(text))),
            "not_found_by_keyword_check": [n for n, p in EXPECTED.items()
                                           if not re.search(p, text, re.I)],
        }
        STATE["chunks"] = chunks
        job["status"] = "done"
    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


@app.post("/api/analyze")
def analyze(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "")[1].lower()
    if suffix not in (".pdf", ".txt"):
        raise HTTPException(415, "Please upload a .pdf or .txt file.")
    data = file.file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "File is larger than 20 MB.")
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    with LOCK:
        if any(j["status"] == "running" for j in JOBS.values()):
            os.remove(path)
            raise HTTPException(409, "An analysis is already running.")
        STATE["chunks"] = []
        job_id = uuid.uuid4().hex
        JOBS[job_id] = {"status": "running", "done": 0, "total": 0, "t0": time.time(),
                        "elapsed": 0, "clauses": [], "result": None, "error": None,
                        "cancelled": False}
    threading.Thread(target=_run, args=(job_id, path), daemon=True).start()
    return {"job_id": job_id}


@app.get("/api/status/{job_id}")
def status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "Unknown job.")
    elapsed = round(time.time() - job["t0"], 1) if job["status"] == "running" else job["elapsed"]
    return {"status": job["status"], "done": job["done"], "total": job["total"],
            "elapsed": elapsed, "clauses": job["clauses"], "result": job["result"],
            "error": job["error"]}


@app.post("/api/ask")
def ask_question(q: Question):
    if not STATE["chunks"]:
        raise HTTPException(400, "Analyze a document first.")
    if not q.question.strip():
        raise HTTPException(422, "Type a question first.")
    try:
        return ask(q.question.strip(), STATE["chunks"])
    except Exception as e:
        raise HTTPException(500, f"Could not answer: {e}")


@app.post("/api/clear")
def clear():
    """Deletion control: forget the document and all results held in memory."""
    with LOCK:
        for j in JOBS.values():
            j["cancelled"] = True
        JOBS.clear()
        STATE["chunks"] = []
    return {"cleared": True}


FRONTEND = os.path.join(HERE, "frontend")
if os.path.isdir(FRONTEND):
    app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="ui")

if __name__ == "__main__":
    print("Open http://127.0.0.1:8000  (local only)")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
