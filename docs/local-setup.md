# Local Setup

Prerequisites: Git, Docker Desktop with Compose, Python 3.11+ for local tests.

1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. Visit the health endpoints and orchestrator `/docs`.
4. Run scaffold contract tests:

   ```bash
   pip install -r tests/requirements.txt
   python -m pytest tests -q
   ```

A green scaffold test does not mean real model inference works. Each model owner must add real inference tests and document evidence.
