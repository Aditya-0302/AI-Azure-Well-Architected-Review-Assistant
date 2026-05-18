from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreateRequest(BaseModel):
    project_id: str
    architecture_version_id: str
    review_type: str = Field(default="well_architected", pattern="^(well_architected|targeted)$")
    requested_pillars: list[str] = Field(default_factory=list)


class ReviewResponse(BaseModel):
    id: str
    project_id: str
    architecture_version_id: str
    status: str
    review_type: str
    created_at: datetime


class ReviewRunResponse(BaseModel):
    review_id: str
    run_id: str
    status: str
    queued_at: datetime

