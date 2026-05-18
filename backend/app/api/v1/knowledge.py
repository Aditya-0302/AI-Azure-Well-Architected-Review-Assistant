from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_current_principal,
    get_rag_ingestion_service,
    get_rag_retrieval_service,
    get_tenant_context,
)
from app.application.dto.knowledge import (
    BlobIngestionRequest,
    IngestionResponse,
    RetrievalRequest,
    RetrievalResponse,
)
from app.application.services.rag_ingestion_service import RagIngestionService
from app.application.services.rag_retrieval_service import RagRetrievalService
from app.core.security import Principal
from app.domain.common.context import TenantContext

router = APIRouter()


@router.post(
    "/ingestions/blob",
    response_model=IngestionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def ingest_blob(
    request: BlobIngestionRequest,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: RagIngestionService = Depends(get_rag_ingestion_service),
) -> IngestionResponse:
    return await service.ingest_blob(request, principal, tenant)


@router.post("/retrieve", response_model=RetrievalResponse)
async def retrieve(
    request: RetrievalRequest,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: RagRetrievalService = Depends(get_rag_retrieval_service),
) -> RetrievalResponse:
    return await service.retrieve(request, principal, tenant)

