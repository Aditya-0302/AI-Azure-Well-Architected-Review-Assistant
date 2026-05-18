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

## RAG Ingestion

The backend includes an enterprise RAG pipeline backed by:

- Azure Blob Storage for source documents
- LangChain recursive chunking
- Azure OpenAI embeddings through `langchain-openai`
- Azure AI Search vector, hybrid, and semantic-hybrid retrieval

Required configuration:

```text
AZURE_STORAGE_ACCOUNT_URL=https://<account>.blob.core.windows.net
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_SEARCH_ENDPOINT=https://<search-service>.search.windows.net
```

Managed identity is used by default. For local development, set `AZURE_OPENAI_API_KEY`,
`AZURE_SEARCH_API_KEY`, or `AZURE_STORAGE_CONNECTION_STRING` when RBAC is not available.

Ingest a blob:

```http
POST /api/v1/knowledge/ingestions/blob
Authorization: Bearer local:admin@example.com:admin,architect
Content-Type: application/json

{
  "container_name": "raw",
  "blob_name": "tenant-a/workload-review.md",
  "project_id": "project-123",
  "document_type": "architecture_evidence",
  "sensitivity_label": "internal"
}
```

Retrieve evidence:

```http
POST /api/v1/knowledge/retrieve
Authorization: Bearer local:manager@example.com:manager
Content-Type: application/json

{
  "query": "How is the architecture handling private endpoint access and key rotation?",
  "project_id": "project-123",
  "pillars": ["security"],
  "mode": "semantic_hybrid",
  "top_k": 8
}
```

The RAG index is created or updated automatically before ingestion using the configured
`RAG_*` settings. Search filters always include tenant scope and can include project,
architecture version, pillar, Azure service, document type, and sensitivity label.

## AI Review Engine

The backend includes a structured Azure Well-Architected review engine for:

- Security
- Reliability
- Cost Optimization
- Performance Efficiency
- Operational Excellence

The engine uses pillar-specific prompts, Azure OpenAI chat completions, strict JSON
response schemas, Pydantic validation, citation guardrails, deterministic scoring,
and cross-pillar synthesis.

Evaluate an architecture:

```http
POST /api/v1/reviews/evaluate
Authorization: Bearer local:architect@example.com:architect
Content-Type: application/json

{
  "project_id": "project-123",
  "architecture_version_id": "v1",
  "workload_name": "Enterprise Claims Platform",
  "workload_description": "Customer-facing claims workflow hosted on Azure.",
  "business_criticality": "high",
  "environment": "production",
  "regions": ["eastus", "westus3"],
  "azure_services": ["app_service", "azure_sql", "key_vault", "front_door"],
  "compliance_requirements": ["SOC2", "HIPAA"],
  "target_rto": "1 hour",
  "target_rpo": "15 minutes",
  "architecture_summary": "The workload uses Azure Front Door, App Service, Azure SQL, Key Vault, and Log Analytics...",
  "evidence": [
    {
      "source_id": "arch-doc-1",
      "title": "Architecture Design",
      "content": "App Service is deployed in two regions. Azure SQL failover group is configured...",
      "source_type": "architecture_evidence",
      "locator": "section 2.1",
      "trust_level": "tenant_evidence",
      "metadata": {}
    }
  ],
  "requested_pillars": []
}
```

Leave `requested_pillars` empty to run all five pillars, or provide a subset such as
`["security", "reliability"]`.
