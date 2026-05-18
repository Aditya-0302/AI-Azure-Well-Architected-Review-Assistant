from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_principal, get_tenant_service
from app.application.dto.tenants import TenantResponse
from app.application.services.tenant_service import TenantService
from app.core.security import Principal

router = APIRouter()


@router.get("/current", response_model=TenantResponse)
async def current_tenant(
    principal: Principal = Depends(get_current_principal),
    service: TenantService = Depends(get_tenant_service),
) -> TenantResponse:
    return await service.get_current_tenant(principal)

