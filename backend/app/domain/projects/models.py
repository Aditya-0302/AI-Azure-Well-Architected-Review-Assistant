from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Project:
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

