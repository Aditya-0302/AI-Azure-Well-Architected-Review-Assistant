from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_current_principal, get_tenant_context, get_upload_service
from app.application.dto.uploads import (
    UploadCompleteRequest,
    UploadInitiateRequest,
    UploadInitiateResponse,
    UploadStatusResponse,
)
from app.application.services.upload_service import UploadService
from app.core.security import Principal
from app.domain.common.context import TenantContext

router = APIRouter()


@router.post("/initiate", response_model=UploadInitiateResponse, status_code=status.HTTP_201_CREATED)
async def initiate_upload(
    request: UploadInitiateRequest,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: UploadService = Depends(get_upload_service),
) -> UploadInitiateResponse:
    return await service.initiate_upload(request, principal, tenant)


@router.post("/complete", response_model=UploadStatusResponse)
async def complete_upload(
    request: UploadCompleteRequest,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: UploadService = Depends(get_upload_service),
) -> UploadStatusResponse:
    return await service.complete_upload(request, principal, tenant)
