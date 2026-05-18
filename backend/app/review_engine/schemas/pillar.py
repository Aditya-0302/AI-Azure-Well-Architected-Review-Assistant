from __future__ import annotations

from pydantic import Field

from app.review_engine.schemas.common import StrictBaseModel, WellArchitectedPillar
from app.review_engine.schemas.finding import ReviewFinding


class PillarReviewResult(StrictBaseModel):
    pillar: WellArchitectedPillar
    executive_summary: str
    technical_summary: str
    strengths: list[str]
    findings: list[ReviewFinding]
    missing_evidence_questions: list[str]
    maturity_level: int = Field(ge=0, le=5)
    score: int = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0, le=1)

