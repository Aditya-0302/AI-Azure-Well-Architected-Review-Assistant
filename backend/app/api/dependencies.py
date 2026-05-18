from __future__ import annotations

from collections.abc import AsyncIterator, Callable

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.authorization_service import AuthorizationService
from app.application.services.chat_service import ChatService
from app.application.services.project_service import ProjectService
from app.application.services.review_service import ReviewService
from app.application.services.tenant_service import TenantService
from app.application.services.upload_service import LocalDevelopmentBlobStorage, UploadService
from app.core.config import Settings, get_settings
from app.core.exceptions import AuthenticationError, PermissionDeniedError
from app.core.logging import set_tenant_id, set_user_id
from app.core.security import Principal, TokenValidator
from app.domain.common.context import TenantContext
from app.infrastructure.db.session import session_scope
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.repositories.project_repository import SqlAlchemyProjectRepository

bearer_scheme = HTTPBearer(auto_error=False)


async def get_db_session(settings: Settings = Depends(get_settings)) -> AsyncIterator[AsyncSession]:
    async for session in session_scope(settings):
        yield session


async def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> Principal:
    if credentials is None:
        raise AuthenticationError("Missing bearer token.")

    validator = TokenValidator(settings)
    principal = await validator.validate(credentials.credentials)
    set_user_id(principal.subject)
    set_tenant_id(principal.tenant_id)
    return principal


async def get_tenant_context(
    principal: Principal = Depends(get_current_principal),
) -> TenantContext:
    if not principal.tenant_id:
        raise AuthenticationError("Token does not contain a tenant claim.")
    return TenantContext(
        tenant_id=principal.tenant_id,
        user_id=principal.subject,
        roles=principal.roles,
    )


def require_roles(*roles: str) -> Callable[[Principal], Principal]:
    async def dependency(principal: Principal = Depends(get_current_principal)) -> Principal:
        if principal.is_admin or principal.has_role(*roles):
            return principal
        raise PermissionDeniedError()

    return dependency


def get_authorization_service() -> AuthorizationService:
    return AuthorizationService()


def get_tenant_service(settings: Settings = Depends(get_settings)) -> TenantService:
    return TenantService(settings)


def get_project_service(
    session: AsyncSession = Depends(get_db_session),
    authorization: AuthorizationService = Depends(get_authorization_service),
) -> ProjectService:
    return ProjectService(
        repository=SqlAlchemyProjectRepository(session),
        unit_of_work=SqlAlchemyUnitOfWork(session),
        authorization=authorization,
    )


def get_upload_service(
    authorization: AuthorizationService = Depends(get_authorization_service),
) -> UploadService:
    return UploadService(blob_storage=LocalDevelopmentBlobStorage(), authorization=authorization)


def get_review_service(
    authorization: AuthorizationService = Depends(get_authorization_service),
) -> ReviewService:
    return ReviewService(authorization=authorization)


def get_chat_service(
    authorization: AuthorizationService = Depends(get_authorization_service),
) -> ChatService:
    return ChatService(authorization=authorization)
