from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class BlobDocument(BaseModel):
    container_name: str
    blob_name: str
    content: bytes
    content_type: str | None = None
    size_bytes: int | None = None
    etag: str | None = None
    last_modified: datetime | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class ExtractedDocument(BaseModel):
    text: str
    page_count: int | None = None
    parser: str
    metadata: dict[str, object] = Field(default_factory=dict)


class KnowledgeChunk(BaseModel):
    id: str
    tenant_id: str
    document_id: str
    source_id: str | None = None
    project_id: str | None = None
    architecture_version_id: str | None = None
    ordinal: int
    content: str
    content_hash: str
    token_estimate: int
    content_vector: list[float] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    score: float | None = None
    reranker_score: float | None = None
    metadata: dict[str, object] = Field(default_factory=dict)

