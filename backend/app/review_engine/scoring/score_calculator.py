from __future__ import annotations

from collections import Counter

from app.review_engine.schemas.common import EvidenceStatus, FindingSeverity
from app.review_engine.schemas.pillar import PillarReviewResult
from app.review_engine.schemas.report import PillarScore


class PillarScoreCalculator:
    PENALTIES = {
        FindingSeverity.CRITICAL: 25,
        FindingSeverity.HIGH: 15,
        FindingSeverity.MEDIUM: 8,
        FindingSeverity.LOW: 3,
        FindingSeverity.INFORMATIONAL: 0,
    }

    def calculate(self, result: PillarReviewResult) -> PillarScore:
        counts = Counter(finding.severity for finding in result.findings)
        weighted_penalty = 0
        for finding in result.findings:
            penalty = self.PENALTIES[finding.severity]
            if finding.evidence_status == EvidenceStatus.INFERRED:
                penalty = int(penalty * 0.7)
            elif finding.evidence_status == EvidenceStatus.MISSING_EVIDENCE:
                penalty = int(penalty * 0.5) + 3
            weighted_penalty += penalty

        missing_evidence_penalty = min(15, len(result.missing_evidence_questions) * 3)
        deterministic_score = max(0, 100 - weighted_penalty - missing_evidence_penalty)

        if counts[FindingSeverity.CRITICAL] > 0:
            deterministic_score = min(deterministic_score, 59)
        elif counts[FindingSeverity.HIGH] > 2:
            deterministic_score = min(deterministic_score, 74)

        score = min(result.score, deterministic_score)
        maturity_level = min(result.maturity_level, self._maturity_from_score(score))
        return PillarScore(
            pillar=result.pillar,
            score=score,
            maturity_level=maturity_level,
            confidence_score=result.confidence_score,
            critical_findings=counts[FindingSeverity.CRITICAL],
            high_findings=counts[FindingSeverity.HIGH],
            medium_findings=counts[FindingSeverity.MEDIUM],
            low_findings=counts[FindingSeverity.LOW],
        )

    @staticmethod
    def _maturity_from_score(score: int) -> int:
        if score >= 90:
            return 5
        if score >= 80:
            return 4
        if score >= 65:
            return 3
        if score >= 50:
            return 2
        if score >= 30:
            return 1
        return 0

