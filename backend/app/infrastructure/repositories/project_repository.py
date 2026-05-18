from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.projects.models import Project
from app.infrastructure.db.models import ProjectRecord


class SqlAlchemyProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, project: Project) -> None:
        self._session.add(
            ProjectRecord(
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
        )
        await self._session.flush()

    async def list_by_tenant(self, tenant_id: str, *, limit: int, offset: int) -> list[Project]:
        result = await self._session.execute(
            select(ProjectRecord)
            .where(ProjectRecord.tenant_id == tenant_id)
            .where(ProjectRecord.status != "deleted")
            .order_by(ProjectRecord.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [_to_domain(record) for record in result.scalars().all()]

    async def get_by_id(self, tenant_id: str, project_id: str) -> Project | None:
        result = await self._session.execute(
            select(ProjectRecord)
            .where(ProjectRecord.tenant_id == tenant_id)
            .where(ProjectRecord.id == project_id)
            .limit(1)
        )
        record = result.scalar_one_or_none()
        return _to_domain(record) if record else None


def _to_domain(record: ProjectRecord) -> Project:
    return Project(
        id=record.id,
        tenant_id=record.tenant_id,
        name=record.name,
        business_owner=record.business_owner,
        criticality=record.criticality,
        regulatory_profile=list(record.regulatory_profile or []),
        description=record.description,
        status=record.status,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )

