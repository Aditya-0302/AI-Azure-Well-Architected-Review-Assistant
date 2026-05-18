from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.application.dto.projects import ProjectCreateRequest, ProjectResponse
from app.application.ports.project_repository import ProjectRepository
from app.application.ports.unit_of_work import UnitOfWork
from app.application.services.authorization_service import AuthorizationService
from app.core.security import Principal
from app.domain.common.context import TenantContext
from app.domain.projects.models import Project


class ProjectService:
    def __init__(
        self,
        repository: ProjectRepository,
        unit_of_work: UnitOfWork,
        authorization: AuthorizationService,
    ) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work
        self._authorization = authorization

    async def create_project(
        self,
        request: ProjectCreateRequest,
        principal: Principal,
        tenant: TenantContext,
    ) -> ProjectResponse:
        self._authorization.require_project_write(principal)
        now = datetime.now(UTC)
        project = Project(
            id=str(uuid4()),
            tenant_id=tenant.tenant_id,
            name=request.name,
            business_owner=request.business_owner,
            criticality=request.criticality,
            regulatory_profile=request.regulatory_profile,
            description=request.description,
            status="active",
            created_at=now,
            updated_at=now,
        )
        await self._repository.add(project)
        await self._unit_of_work.commit()
        return _to_response(project)

    async def list_projects(
        self,
        principal: Principal,
        tenant: TenantContext,
        *,
        limit: int,
        offset: int,
    ) -> list[ProjectResponse]:
        self._authorization.require_read_access(principal)
        projects = await self._repository.list_by_tenant(tenant.tenant_id, limit=limit, offset=offset)
        return [_to_response(project) for project in projects]


def _to_response(project: Project) -> ProjectResponse:
    return ProjectResponse(
        id=project.id,
        tenant_id=project.tenant_id,
        name=project.name,
        business_owner=project.business_owner,
        criticality=project.criticality,
        regulatory_profile=project.regulatory_profile,
        description=project.description,
        status=project.status,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )

