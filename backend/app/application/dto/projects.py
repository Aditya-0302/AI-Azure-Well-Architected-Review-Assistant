from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    business_owner: str | None = Field(default=None, max_length=200)
    criticality: str = Field(default="medium", pattern="^(low|medium|high|mission_critical)$")
    regulatory_profile: list[str] = Field(default_factory=list)
    description: str | None = Field(default=None, max_length=4000)


class ProjectResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    business_owner: str | None
    criticality: str
    regulatory_profile: list[str]
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

