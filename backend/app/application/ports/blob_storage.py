from __future__ import annotations

from datetime import datetime
from typing import Protocol

from pydantic import BaseModel


class UploadUrl(BaseModel):
    url: str
    expires_at: datetime
    required_headers: dict[str, str]


class BlobStoragePort(Protocol):
    async def create_upload_url(
        self,
        *,
        tenant_id: str,
        blob_path: str,
        content_type: str,
        size_bytes: int,
    ) -> UploadUrl:
        """Create a short-lived direct upload URL."""

