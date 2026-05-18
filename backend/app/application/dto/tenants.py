from __future__ import annotations

from pydantic import BaseModel


class TenantResponse(BaseModel):
    id: str
    name: str
    slug: str
    environment: str
    isolation_mode: str = "shared"

