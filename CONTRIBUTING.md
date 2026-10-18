# Contributing to Private Legal Document Triage Agent

Thank you for your interest in contributing. This project was developed for **ZeroDay OSS Hacktoberfest 2026 (IIIT Dharwad, Problem Statement 2)** as a privacy-first, on-device legal comprehension tool.

---

## Core Development Principles

Before contributing code, please ensure your changes uphold our strict architectural boundaries:

1. **Zero External Network Calls at Runtime**:
   - The application must remain 100% functional without an active internet connection.
   - Never add cloud API calls, analytics, remote logging, or external font/script CDN imports.
   - Ollama and FastAPI connections must remain hard-coded to `127.0.0.1`.
2. **Defensive Verification in Deterministic Code**:
   - Do not trust LLM outputs for citations or safety decisions. Verbatim verification, prompt-injection defense, and legal verdict refusals must remain enforced in deterministic Python code.
3. **No Definitive Legal Advice**:
   - The tool must never evaluate whether a clause is legal, valid, or enforceable under applicable law.
   - The disclaimer must remain visible across the UI and CLI outputs.
4. **Minimal Dependencies**:
   - Keep `requirements.txt` minimal. Avoid heavy ML frameworks, separate vector databases, or AGPL-licensed libraries.

---

## Local Development Workflow

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/ZERODAY-2026/Kernel_knights.git
cd Kernel_knights

# Create virtual environment
python -m venv .venv

# Activate on Windows PowerShell:
.venv\Scripts\Activate.ps1

# Activate on macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify with Test Suite

All unit and regression tests run offline without requiring a running Ollama daemon:

```bash
pytest -v
```

Ensure all tests pass before submitting any changes.

### 3. Running the Application Locally

Start your local Ollama server with Gemma 4:

```bash
ollama run gemma4:e4b
```

Run the local web server:

```bash
python api.py
```

Access the UI at `http://127.0.0.1:8000`.

---

## Pull Request Guidelines

1. **Focused Changes**: Keep PRs small and focused on a single bug fix, performance optimization, or documentation improvement.
2. **Add Tests**: When fixing a bug or adding an edge case handler, provide a corresponding test in `tests/test_pipeline.py`.
3. **No Synthetic PII**: Never commit real consumer contracts or personal identifiable information. Only commit synthetic test files to `samples/`.
4. **Format & Style**: Maintain PEP 8 style for Python code and semantic, standard HTML/CSS/JS for frontend assets.
