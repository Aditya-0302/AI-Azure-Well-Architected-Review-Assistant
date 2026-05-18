from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.application.dto.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatSessionCreateRequest,
    ChatSessionResponse,
)
from app.application.services.authorization_service import AuthorizationService
from app.core.exceptions import DependencyUnavailableError
from app.core.security import Principal
from app.domain.common.context import TenantContext


class ChatService:
    def __init__(self, authorization: AuthorizationService) -> None:
        self._authorization = authorization

    async def create_session(
        self,
        request: ChatSessionCreateRequest,
        principal: Principal,
        tenant: TenantContext,
    ) -> ChatSessionResponse:
        self._authorization.require_read_access(principal)
        now = datetime.now(UTC)
        return ChatSessionResponse(
            id=str(uuid4()),
            project_id=request.project_id,
            review_id=request.review_id,
            title=request.title or "Architecture consultation",
            created_at=now,
        )

    async def send_message(
        self,
        session_id: str,
        request: ChatMessageRequest,
        principal: Principal,
        tenant: TenantContext,
    ) -> ChatMessageResponse:
        self._authorization.require_read_access(principal)
        raise DependencyUnavailableError(
            "Chat requires Azure OpenAI and retrieval adapters before inference can run.",
            code="chat_orchestrator_not_configured",
            details={"session_id": session_id, "tenant_id": tenant.tenant_id},
        )
