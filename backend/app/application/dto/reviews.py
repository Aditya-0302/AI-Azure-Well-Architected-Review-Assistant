from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.review_engine.schemas.common import ReviewEvidence, WellArchitectedPillar


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


class ArchitectureEvaluationRequest(BaseModel):
    project_id: str | None = None
    architecture_version_id: str | None = None
    workload_name: str = Field(min_length=2, max_length=200)
    workload_description: str = Field(min_length=10, max_length=12000)
    business_criticality: str = Field(default="medium", max_length=64)
    environment: str = Field(default="production", max_length=64)
    regions: list[str] = Field(default_factory=list)
    azure_services: list[str] = Field(default_factory=list)
    compliance_requirements: list[str] = Field(default_factory=list)
    target_rto: str | None = Field(default=None, max_length=128)
    target_rpo: str | None = Field(default=None, max_length=128)
    monthly_budget_usd: float | None = Field(default=None, ge=0)
    architecture_summary: str = Field(min_length=20, max_length=24000)
    evidence: list[ReviewEvidence] = Field(default_factory=list)
    requested_pillars: list[WellArchitectedPillar] = Field(default_factory=list)

