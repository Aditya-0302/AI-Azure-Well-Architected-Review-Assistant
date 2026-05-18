from __future__ import annotations

from app.application.dto.reviews import ArchitectureEvaluationRequest
from app.application.services.authorization_service import AuthorizationService
from app.core.security import Principal
from app.domain.common.context import TenantContext
from app.review_engine.orchestrator import ArchitectureReviewEngine
from app.review_engine.schemas.common import ArchitectureReviewContext
from app.review_engine.schemas.report import ArchitectureReviewResult


class ArchitectureReviewService:
    def __init__(
        self,
        *,
        authorization: AuthorizationService,
        review_engine: ArchitectureReviewEngine,
    ) -> None:
        self._authorization = authorization
        self._review_engine = review_engine

    async def evaluate_architecture(
        self,
        request: ArchitectureEvaluationRequest,
        principal: Principal,
        tenant: TenantContext,
    ) -> ArchitectureReviewResult:
        self._authorization.require_review_access(principal)
        context = ArchitectureReviewContext(
            tenant_id=tenant.tenant_id,
            project_id=request.project_id,
            architecture_version_id=request.architecture_version_id,
            workload_name=request.workload_name,
            workload_description=request.workload_description,
            business_criticality=request.business_criticality,
            environment=request.environment,
            regions=request.regions,
            azure_services=request.azure_services,
            compliance_requirements=request.compliance_requirements,
            target_rto=request.target_rto,
            target_rpo=request.target_rpo,
            monthly_budget_usd=request.monthly_budget_usd,
            architecture_summary=request.architecture_summary,
            evidence=request.evidence,
        )
        return await self._review_engine.evaluate(
            context=context,
            requested_pillars=request.requested_pillars or None,
        )

