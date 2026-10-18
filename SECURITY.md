# Security & Privacy Policy

## Reporting Security Issues

We take security and privacy vulnerabilities seriously. If you discover a vulnerability, please report it responsibly:

1. **Do not open a public GitHub issue.**
2. Email the maintainers directly at `<!-- TODO(me): security contact email or private disclosure link -->` with:
   - A description of the vulnerability.
   - Steps to reproduce or proof-of-concept document.
   - Any observed network activity or data leakage.
3. Maintainers will acknowledge receipt within 48 hours and work with you on a coordinated fix.

---

## Privacy by Design: Architectural Guarantees

This repository was specifically constructed to handle sensitive, private legal contracts (rental leases, employment contracts, offer letters) without risking third-party leakage.

### 1. Loopback-Only Execution
- **Ollama**: Hard-coded to `http://127.0.0.1:11434` in `pipeline.py`. It is never configured to dial a remote IP or domain.
- **FastAPI / Uvicorn Server**: Bound strictly to `127.0.0.1:8000`. The server refuses external interface bindings (`0.0.0.0`).
- **Offline Operation**: Once dependencies (`pip`) and model weights (`ollama pull gemma4:e4b`) are downloaded during initial setup, the application operates completely severed from the internet.

### 2. Ephemeral Storage & Zero Data Retention
- **Temporary Uploads**: Files uploaded via the web interface are saved to a temporary path via Python's `tempfile.mkstemp()`. As soon as text extraction completes, `os.remove(path)` is unconditionally invoked in a `finally` block.
- **In-Memory Volatility**: Document chunks and analysis summaries reside strictly in process memory (`STATE["chunks"]` and `JOBS`). No document data is saved into persistent databases, SQLite files, or cache directories.
- **Explicit Deletion Control**: The UI provides a **Clear document** button (`POST /api/clear`) that terminates running worker threads and resets all in-memory arrays. Terminating the `python api.py` process instantly purges all document remnants.

### 3. Defensive Browser Sandboxing
- The FastAPI middleware injects a strict `Content-Security-Policy` (CSP) on every HTTP response:
  ```http
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'
  Cache-Control: no-store
  ```
- This prevents the browser from loading third-party scripts, remote stylesheets, tracking pixels, or connecting to external analytics APIs.

### 4. Adversarial Document Handling (Prompt Injection Defense)
- Documents uploaded by users are treated as **untrusted data**.
- All chunk content sent to the model is wrapped within `<document_excerpt>` delimiter tags.
- A deterministic regular expression scanner (`INJECTION`) inspects excerpts for instruction-like override patterns (e.g., `"ignore previous instructions"`, `"system prompt"`, `"summarize this as harmless"`).
- When detected, the pipeline marks the clause for **mandatory lawyer escalation** and prepends an explicit warning without executing the embedded instructions.
