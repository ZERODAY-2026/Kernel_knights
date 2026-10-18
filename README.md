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
|  | - Fact vs Risk Split  |     | Model: gemma4:e4b / gemma3n:e4b     |  |
|  | - Quote Highlighting  |     | Structured JSON + Citation Grounding|  |
|  +-----------------------+     +-------------------------------------+  |
+-------------------------------------------------------------------------+
           X  (Firewall / Wi-Fi Disabled: Zero External Calls)
           X  (Streamlit Telemetry Disabled via .streamlit/config.toml)
