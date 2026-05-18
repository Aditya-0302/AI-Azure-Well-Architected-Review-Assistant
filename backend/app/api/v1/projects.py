from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import (
    get_current_principal,
    get_project_service,
    get_tenant_context,
)
from app.api.responses import PageMeta, PagedEnvelope
from app.application.dto.projects import ProjectCreateRequest, ProjectResponse
from app.application.services.project_service import ProjectService
from app.core.security import Principal
from app.domain.common.context import TenantContext

router = APIRouter()


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: ProjectCreateRequest,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    return await service.create_project(request, principal, tenant)


@router.get("", response_model=PagedEnvelope[ProjectResponse])
async def list_projects(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: ProjectService = Depends(get_project_service),
) -> PagedEnvelope[ProjectResponse]:
    data = await service.list_projects(principal, tenant, limit=limit, offset=offset)
    return PagedEnvelope(data=data, meta=PageMeta(limit=limit, offset=offset))

