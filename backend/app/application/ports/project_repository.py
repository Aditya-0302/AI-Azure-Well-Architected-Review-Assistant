from __future__ import annotations

from typing import Protocol

from app.domain.projects.models import Project


class ProjectRepository(Protocol):
    async def add(self, project: Project) -> None:
        """Persist a project aggregate."""

    async def list_by_tenant(self, tenant_id: str, *, limit: int, offset: int) -> list[Project]:
        """List projects visible in a tenant."""

    async def get_by_id(self, tenant_id: str, project_id: str) -> Project | None:
        """Get a project by tenant and ID."""

