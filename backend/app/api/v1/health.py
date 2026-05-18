from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.core.config import Settings, get_settings
from app.core.exceptions import DependencyUnavailableError

router = APIRouter()


@router.get("/health/live")
async def live(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@router.get("/health/ready")
async def ready(session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    try:
        await session.execute(text("select 1"))
    except SQLAlchemyError as exc:
        raise DependencyUnavailableError(
            "Database readiness check failed.",
            code="database_unavailable",
        ) from exc
    return {"status": "ready"}

