from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class UploadInitiateRequest(BaseModel):
    project_id: str
    file_name: str = Field(min_length=1, max_length=512)
    content_type: str = Field(min_length=3, max_length=256)
    size_bytes: int = Field(gt=0, le=250 * 1024 * 1024)
    checksum_sha256: str | None = Field(default=None, min_length=64, max_length=64)
    asset_type: str = Field(default="architecture_document", max_length=100)


class UploadInitiateResponse(BaseModel):
    upload_id: str
    upload_url: str
    expires_at: datetime
    required_headers: dict[str, str]


class UploadCompleteRequest(BaseModel):
    upload_id: str
    checksum_sha256: str = Field(min_length=64, max_length=64)


class UploadStatusResponse(BaseModel):
    upload_id: str
    status: str
    ingestion_job_id: str | None = None

