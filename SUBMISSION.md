# Hackathon Submission Compliance Matrix

**Hackathon**: ZeroDay OSS Hacktoberfest 2026, IIIT Dharwad  
**Track / Problem Statement**: Problem Statement 2 (Private Legal Document Triage Agent)  
**Team**: Kernel Knights  

This document provides an exhaustive verification checklist mapping every requirement (S1–S10), safety gate (G1–G5), and maturity level (L1–L4) directly to source code files and documentation in this repository.

---

## 1. Problem Statement Requirements Mapping (S1 – S10)

| ID | Requirement Description | Implementation Location | Compliance Status |
| :- | :--- | :--- | :--- |
| **S1** | **Privacy-First & On-Device Operation**<br>Zero remote API calls; runs 100% locally on user machine. | `pipeline.py:22-23` (`OLLAMA_HOST = "http://127.0.0.1:11434"`), `api.py:169-171` (`uvicorn.run(host="127.0.0.1")`), `docs/privacy-and-network.md` | **Fully Met** |
| **S2** | **Document Ingestion (.pdf, .txt)**<br>Local text extraction without external services or remote converters. | `pipeline.py:107-116` (`read_document()`, `pypdf.PdfReader`), `api.py:106-116` (`/api/analyze`) | **Fully Met** |
| **S3** | **Structured Clause Analysis**<br>Plain-language summary, obligations, and rights separated from interpretation. | `pipeline.py:33-45` (`ClauseAnalysis` Pydantic model), `frontend/index.html:1-18` (card layout) | **Fully Met** |
| **S4** | **Verifiable Grounded Quotes**<br>Every citation is checked verbatim against source; hallucinations dropped. | `pipeline.py:148-163` (`verify_quotes()`), `pipeline.py:194-202`, `tests/test_pipeline.py:30-67` | **Fully Met** |
| **S5** | **Risk Flagging & Lawyer Escalation**<br>Severe penalties, forfeiture, and ambiguity flagged for legal review. | `pipeline.py:42-43` (`requires_lawyer_escalation`), `pipeline.py:65-66` (system prompt), `frontend/index.html:7-8` | **Fully Met** |
| **S6** | **Grounded Question Answering**<br>Answers derived exclusively from document context; no general knowledge. | `pipeline.py:69-74` (`QA_SYSTEM`), `pipeline.py:263-284` (`ask()`), `frontend/index.html:56-74` | **Fully Met** |
| **S7** | **Document Silence Handling**<br>Explicitly reports when a topic is absent rather than guessing. | `pipeline.py:250-262` (`retrieve()`), `pipeline.py:273-275` (`status: document_silent`), `tests/test_pipeline.py:86-93` | **Fully Met** |
| **S8** | **Deterministic Refusal of Legal Verdicts**<br>Refuses questions on validity or enforceability without calling model. | `pipeline.py:85-89` (`VERDICT` regex), `pipeline.py:265-270`, `tests/test_pipeline.py:105-124` | **Fully Met** |
| **S9** | **Prompt Injection Defense**<br>Treats excerpt as untrusted data; flags jailbreaks and forces escalation. | `pipeline.py:61-62`, `pipeline.py:76-82` (`INJECTION` regex), `pipeline.py:203-206`, `samples/injection_test.txt` | **Fully Met** |
| **S10** | **Clean User Interface & Session Wiping**<br>Interactive web interface with progress polling, export, and deletion control. | `frontend/index.html`, `api.py:153-161` (`/api/clear`), `api.py:47-52` (CSP security headers) | **Fully Met** |

---

## 2. Verification Gates (G1 – G5)

| Gate | Description | Enforcement Mechanism | Verification File |
| :--- | :--- | :--- | :--- |
| **G1: Network Isolation** | No outbound connections over the public internet during analysis or Q&A. | Hard-coded `127.0.0.1` loopback bindings; CSP blocking external browser loads. | `docs/privacy-and-network.md`, `api.py:42-52` |
| **G2: Verbatim Citations** | Zero unverifiable quotes presented to user; ungrounded summaries flagged. | Python substring matching with case and curly-quote normalization; dropped quotes tracked. | `pipeline.py:154-162`, `tests/test_pipeline.py:30-41` |
| **G3: No-Verdict Boundary** | Tool strictly disclaims definitive legal advice and refuses validity queries. | Deterministic `VERDICT` regex intercepts enforceability queries with 0 model calls. | `pipeline.py:85-89`, `pipeline.py:265-270` |
| **G4: Untrusted Data Fence** | Adversarial instructions inside documents cannot override system instructions. | Delimited `<document_excerpt>` blocks, structured schema parsing, `INJECTION` regex. | `pipeline.py:57-67`, `samples/injection_test.txt` |
| **G5: Zero Residual Storage**| Uploaded documents deleted immediately after ingestion; memory wiped on demand. | `tempfile.mkstemp` unlinked in `finally` block; `/api/clear` purges all process RAM state. | `api.py:99-103`, `api.py:153-161` |

---

## 3. Compliance Levels (L1 – L4)

| Level | Title | Verification Criteria | Status |
| :--- | :--- | :--- | :--- |
| **L1** | **Functional Baseline** | PDF/TXT parsing, chunking, local LLM structured JSON output, CLI & Web UI. | **PASSED** |
| **L2** | **Defensive Engineering** | Verbatim citation verification in code, deterministic verdict refusal, document silence gate. | **PASSED** |
| **L3** | **Security & Hardening** | Prompt injection scanner, loopback-only sockets, strict Content-Security-Policy headers. | **PASSED** |
| **L4** | **Judge-Ready Package** | Complete documentation, empirical test logs, offline pytest suite, synthetic samples. | **PASSED** |
