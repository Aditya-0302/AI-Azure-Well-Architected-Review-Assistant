from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class WellArchitectedPillar(StrEnum):
    SECURITY = "security"
    RELIABILITY = "reliability"
    COST_OPTIMIZATION = "cost_optimization"
    PERFORMANCE_EFFICIENCY = "performance_efficiency"
    OPERATIONAL_EXCELLENCE = "operational_excellence"


class FindingSeverity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class FindingConfidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EvidenceStatus(StrEnum):
    CONFIRMED = "confirmed"
    INFERRED = "inferred"
    MISSING_EVIDENCE = "missing_evidence"


class RemediationEffort(StrEnum):
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"


class Citation(StrictBaseModel):
    source_id: str = Field(description="Stable source or document identifier.")
    title: str = Field(description="Human-readable source title.")
    locator: str = Field(description="Page, chunk, URL fragment, section, or evidence locator.")
    evidence_summary: str = Field(description="Brief summary of what this citation supports.")


class ReviewEvidence(StrictBaseModel):
    source_id: str
    title: str
    content: str
    source_type: str = "architecture_evidence"
    locator: str = "provided_context"
    trust_level: str = "tenant_evidence"
    metadata: dict[str, str] = Field(default_factory=dict)


class ArchitectureReviewContext(StrictBaseModel):
    tenant_id: str
    project_id: str | None = None
    architecture_version_id: str | None = None
    workload_name: str
    workload_description: str
    business_criticality: str = "medium"
    environment: str = "production"
    regions: list[str] = Field(default_factory=list)
    azure_services: list[str] = Field(default_factory=list)
    compliance_requirements: list[str] = Field(default_factory=list)
    target_rto: str | None = None
    target_rpo: str | None = None
    monthly_budget_usd: float | None = None
    architecture_summary: str
    evidence: list[ReviewEvidence] = Field(default_factory=list)

