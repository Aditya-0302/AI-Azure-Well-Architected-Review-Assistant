from __future__ import annotations

from app.application.ports.review_model import StructuredReviewModel
from app.review_engine.prompts.registry import SYSTEM_PROMPT, build_pillar_prompt
from app.review_engine.schemas.common import ArchitectureReviewContext, WellArchitectedPillar
from app.review_engine.schemas.pillar import PillarReviewResult
from app.review_engine.validators.output_validator import ReviewOutputValidator


class PillarAnalyzer:
    def __init__(
        self,
        *,
        pillar: WellArchitectedPillar,
        model: StructuredReviewModel,
        validator: ReviewOutputValidator,
    ) -> None:
        self._pillar = pillar
        self._model = model
        self._validator = validator

    async def analyze(self, context: ArchitectureReviewContext) -> PillarReviewResult:
        result = await self._model.complete_json(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=build_pillar_prompt(pillar=self._pillar, context=context),
            response_model=PillarReviewResult,
            schema_name=f"{self._pillar.value}_pillar_review",
            temperature=0.1,
        )
        self._validator.validate_pillar_result(result, expected_pillar=self._pillar)
        return result

