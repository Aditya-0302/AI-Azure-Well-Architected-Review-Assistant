from __future__ import annotations

from pydantic import BaseModel, EmailStr


class CurrentUserResponse(BaseModel):
    subject: str
    tenant_id: str | None
    email: EmailStr | None
    display_name: str | None
    roles: list[str]
    scopes: list[str]

