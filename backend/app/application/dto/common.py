from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Role(StrEnum):
    ADMIN = "admin"
    ARCHITECT = "architect"
    REVIEWER = "reviewer"
    MANAGER = "manager"


class ResourceStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DISABLED = "disabled"


class MessageResponse(BaseModel):
    message: str


class OperationAcceptedResponse(BaseModel):
    operation_id: str
    status: str = "accepted"
    links: dict[str, str] = Field(default_factory=dict)

