from __future__ import annotations

import json
from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.identity.aio import DefaultAzureCredential
from azure.search.documents.aio import SearchClient
from azure.search.documents.indexes.aio import SearchIndexClient
from azure.search.documents.models import VectorizedQuery

from app.application.dto.knowledge import RetrievalMode
from app.core.config import Settings
from app.core.exceptions import DependencyUnavailableError
from app.infrastructure.azure_search.index_schema import build_knowledge_index
from app.rag.models import KnowledgeChunk, SearchResult


class AzureAISearchKnowledgeIndex:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        if not settings.azure_search_endpoint:
            raise DependencyUnavailableError(
                "AZURE_SEARCH_ENDPOINT is required for knowledge indexing.",
                code="azure_search_not_configured",
            )

    async def ensure_index(self) -> None:
        client = SearchIndexClient(
            endpoint=self._settings.azure_search_endpoint,
            credential=self._credential(),
        )
        async with client:
            await client.create_or_update_index(build_knowledge_index(self._settings))

    async def index_chunks(self, chunks: list[KnowledgeChunk]) -> int:
        if not chunks:
            return 0

        client = self._search_client()
        documents = [self._to_search_document(chunk) for chunk in chunks]
        async with client:
            results = await client.upload_documents(documents=documents)

        failed = [result for result in results if not result.succeeded]
        if failed:
            raise DependencyUnavailableError(
                "Azure AI Search rejected one or more chunks.",
                code="azure_search_indexing_failed",
                details={"failed_keys": [result.key for result in failed]},
            )

        return len(results)

    async def search(
        self,
        *,
        query: str,
        query_vector: list[float],
        tenant_id: str,
        mode: RetrievalMode,
        top_k: int,
        filters: dict[str, object],
    ) -> list[SearchResult]:
        vector_query = VectorizedQuery(
            vector=query_vector,
            k_nearest_neighbors=top_k,
            fields="content_vector",
        )
        filter_expression = self._build_filter_expression(tenant_id=tenant_id, filters=filters)
        kwargs: dict[str, Any] = {
            "top": top_k,
            "select": [
                "id",
                "document_id",
                "content",
                "metadata_json",
                "file_name",
                "source_uri",
                "ordinal",
            ],
            "filter": filter_expression,
            "include_total_count": False,
        }

        if mode == RetrievalMode.VECTOR:
            kwargs["vector_queries"] = [vector_query]
        elif mode == RetrievalMode.HYBRID:
            kwargs["search_text"] = query
            kwargs["vector_queries"] = [vector_query]
        else:
            kwargs["search_text"] = query
            kwargs["vector_queries"] = [vector_query]
            kwargs["query_type"] = "semantic"
            kwargs["semantic_configuration_name"] = self._settings.rag_semantic_configuration_name
            kwargs["query_caption"] = "extractive"

        client = self._search_client()
        results: list[SearchResult] = []
        async with client:
            async for row in await client.search(**kwargs):
                metadata = self._load_metadata(row.get("metadata_json"))
                results.append(
                    SearchResult(
                        chunk_id=row["id"],
                        document_id=row["document_id"],
                        content=row["content"],
                        score=row.get("@search.score"),
                        reranker_score=row.get("@search.reranker_score"),
                        metadata=metadata,
                    )
                )
        return results

    def _search_client(self) -> SearchClient:
        return SearchClient(
            endpoint=self._settings.azure_search_endpoint,
            index_name=self._settings.resolved_rag_index_name,
            credential=self._credential(),
        )

    def _credential(self) -> AzureKeyCredential | DefaultAzureCredential:
        if self._settings.azure_search_api_key and self._settings.azure_search_api_key.get_secret_value():
            return AzureKeyCredential(self._settings.azure_search_api_key.get_secret_value())
        return DefaultAzureCredential()

    def _to_search_document(self, chunk: KnowledgeChunk) -> dict[str, object]:
        metadata = dict(chunk.metadata)
        return {
            "id": chunk.id,
            "tenant_id": chunk.tenant_id,
            "document_id": chunk.document_id,
            "source_id": chunk.source_id,
            "project_id": chunk.project_id,
            "architecture_version_id": chunk.architecture_version_id,
            "content": chunk.content,
            "content_vector": chunk.content_vector,
            "content_hash": chunk.content_hash,
            "ordinal": chunk.ordinal,
            "token_estimate": chunk.token_estimate,
            "file_name": metadata.get("file_name"),
            "source_uri": metadata.get("source_uri"),
            "document_type": metadata.get("document_type"),
            "sensitivity_label": metadata.get("sensitivity_label"),
            "pillars": metadata.get("pillars", []),
            "azure_services": metadata.get("azure_services", []),
            "ingested_at": metadata.get("ingested_at"),
            "metadata_json": json.dumps(metadata, default=str, separators=(",", ":")),
        }

    def _build_filter_expression(self, *, tenant_id: str, filters: dict[str, object]) -> str:
        expressions = [f"tenant_id eq '{self._escape(tenant_id)}'"]
        for field in [
            "project_id",
            "architecture_version_id",
            "document_type",
            "sensitivity_label",
        ]:
            value = filters.get(field)
            if isinstance(value, str) and value:
                expressions.append(f"{field} eq '{self._escape(value)}'")

        for field in ["pillars", "azure_services"]:
            values = filters.get(field)
            if isinstance(values, list) and values:
                collection_filters = [
                    f"{field}/any(item: item eq '{self._escape(str(value))}')"
                    for value in values
                    if value
                ]
                if collection_filters:
                    expressions.append("(" + " or ".join(collection_filters) + ")")

        return " and ".join(expressions)

    @staticmethod
    def _escape(value: str) -> str:
        return value.replace("'", "''")

    @staticmethod
    def _load_metadata(value: object) -> dict[str, object]:
        if isinstance(value, str) and value:
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                return {}
            if isinstance(parsed, dict):
                return parsed
        return {}
