from __future__ import annotations

from typing import Protocol

from app.application.dto.knowledge import RetrievalMode
from app.rag.models import BlobDocument, KnowledgeChunk, SearchResult


class BlobDocumentLoader(Protocol):
    async def load_blob(
        self,
        *,
        container_name: str,
        blob_name: str,
        content_type: str | None = None,
    ) -> BlobDocument:
        """Load a document from blob storage."""


class EmbeddingProvider(Protocol):
    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed document chunks."""

    async def embed_query(self, text: str) -> list[float]:
        """Embed a retrieval query."""


class KnowledgeIndex(Protocol):
    async def ensure_index(self) -> None:
        """Create or update the knowledge index."""

    async def index_chunks(self, chunks: list[KnowledgeChunk]) -> int:
        """Index embedded chunks."""

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
        """Retrieve chunks from Azure AI Search."""

