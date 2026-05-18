from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class RetrievalMode(StrEnum):
    VECTOR = "vector"
    HYBRID = "hybrid"
    SEMANTIC_HYBRID = "semantic_hybrid"


class BlobIngestionRequest(BaseModel):
    container_name: str | None = None
    blob_name: str = Field(min_length=1, max_length=2048)
    project_id: str | None = Field(default=None, max_length=128)
    architecture_version_id: str | None = Field(default=None, max_length=128)
    source_id: str | None = Field(default=None, max_length=128)
    document_id: str | None = Field(default=None, max_length=128)
    file_name: str | None = Field(default=None, max_length=512)
    content_type: str | None = Field(default=None, max_length=256)
    source_uri: str | None = Field(default=None, max_length=2048)
    document_type: str = Field(default="architecture_evidence", max_length=128)
    sensitivity_label: str = Field(default="internal", max_length=128)
    extra_metadata: dict[str, str] = Field(default_factory=dict)


class IngestionChunkResponse(BaseModel):
    chunk_id: str
    ordinal: int
    token_estimate: int
    content_hash: str


class IngestionResponse(BaseModel):
    ingestion_id: str
    index_name: str
    document_id: str
    chunk_count: int
    indexed_count: int
    metadata: dict[str, object]
    chunks: list[IngestionChunkResponse]


class RetrievalRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000)
    project_id: str | None = None
    architecture_version_id: str | None = None
    pillars: list[str] = Field(default_factory=list)
    azure_services: list[str] = Field(default_factory=list)
    document_type: str | None = None
    sensitivity_label: str | None = None
    mode: RetrievalMode = RetrievalMode.SEMANTIC_HYBRID
    top_k: int = Field(default=8, ge=1, le=50)


class RetrievalCitation(BaseModel):
    document_id: str
    chunk_id: str
    source_uri: str | None = None
    file_name: str | None = None
    page_number: int | None = None


class RetrievalResult(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    score: float | None = None
    reranker_score: float | None = None
    metadata: dict[str, object]
    citation: RetrievalCitation


class RetrievalResponse(BaseModel):
    query: str
    mode: RetrievalMode
    index_name: str
    results: list[RetrievalResult]

