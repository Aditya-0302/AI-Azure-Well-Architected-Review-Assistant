from __future__ import annotations

from pathlib import PurePosixPath
from uuid import uuid4

from app.application.dto.knowledge import (
    BlobIngestionRequest,
    IngestionChunkResponse,
    IngestionResponse,
)
from app.application.ports.rag import BlobDocumentLoader, EmbeddingProvider, KnowledgeIndex
from app.application.services.authorization_service import AuthorizationService
from app.core.config import Settings
from app.core.security import Principal
from app.domain.common.context import TenantContext
from app.rag.chunking.langchain_chunker import LangChainChunker
from app.rag.extraction.text_extractor import DocumentTextExtractor
from app.rag.metadata.tagger import MetadataTagger


class RagIngestionService:
    def __init__(
        self,
        *,
        settings: Settings,
        blob_loader: BlobDocumentLoader,
        embedding_provider: EmbeddingProvider,
        knowledge_index: KnowledgeIndex,
        authorization: AuthorizationService,
        extractor: DocumentTextExtractor,
        metadata_tagger: MetadataTagger,
        chunker: LangChainChunker,
    ) -> None:
        self._settings = settings
        self._blob_loader = blob_loader
        self._embedding_provider = embedding_provider
        self._knowledge_index = knowledge_index
        self._authorization = authorization
        self._extractor = extractor
        self._metadata_tagger = metadata_tagger
        self._chunker = chunker

    async def ingest_blob(
        self,
        request: BlobIngestionRequest,
        principal: Principal,
        tenant: TenantContext,
    ) -> IngestionResponse:
        self._authorization.require_project_write(principal)

        ingestion_id = str(uuid4())
        document_id = request.document_id or str(uuid4())
        container_name = request.container_name or self._settings.azure_storage_container_raw
        file_name = request.file_name or PurePosixPath(request.blob_name).name
        source_uri = request.source_uri or f"azure-blob://{container_name}/{request.blob_name}"

        blob_document = await self._blob_loader.load_blob(
            container_name=container_name,
            blob_name=request.blob_name,
            content_type=request.content_type,
        )
        extracted = await self._extractor.extract(blob_document, file_name=file_name)
        document_metadata = self._metadata_tagger.build_document_metadata(
            tenant_id=tenant.tenant_id,
            blob_name=request.blob_name,
            file_name=file_name,
            content_type=blob_document.content_type,
            document_type=request.document_type,
            sensitivity_label=request.sensitivity_label,
            source_uri=source_uri,
            project_id=request.project_id,
            architecture_version_id=request.architecture_version_id,
            extra_metadata={
                **blob_document.metadata,
                **request.extra_metadata,
                "ingestion_id": ingestion_id,
                "parser": extracted.parser,
            },
            text=extracted.text,
        )

        chunks = self._chunker.chunk(
            extracted=extracted,
            tenant_id=tenant.tenant_id,
            document_id=document_id,
            source_id=request.source_id,
            project_id=request.project_id,
            architecture_version_id=request.architecture_version_id,
            base_metadata=document_metadata,
        )
        if chunks:
            embeddings = await self._embedding_provider.embed_documents([chunk.content for chunk in chunks])
            for chunk, vector in zip(chunks, embeddings, strict=True):
                chunk.content_vector = vector

        await self._knowledge_index.ensure_index()
        indexed_count = await self._knowledge_index.index_chunks(chunks)

        return IngestionResponse(
            ingestion_id=ingestion_id,
            index_name=self._settings.resolved_rag_index_name,
            document_id=document_id,
            chunk_count=len(chunks),
            indexed_count=indexed_count,
            metadata=document_metadata,
            chunks=[
                IngestionChunkResponse(
                    chunk_id=chunk.id,
                    ordinal=chunk.ordinal,
                    token_estimate=chunk.token_estimate,
                    content_hash=chunk.content_hash,
                )
                for chunk in chunks
            ],
        )

