from __future__ import annotations

from app.application.dto.knowledge import (
    RetrievalCitation,
    RetrievalRequest,
    RetrievalResponse,
    RetrievalResult,
)
from app.application.ports.rag import EmbeddingProvider, KnowledgeIndex
from app.application.services.authorization_service import AuthorizationService
from app.core.config import Settings
from app.core.security import Principal
from app.domain.common.context import TenantContext


class RagRetrievalService:
    def __init__(
        self,
        *,
        settings: Settings,
        embedding_provider: EmbeddingProvider,
        knowledge_index: KnowledgeIndex,
        authorization: AuthorizationService,
    ) -> None:
        self._settings = settings
        self._embedding_provider = embedding_provider
        self._knowledge_index = knowledge_index
        self._authorization = authorization

    async def retrieve(
        self,
        request: RetrievalRequest,
        principal: Principal,
        tenant: TenantContext,
    ) -> RetrievalResponse:
        self._authorization.require_read_access(principal)
        query_vector = await self._embedding_provider.embed_query(request.query)
        results = await self._knowledge_index.search(
            query=request.query,
            query_vector=query_vector,
            tenant_id=tenant.tenant_id,
            mode=request.mode,
            top_k=request.top_k or self._settings.rag_default_top_k,
            filters={
                "project_id": request.project_id,
                "architecture_version_id": request.architecture_version_id,
                "pillars": request.pillars,
                "azure_services": request.azure_services,
                "document_type": request.document_type,
                "sensitivity_label": request.sensitivity_label,
            },
        )

        return RetrievalResponse(
            query=request.query,
            mode=request.mode,
            index_name=self._settings.resolved_rag_index_name,
            results=[
                RetrievalResult(
                    chunk_id=result.chunk_id,
                    document_id=result.document_id,
                    content=result.content,
                    score=result.score,
                    reranker_score=result.reranker_score,
                    metadata=result.metadata,
                    citation=RetrievalCitation(
                        document_id=result.document_id,
                        chunk_id=result.chunk_id,
                        source_uri=_str_or_none(result.metadata.get("source_uri")),
                        file_name=_str_or_none(result.metadata.get("file_name")),
                    ),
                )
                for result in results
            ],
        )


def _str_or_none(value: object) -> str | None:
    return value if isinstance(value, str) else None

