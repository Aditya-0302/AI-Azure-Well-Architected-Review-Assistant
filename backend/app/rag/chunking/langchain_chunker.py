from __future__ import annotations

from hashlib import sha256
from uuid import uuid5, NAMESPACE_URL

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import Settings
from app.rag.models import ExtractedDocument, KnowledgeChunk


class LangChainChunker:
    def __init__(self, settings: Settings) -> None:
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.rag_chunk_size,
            chunk_overlap=settings.rag_chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def chunk(
        self,
        *,
        extracted: ExtractedDocument,
        tenant_id: str,
        document_id: str,
        source_id: str | None,
        project_id: str | None,
        architecture_version_id: str | None,
        base_metadata: dict[str, object],
    ) -> list[KnowledgeChunk]:
        source_document = Document(page_content=extracted.text, metadata=base_metadata)
        documents = self._splitter.split_documents([source_document])
        chunks: list[KnowledgeChunk] = []

        for ordinal, document in enumerate(documents):
            content = document.page_content.strip()
            if not content:
                continue
            content_hash = sha256(content.encode("utf-8")).hexdigest()
            chunk_id = str(uuid5(NAMESPACE_URL, f"{tenant_id}:{document_id}:{ordinal}:{content_hash}"))
            metadata = {
                **document.metadata,
                "chunk_id": chunk_id,
                "chunk_ordinal": ordinal,
                "content_hash": content_hash,
            }
            chunks.append(
                KnowledgeChunk(
                    id=chunk_id,
                    tenant_id=tenant_id,
                    document_id=document_id,
                    source_id=source_id,
                    project_id=project_id,
                    architecture_version_id=architecture_version_id,
                    ordinal=ordinal,
                    content=content,
                    content_hash=content_hash,
                    token_estimate=max(1, len(content) // 4),
                    metadata=metadata,
                )
            )

        return chunks

