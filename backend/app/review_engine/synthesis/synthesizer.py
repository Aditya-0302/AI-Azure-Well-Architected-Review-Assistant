from __future__ import annotations

import json

from app.application.ports.review_model import StructuredReviewModel
from app.review_engine.prompts.registry import SYNTHESIS_SYSTEM_PROMPT, build_synthesis_prompt
from app.review_engine.schemas.common import ArchitectureReviewContext
from app.review_engine.schemas.pillar import PillarReviewResult
from app.review_engine.schemas.report import ReviewSynthesisResult


class ReviewSynthesizer:
    def __init__(self, model: StructuredReviewModel) -> None:
        self._model = model

    async def synthesize(
        self,
        *,
        context: ArchitectureReviewContext,
        pillar_results: list[PillarReviewResult],
    ) -> ReviewSynthesisResult:
        pillar_json = json.dumps(
            [result.model_dump(mode="json") for result in pillar_results],
            separators=(",", ":"),
        )
        return await self._model.complete_json(
            system_prompt=SYNTHESIS_SYSTEM_PROMPT,
            user_prompt=build_synthesis_prompt(context=context, pillar_json=pillar_json),
            response_model=ReviewSynthesisResult,
            schema_name="architecture_review_synthesis",
            temperature=0.1,
        )

