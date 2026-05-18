from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.application.dto.uploads import UploadInitiateRequest, UploadInitiateResponse
from app.application.dto.uploads import UploadCompleteRequest, UploadStatusResponse
from app.application.ports.blob_storage import BlobStoragePort
from app.application.services.authorization_service import AuthorizationService
from app.core.exceptions import DependencyUnavailableError
from app.core.security import Principal
from app.domain.common.context import TenantContext


class UploadService:
    def __init__(self, blob_storage: BlobStoragePort, authorization: AuthorizationService) -> None:
        self._blob_storage = blob_storage
        self._authorization = authorization

    async def initiate_upload(
        self,
        request: UploadInitiateRequest,
        principal: Principal,
        tenant: TenantContext,
    ) -> UploadInitiateResponse:
        self._authorization.require_project_write(principal)
        upload_id = str(uuid4())
        blob_path = (
            f"tenants/{tenant.tenant_id}/projects/{request.project_id}/uploads/"
            f"{upload_id}/{request.file_name}"
        )
        upload_url = await self._blob_storage.create_upload_url(
            tenant_id=tenant.tenant_id,
            blob_path=blob_path,
            content_type=request.content_type,
            size_bytes=request.size_bytes,
        )
        return UploadInitiateResponse(
            upload_id=upload_id,
            upload_url=upload_url.url,
            expires_at=upload_url.expires_at,
            required_headers=upload_url.required_headers,
        )

    async def complete_upload(
        self,
        request: UploadCompleteRequest,
        principal: Principal,
        tenant: TenantContext,
    ) -> UploadStatusResponse:
        self._authorization.require_project_write(principal)
        raise DependencyUnavailableError(
            "Upload completion requires Blob verification and ingestion queue adapters.",
            code="upload_completion_not_configured",
            details={"upload_id": request.upload_id, "tenant_id": tenant.tenant_id},
        )


class LocalDevelopmentBlobStorage:
    async def create_upload_url(
        self,
        *,
        tenant_id: str,
        blob_path: str,
        content_type: str,
        size_bytes: int,
    ):
        from app.application.ports.blob_storage import UploadUrl

        return UploadUrl(
            url=f"http://localhost:10000/devstoreaccount1/{blob_path}",
            expires_at=datetime.now(UTC) + timedelta(minutes=15),
            required_headers={
                "x-ms-blob-type": "BlockBlob",
                "content-type": content_type,
                "x-ms-meta-tenant-id": tenant_id,
                "x-ms-meta-size-bytes": str(size_bytes),
            },
        )
