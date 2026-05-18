from __future__ import annotations

from app.application.ports.review_model import StructuredReviewModel
from app.review_engine.analyzers.pillar_analyzer import PillarAnalyzer
from app.review_engine.schemas.common import WellArchitectedPillar
from app.review_engine.validators.output_validator import ReviewOutputValidator


class PillarAnalyzerFactory:
    def __init__(self, model: StructuredReviewModel, validator: ReviewOutputValidator) -> None:
        self._model = model
        self._validator = validator

    def create(self, pillar: WellArchitectedPillar) -> PillarAnalyzer:
        return PillarAnalyzer(pillar=pillar, model=self._model, validator=self._validator)

