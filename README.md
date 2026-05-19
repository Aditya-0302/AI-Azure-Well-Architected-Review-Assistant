# AI Azure Well-Architected Review Assistant

Enterprise SaaS platform blueprint for automating Azure Well-Architected reviews with Azure OpenAI, Azure AI Search, retrieval-augmented generation, document ingestion, review scoring, chat-based consulting, and production-grade governance.

Architecture deliverables:

- [Enterprise System Architecture](docs/architecture/enterprise-system-architecture.md)
- [Backend Architecture](docs/architecture/backend-architecture.md)

Backend implementation:

- [FastAPI Backend](backend/README.md)

## How to Run Locally

This guide provides step-by-step instructions to run the full application (frontend and backend) on your local machine with complete functionality.

### Prerequisites

- **Python 3.10+** (for the FastAPI backend)
- **Node.js 18+** (for the Next.js frontend)
- **Docker** (for running local PostgreSQL and Redis containers)
- **Azure Subscription** (required for full AI functionality: Azure OpenAI, AI Search, and Blob Storage)

### 1. Start Local Infrastructure

The project includes a `docker-compose.yml` file to quickly spin up the local database (PostgreSQL) and cache (Redis).

```bash
# In the root directory, start the containers in the background
docker-compose up -d
```

### 2. Configure and Run the Backend

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```powershell
   # Windows
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Configure environment variables. Copy the example file and update it with your credentials:
   ```powershell
   # Windows
   Copy-Item .env.example .env
   ```
   *For complete AI functionality, populate your `.env` with actual values for `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_API_KEY`, and `AZURE_STORAGE_CONNECTION_STRING`.*
   *For local authentication without Entra ID, ensure `APP_ENV=local`, `AUTH_MODE=local`, and `AUTH_ALLOW_LOCAL_TOKENS=true` are set.*

5. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   *The backend health endpoints will be available at `http://127.0.0.1:8000/api/v1/health/live`.*

### 3. Configure and Run the Frontend

1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:3000` to view the full application.
