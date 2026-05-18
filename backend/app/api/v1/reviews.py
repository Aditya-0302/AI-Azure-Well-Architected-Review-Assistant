from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_architecture_review_service,
    get_current_principal,
    get_review_service,
    get_tenant_context,
)
from app.application.dto.reviews import (
    ArchitectureEvaluationRequest,
    ReviewCreateRequest,
    ReviewResponse,
    ReviewRunResponse,
)
from app.application.services.architecture_review_service import ArchitectureReviewService
from app.application.services.review_service import ReviewService
from app.core.security import Principal
from app.domain.common.context import TenantContext
from app.review_engine.schemas.report import ArchitectureReviewResult

router = APIRouter()


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    request: ReviewCreateRequest,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: ReviewService = Depends(get_review_service),
) -> ReviewResponse:
    return await service.create_review(request, principal, tenant)


@router.post("/{review_id}/run", response_model=ReviewRunResponse, status_code=status.HTTP_202_ACCEPTED)
async def run_review(
    review_id: str,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: ReviewService = Depends(get_review_service),
) -> ReviewRunResponse:
    return await service.start_review_run(review_id, principal, tenant)


@router.post(
    "/evaluate",
    response_model=ArchitectureReviewResult,
    status_code=status.HTTP_200_OK,
)
async def evaluate_architecture(
    request: ArchitectureEvaluationRequest,
    principal: Principal = Depends(get_current_principal),
    tenant: TenantContext = Depends(get_tenant_context),
    service: ArchitectureReviewService = Depends(get_architecture_review_service),
) -> ArchitectureReviewResult:
    return await service.evaluate_architecture(request, principal, tenant)
