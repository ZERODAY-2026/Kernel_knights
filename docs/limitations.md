# Known Limitations & Non-Goals

To maintain transparency and prevent misuse, this document outlines the explicit boundaries, technical trade-offs, and current operational limitations of the **Private Legal Document Triage Agent**.

---

## 1. Document Scope & Formatting Limitations

### A. English Language Only
- **Limitation**: The prompt templates, regular expressions, and stemmers are optimized strictly for **English language** contracts.
- **Impact**: Non-English agreements (or mixed-language contracts) may fail chunking heuristics, yield inaccurate summaries, or drop quotes due to language-specific character sets.

### B. No Optical Character Recognition (OCR)
- **Limitation**: Ingestion relies on `pypdf`, which extracts native text streams from digital PDFs. It does **not** include OCR libraries (such as Tesseract or OCRmyPDF).
- **Impact**: Scanned paper leases, image-based exports, or photograph PDFs will be rejected with an explicit error:  
  `ValueError: "No extractable text (scanned PDF?). OCR is out of scope."`
- **Workaround**: Users must run local OCR prior to uploading (e.g., using open-source tools like `ocrmypdf`).

### C. Contract Domain Focus
- **Limitation**: Regex heuristics and prompt instructions are tailored for **residential rental leases** and **employment/consulting agreements**.
- **Impact**: Complex corporate mergers, patents, cross-border credit facilities, or bond indentures contain structural nuances that exceed this tool's heuristic designs.

---

## 2. Legal & Safety Boundaries (Non-Goals)

### A. No Legal Advice & No Enforceability Verdicts
- **Boundary**: This software is an informational reading aid, **not an attorney**.
- **Refusal**: The system deterministically refuses queries such as *"Is this clause legal?"*, *"Will this hold up in court?"*, or *"Can my landlord sue me?"*.
- **Rationale**: Legal validity depends on statutory caps, state/provincial tenancy laws, unconscionability standards, and judicial precedent that cannot be reliably assessed by a general edge model without legal counsel.

### B. Not a Substitute for Professional Counsel
- **Boundary**: When aggressive terms, forfeiture clauses, or ambiguous liabilities are flagged, the user must consult a qualified attorney before signing or disputing.

---

## 3. Retrieval & Semantic Nuance

### A. Lexical TF-IDF vs. Dense Semantic Retrieval
- **Limitation**: Document search uses lexical TF-IDF with 5-character prefix stemming (`sublet` ~ `sublease`, `terminat` ~ `termination`) and a 30% coverage cutoff.
- **Impact**: Queries that rely heavily on abstract synonyms without sharing lexical roots may fail to retrieve relevant passages, causing the system to report that the document is silent.
- **Design Rationale**: Avoids loading an auxiliary dense embedding model (e.g., `all-MiniLM-L6-v2`) into system memory alongside Gemma 4, keeping the RAM footprint accessible on standard consumer hardware.

---

## 4. Verification Gaps

### A. Model Caveats Field Unverified Against Source
- **Known Issue**: While `verifiable_quotes` are strictly checked against source text using exact substring matching, the model's free-text `caveats` field returned during Q&A is **not** verified against the document.
- **Impact**: If Gemma 4 hallucinates an extraneous contextual caveat, it will display under the "Model note" header in the UI. Users should rely primarily on the verbatim quotes block.

---

## 5. Concurrency & Performance

### A. Single-User In-Memory Concurrency
- **Limitation**: State management (`STATE["chunks"]` and `JOBS`) is stored in Python process RAM. The web API enforces a concurrency lock preventing multiple simultaneous analysis jobs.
- **Impact**: Attempting to upload a second document while an analysis is running will return HTTP 409 (`"An analysis is already running."`). The tool is designed for individual personal workstations, not multi-tenant cloud hosting.

### B. Evaluation Scale
- **Limitation**: The system has been validated on synthetic test documents and individual real-world samples, but has **not** been benchmarked across large public corpora (such as the CUAD 510-contract dataset) or subjected to automated F1 accuracy scoring.
