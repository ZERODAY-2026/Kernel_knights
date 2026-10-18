# Security & Secrets Management

## 1. Zero Cloud Egress Architecture
- **On-Device Processing**: All document parsing, regex chunking, and AI inferences run strictly on `127.0.0.1` (localhost).
- **No Third-Party API Keys**: By design, no cloud LLM API keys (OpenAI, Anthropic, Google Cloud) are needed or accepted. This prevents confidential legal documents from ever leaking to external services.
- **Strict Network Isolation**: The FastAPI backend serves responses with a restrictive `Content-Security-Policy: default-src 'self'` and `Cache-Control: no-store` to prevent external script injection and client-side data leakage.

## 2. Managing Local Environment Secrets
If you add private certificates, session keys, or local authentication credentials:
1. Copy `.env.example` to `.env`:
   ```bash
   cp secret/.env.example secret/.env
   ```
2. Populate any local environment overrides.
3. The `.env` file and any `.key` or `.pem` files are protected by `.gitignore` and will never be committed to Git.
