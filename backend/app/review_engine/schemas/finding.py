from __future__ import annotations

from app.review_engine.schemas.common import (
    Citation,
    EvidenceStatus,
    FindingConfidence,
    FindingSeverity,
    RemediationEffort,
    StrictBaseModel,
    WellArchitectedPillar,
)


class ReviewFinding(StrictBaseModel):
    pillar: WellArchitectedPillar
    severity: FindingSeverity
    confidence: FindingConfidence
    evidence_status: EvidenceStatus
    category: str
    title: str
    description: str
    business_impact: str
    technical_impact: str
    recommendation: str
    azure_services: list[str]
    anti_patterns: list[str]
    missing_evidence: list[str]
    remediation_effort: RemediationEffort
    priority_rank: int
    citations: list[Citation]

