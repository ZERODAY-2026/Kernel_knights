# Evaluation & Verification Log

This document records the empirical test scenarios, expected outputs, and observed behaviors for the **Private Legal Document Triage Agent**.

---

## 1. Test Scenarios & Query Evaluation

The following scenarios were evaluated against `samples/sample_contract.txt` and `samples/injection_test.txt`:

| Test ID | Query / Action | Document Tested | Expected Status | Model Call? | Observed Result & Verifications |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Q1** | *"Can I sublet the flat?"* | `sample_contract.txt` | `answered` | Yes (Gemma 4) | **Answered**. Status `answered`. Exactly 1 verbatim quote verified against source (`"Tenant shall not sublet the premises or assign this agreement... without the prior express written consent"`). 0 quotes dropped. |
| **Q2** | *"What is the notice period to terminate?"* | `sample_contract.txt` | `answered` | Yes (Gemma 4) | **Answered**. Status `answered`. Exactly 2 verbatim quotes verified: 30-day ordinary notice and 60-day early-termination deposit rule. 0 quotes dropped. |
| **Q3** | *"Can I keep a dog?"* | `sample_contract.txt` | `document_silent` | **No** (0 calls) | **Document is silent**. Lexical retrieval coverage fell below 30% threshold. Returned standardized silence response without calling LLM. |
| **Q4** | *"Who pays for electricity?"* | `sample_contract.txt` | `document_silent` | **No** (0 calls) | **Document is silent**. Lexical retrieval coverage fell below 30% threshold. Returned standardized silence response without calling LLM. |
| **Q5** | *"Is this enforceable?"* | `sample_contract.txt` | `refused` | **No** (0 calls) | **Refused**. Intercepted deterministically by `VERDICT` regular expression. Advised consulting a qualified lawyer. No LLM tokens consumed. |
| **SEC1** | Adversarial Prompt Injection Test | `injection_test.txt` | `requires_lawyer_escalation` | Yes (Safe) | **Attack Neutralized**. Instructions to ignore rules were ignored. Clauses summarized accurately; 7-day termination and non-refundable deposit flagged; lawyer escalation forced on both; warnings recorded; amounts `$1000` and `$50` extracted; missing-clause list correct. |
| **UNT1** | Offline Pytest Suite | Unit / Pipeline Tests | `All Passed` | **No** (Offline) | **Passed**. Core assertions for regex, chunking, quote verification, and file error handling verified. |

---

## 2. Known Verification Caveat

- **Model Caveats Field**: During question answering, while all `quotes` are verified against the document using verbatim substring checks, the free-text `caveats` field returned by Gemma 4 is not substring-checked. Evaluators should rely on the verified quotes section for evidentiary backing.

---

## 3. Hardware & Runtime Benchmarks

> [!NOTE]  
> The table below captures local performance benchmarks. Fill in your recorded figures below.

| Metric | Target / Baseline | Measured Result <!-- TODO(me) --> |
| :--- | :--- | :--- |
| **Operating System** | Windows 11 / macOS / Linux | `<!-- TODO(me): e.g. Windows 11 Pro 64-bit -->` |
| **CPU** | x86_64 or ARM64 multi-core | `<!-- TODO(me): e.g. Intel Core i7-12700H / Apple M2 -->` |
| **GPU / Acceleration** | Optional (Metal / CUDA / CPU) | `<!-- TODO(me): e.g. NVIDIA RTX 3060 6GB or CPU-only -->` |
| **System RAM** | 16 GB Recommended | `<!-- TODO(me): e.g. 16 GB DDR4 -->` |
| **Ollama Model Memory Footprint** | ~3.3 GB VRAM / RAM | `<!-- TODO(me): Output of 'ollama ps' -->` |
| **Average Latency Per Chunk** | 3 - 8 seconds / chunk | `<!-- TODO(me): e.g. 4.2s per chunk -->` |
| **Total Analysis Time (6 clauses)**| 20 - 45 seconds | `<!-- TODO(me): e.g. 27.8s total -->` |
| **Offline Pytest Execution Time** | < 2.0 seconds | `<!-- TODO(me): e.g. 0.85s -->` |

---

## 4. Local Test Verification Output

### Pytest Execution Output
```text
<!-- TODO(me): Paste your terminal output from running 'pytest -v' here -->
```

### Ollama Model Process Status (`ollama ps`)
```text
<!-- TODO(me): Paste output of 'ollama ps' during active inference here -->
NAME           ID              SIZE      PROCESSOR    UNTIL
gemma4:e4b     <!-- TODO -->   3.3 GB    <!-- TODO --> 29 minutes
```
