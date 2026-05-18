# Backend

Production-grade FastAPI backend foundation for AI Azure Well-Architected Review Assistant.

## Local Run

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Health endpoints:

- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`

Local auth mode accepts development bearer tokens only when `APP_ENV=local`, `AUTH_MODE=local`, and `AUTH_ALLOW_LOCAL_TOKENS=true`.

Example:

```text
Authorization: Bearer local:admin@example.com:admin,architect
```

