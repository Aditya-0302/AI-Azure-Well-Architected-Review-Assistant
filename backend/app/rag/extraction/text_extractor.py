from __future__ import annotations

from io import BytesIO
from pathlib import PurePosixPath

from pypdf import PdfReader

from app.core.exceptions import AppError
from app.rag.models import BlobDocument, ExtractedDocument


class DocumentExtractionError(AppError):
    status_code = 422
    code = "document_extraction_failed"
    message = "The document could not be extracted."


class DocumentTextExtractor:
    TEXT_CONTENT_TYPES = {
        "text/plain",
        "text/markdown",
        "text/csv",
        "application/json",
        "application/xml",
        "text/xml",
    }

    async def extract(self, document: BlobDocument, *, file_name: str | None = None) -> ExtractedDocument:
        name = file_name or PurePosixPath(document.blob_name).name
        content_type = (document.content_type or "").split(";")[0].lower()
        extension = PurePosixPath(name).suffix.lower()

        if content_type == "application/pdf" or extension == ".pdf":
            return self._extract_pdf(document)

        if content_type in self.TEXT_CONTENT_TYPES or extension in {
            ".txt",
            ".md",
            ".markdown",
            ".csv",
            ".json",
            ".xml",
            ".yaml",
            ".yml",
            ".bicep",
            ".tf",
        }:
            return ExtractedDocument(
                text=self._decode_text(document.content),
                parser="utf8_text",
                metadata={"file_extension": extension.lstrip(".")},
            )

        try:
            text = self._decode_text(document.content)
        except UnicodeDecodeError as exc:
            raise DocumentExtractionError(
                "Unsupported binary document. Route Office files and diagrams through the document "
                "intelligence pipeline before RAG indexing.",
                details={"blob_name": document.blob_name, "content_type": content_type},
            ) from exc

        return ExtractedDocument(
            text=text,
            parser="utf8_fallback",
            metadata={"file_extension": extension.lstrip(".")},
        )

    def _extract_pdf(self, document: BlobDocument) -> ExtractedDocument:
        try:
            reader = PdfReader(BytesIO(document.content))
            pages = [page.extract_text() or "" for page in reader.pages]
        except Exception as exc:
            raise DocumentExtractionError(
                "PDF extraction failed.",
                details={"blob_name": document.blob_name},
            ) from exc

        return ExtractedDocument(
            text="\n\n".join(page.strip() for page in pages if page.strip()),
            page_count=len(reader.pages),
            parser="pypdf",
            metadata={"file_extension": "pdf"},
        )

    @staticmethod
    def _decode_text(content: bytes) -> str:
        if content.startswith(b"\xef\xbb\xbf"):
            content = content[3:]
        return content.decode("utf-8")

