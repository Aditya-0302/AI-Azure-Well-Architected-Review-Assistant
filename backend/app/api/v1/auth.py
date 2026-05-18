from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_principal
from app.application.dto.identity import CurrentUserResponse
from app.core.security import Principal

router = APIRouter()


@router.get("/me", response_model=CurrentUserResponse)
async def me(principal: Principal = Depends(get_current_principal)) -> CurrentUserResponse:
    return CurrentUserResponse(
        subject=principal.subject,
        tenant_id=principal.tenant_id,
        email=principal.email,
        display_name=principal.display_name,
        roles=sorted(principal.roles),
        scopes=sorted(principal.scopes),
    )

