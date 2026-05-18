from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_chat_service, get_current_principal, get_tenant_context
from app.application.dto.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatSessionCreateRequest,
    ChatSessionResponse,
)
from app.application.services.chat_service import ChatService
from app.core.security import Principal
from app.domain.common.context import TenantContext

router = APIRouter()


@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    request: ChatSessionCreateRequest,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: ChatService = Depends(get_chat_service),
) -> ChatSessionResponse:
    return await service.create_session(request, principal, tenant)


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    request: ChatMessageRequest,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: ChatService = Depends(get_chat_service),
) -> ChatMessageResponse:
    return await service.send_message(session_id, request, principal, tenant)

