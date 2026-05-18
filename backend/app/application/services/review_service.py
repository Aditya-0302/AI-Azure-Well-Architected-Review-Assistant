from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.application.dto.reviews import ReviewCreateRequest, ReviewResponse, ReviewRunResponse
from app.application.services.authorization_service import AuthorizationService
from app.core.security import Principal
from app.domain.common.context import TenantContext


class ReviewService:
    def __init__(self, authorization: AuthorizationService) -> None:
        self._authorization = authorization

    async def create_review(
        self,
        request: ReviewCreateRequest,
        principal: Principal,
        tenant: TenantContext,
    ) -> ReviewResponse:
        self._authorization.require_review_access(principal)
        return ReviewResponse(
            id=str(uuid4()),
            project_id=request.project_id,
            architecture_version_id=request.architecture_version_id,
            status="draft",
            review_type=request.review_type,
            created_at=datetime.now(UTC),
        )

    async def start_review_run(
        self,
        review_id: str,
        principal: Principal,
        tenant: TenantContext,
    ) -> ReviewRunResponse:
        self._authorization.require_review_access(principal)
        return ReviewRunResponse(
            review_id=review_id,
            run_id=str(uuid4()),
            status="queued",
            queued_at=datetime.now(UTC),
        )

