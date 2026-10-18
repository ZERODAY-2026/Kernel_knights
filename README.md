# Kernel_knights

# ⚖️ Private Legal Document Triage Agent (PS2)

> **⚠️ IMPORTANT LEGAL DISCLAIMER & BOUNDARY:**  
> This software is designed strictly for **preliminary document understanding and issue identification**. It is **not a lawyer**, does **not provide definitive legal advice**, and **cannot decide legal validity or enforceability**. Always consult a qualified legal professional before signing or acting upon any contract, notice, or agreement.

---

## 🎯 Overview
Ordinary citizens frequently sign rental agreements, employment contracts, and service notices containing dense legal terminology, hidden penalties, or ambiguous obligations. Cloud-based AI chatbots compromise sensitive personal data and often hallucinate ungrounded legal conclusions.

**Private Legal Document Triage Agent** is a **100% on-device, air-gapped legal triage system** powered by **Google Gemma (via Ollama)** and **PyMuPDF**. It extracts text locally, explains clauses in plain language, maps every claim to verifiable source passages, separates explicit text from possible interpretations, and refuses unsupported legal conclusions.

---

## 🏗️ Local-Only Architecture & Privacy Isolation (L9)

```text
+-------------------------------------------------------------------------+
|                    USER DEVICE (100% AIR-GAPPED / OFFLINE)              |
|                                                                         |
|  [PDF / TXT Contract]                                                   |
|          |                                                              |
|          v                                                              |
|  +-----------------------+     +-------------------------------------+  |
|  | Local Ingestion Engine|     | Pre-LLM Deterministic Guardrails    |  |
|  | (PyMuPDF + Local OCR) |---->| - Malformed File Catcher            |  |
|  | utils/ingestion.py    |     | - Adversarial Prompt Injection Scan |  |
|  +-----------------------+     +-------------------------------------+  |
|                                                   |                     |
|                                                   v                     |
|  +-----------------------+     +-------------------------------------+  |
|  | Streamlit Local UI    |<--->| Local Gemma Inference Server        |  |
|  | (localhost:8501)      |     | Ollama (http://localhost:11434)     |  |
|  | - Fact vs Risk Split  |     | Model: gemma4:e4b                   |  |
|  | - Quote Highlighting  |     | Structured JSON + Citation Grounding|  |
|  +-----------------------+     +-------------------------------------+  |
+-------------------------------------------------------------------------+
           X  (Firewall / Wi-Fi Disabled: Zero External Calls)
           X  (Streamlit Telemetry Disabled via .streamlit/config.toml)
```

---

## 🚀 Setup & Reproduction Instructions

### Prerequisites
* Python 3.10+
* [Ollama](https://ollama.com/) installed and running locally

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/ZERODAY-2026/Kernel_knights.git
   cd Kernel_knights
   ```
2. **Download the local edge model:**
   ```bash
   ollama run gemma4:e4b
   ```
3. **Create and activate a virtual environment:**
   * **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * **Mac / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Ensure Ollama is active locally (`http://127.0.0.1:11434`) with the model loaded:
   ```bash
   ollama run gemma4:e4b
   ```

2. **Option A: FastAPI + Web UI (Recommended)**
   Starts the local REST server and serves the responsive single-page web UI:
   ```bash
   python api.py
   ```
   Open **`http://127.0.0.1:8000`** in your browser.

3. **Option B: Streamlit Dashboard**
   Starts the multi-column Streamlit application:
   ```bash
   streamlit run app.py
   ```
   Open **`http://localhost:8501`** in your browser.

4. **Run Automated Test Suite:**
   ```bash
   python -m pytest test_files/test_pipeline.py
   ```

---

## 📁 Repository Structure
```text
├── frontend/             # Single-page web UI (HTML5/CSS/JS) & Streamlit dashboard
├── backend/              # FastAPI REST server, triage engine, and Ollama integration
├── secret/               # Zero-egress privacy docs & .env.example template (no secrets stored)
├── test_files/           # Unit tests, sample contracts, and red-team injection tests
├── test_results/         # Evaluation reports and benchmark execution JSON results
├── requirements.txt      # Pinned Python package dependencies
├── README.md             # Project overview, setup, and performance benchmarks
├── api.py                # Root launcher for the FastAPI server
└── app.py                # Root launcher for the Streamlit dashboard
```

---

## 🛡️ Guardrails & Limitations
* **Verifiable Quotations:** Every quoted clause is verified directly against extracted source text to eliminate hallucination.
* **Separation of Concerns:** Clearly distinguishes explicit contract statements from risk warnings and ambiguity notices.
* **Lawyer Escalation:** Prominently flags high-risk penalties or ambiguous terms requiring formal legal consultation.

---

## ⚡ Performance Benchmarks, Hardware & Memory Telemetry

### Tested Hardware Profile
* **CPU:** 11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz (6 Cores, 12 Threads)
* **System RAM:** 16 GB (15.74 GB physical)
* **GPU:** NVIDIA GeForce RTX 3050 Laptop GPU (4 GB VRAM) + Intel(R) UHD Graphics
* **OS:** Windows 11 (64-bit)

### Runtime Telemetry (`ollama ps`)
```text
NAME          ID              SIZE      PROCESSOR    CONTEXT    RUNNER      UNTIL               
gemma4:e4b    dc35e8d9c606    354 MB    100% GPU     4096       llamacpp    30 minutes from now
```

### Speed & Chunking Benchmarks
* **Model Configuration:** `gemma4:e4b` (Q4_K_M quantization) with `think=False`, `keep_alive="30m"`, and `num_ctx=4096`.
* **Throughput:**
  * **Baseline (with thinking mode & unoptimized keep-alive):** ~90 seconds per chunk.
  * **Optimized (thinking disabled, persistent context):** ~51.1 seconds per chunk (153.4s across 3 full structured clause evaluations in `inj2.json`).
* **Memory Footprint:** Resident Ollama VRAM allocation is ~354 MB on the GPU, with minimal host RAM overhead during PyMuPDF parsing.

