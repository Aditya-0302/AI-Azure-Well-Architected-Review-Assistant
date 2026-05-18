from __future__ import annotations

import asyncio
from uuid import uuid4

from app.review_engine.analyzers.factory import PillarAnalyzerFactory
from app.review_engine.prompts.registry import PROMPT_VERSION
from app.review_engine.schemas.common import ArchitectureReviewContext, FindingSeverity, WellArchitectedPillar
from app.review_engine.schemas.finding import ReviewFinding
from app.review_engine.schemas.pillar import PillarReviewResult
from app.review_engine.schemas.report import ArchitectureReviewResult, PillarScore
from app.review_engine.scoring.score_calculator import PillarScoreCalculator
from app.review_engine.synthesis.synthesizer import ReviewSynthesizer


class ArchitectureReviewEngine:
    DEFAULT_PILLARS = [
        WellArchitectedPillar.SECURITY,
        WellArchitectedPillar.RELIABILITY,
        WellArchitectedPillar.COST_OPTIMIZATION,
        WellArchitectedPillar.PERFORMANCE_EFFICIENCY,
        WellArchitectedPillar.OPERATIONAL_EXCELLENCE,
    ]

    SEVERITY_ORDER = {
        FindingSeverity.CRITICAL: 0,
        FindingSeverity.HIGH: 1,
        FindingSeverity.MEDIUM: 2,
        FindingSeverity.LOW: 3,
        FindingSeverity.INFORMATIONAL: 4,
    }

    def __init__(
        self,
        *,
        analyzer_factory: PillarAnalyzerFactory,
        score_calculator: PillarScoreCalculator,
        synthesizer: ReviewSynthesizer,
        model_alias: str,
    ) -> None:
        self._analyzer_factory = analyzer_factory
        self._score_calculator = score_calculator
        self._synthesizer = synthesizer
        self._model_alias = model_alias

    async def evaluate(
        self,
        *,
        context: ArchitectureReviewContext,
        requested_pillars: list[WellArchitectedPillar] | None = None,
    ) -> ArchitectureReviewResult:
        pillars = requested_pillars or self.DEFAULT_PILLARS
        pillar_results = await asyncio.gather(
            *(self._analyzer_factory.create(pillar).analyze(context) for pillar in pillars)
        )
        pillar_scores = [self._score_calculator.calculate(result) for result in pillar_results]
        adjusted_results = self._apply_deterministic_scores(pillar_results, pillar_scores)
        findings = self._sort_findings(
            [finding for result in adjusted_results for finding in result.findings]
        )
        synthesis = await self._synthesizer.synthesize(
            context=context,
            pillar_results=adjusted_results,
        )

        return ArchitectureReviewResult(
            review_id=str(uuid4()),
            tenant_id=context.tenant_id,
            project_id=context.project_id,
            architecture_version_id=context.architecture_version_id,
            model_alias=self._model_alias,
            prompt_version=PROMPT_VERSION,
            pillar_results=adjusted_results,
            pillar_scores=pillar_scores,
            findings=findings,
            synthesis=synthesis,
        )

    @staticmethod
    def _apply_deterministic_scores(
        pillar_results: list[PillarReviewResult],
        pillar_scores: list[PillarScore],
    ) -> list[PillarReviewResult]:
        scores_by_pillar = {score.pillar: score for score in pillar_scores}
        return [
            result.model_copy(
                update={
                    "score": scores_by_pillar[result.pillar].score,
                    "maturity_level": scores_by_pillar[result.pillar].maturity_level,
                    "confidence_score": scores_by_pillar[result.pillar].confidence_score,
                }
            )
            for result in pillar_results
        ]

    def _sort_findings(self, findings: list[ReviewFinding]) -> list[ReviewFinding]:
        return sorted(
            findings,
            key=lambda finding: (self.SEVERITY_ORDER[finding.severity], finding.priority_rank),
        )

