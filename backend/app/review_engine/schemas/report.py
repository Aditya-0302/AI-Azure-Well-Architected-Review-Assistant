from __future__ import annotations

from pydantic import Field

from app.review_engine.schemas.common import StrictBaseModel, WellArchitectedPillar
from app.review_engine.schemas.finding import ReviewFinding
from app.review_engine.schemas.pillar import PillarReviewResult


class PillarScore(StrictBaseModel):
    pillar: WellArchitectedPillar
    score: int = Field(ge=0, le=100)
    maturity_level: int = Field(ge=0, le=5)
    confidence_score: float = Field(ge=0, le=1)
    critical_findings: int
    high_findings: int
    medium_findings: int
    low_findings: int


class ImprovementRoadmapItem(StrictBaseModel):
    sequence: int
    title: str
    pillar: WellArchitectedPillar
    rationale: str
    expected_outcome: str
    effort: str
    dependencies: list[str]
    related_finding_titles: list[str]


class ReviewSynthesisResult(StrictBaseModel):
    executive_summary: str
    architecture_maturity_score: int = Field(ge=0, le=100)
    overall_maturity_level: int = Field(ge=0, le=5)
    top_risks: list[str]
    cross_pillar_tradeoffs: list[str]
    modernization_opportunities: list[str]
    improvement_roadmap: list[ImprovementRoadmapItem]


class ArchitectureReviewResult(StrictBaseModel):
    review_id: str
    tenant_id: str
    project_id: str | None
    architecture_version_id: str | None
    model_alias: str
    prompt_version: str
    pillar_results: list[PillarReviewResult]
    pillar_scores: list[PillarScore]
    findings: list[ReviewFinding]
    synthesis: ReviewSynthesisResult

