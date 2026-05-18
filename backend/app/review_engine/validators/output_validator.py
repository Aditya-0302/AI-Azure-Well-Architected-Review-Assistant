from __future__ import annotations

from app.core.exceptions import AppError
from app.review_engine.schemas.common import FindingSeverity, WellArchitectedPillar
from app.review_engine.schemas.pillar import PillarReviewResult


class ReviewOutputValidationError(AppError):
    status_code = 502
    code = "review_model_output_invalid"
    message = "The AI review model returned invalid review output."


class ReviewOutputValidator:
    MATERIAL_SEVERITIES = {FindingSeverity.CRITICAL, FindingSeverity.HIGH}

    def validate_pillar_result(
        self,
        result: PillarReviewResult,
        *,
        expected_pillar: WellArchitectedPillar,
    ) -> None:
        if result.pillar != expected_pillar:
            raise ReviewOutputValidationError(
                "Pillar result does not match the requested pillar.",
                details={"expected": expected_pillar, "actual": result.pillar},
            )

        for finding in result.findings:
            if finding.pillar != expected_pillar:
                raise ReviewOutputValidationError(
                    "Finding pillar does not match the requested pillar.",
                    details={
                        "expected": expected_pillar,
                        "actual": finding.pillar,
                        "title": finding.title,
                    },
                )
            if finding.severity in self.MATERIAL_SEVERITIES and (
                not finding.citations and not finding.missing_evidence
            ):
                raise ReviewOutputValidationError(
                    "Material finding must include citations or missing evidence.",
                    details={"title": finding.title, "severity": finding.severity},
                )

