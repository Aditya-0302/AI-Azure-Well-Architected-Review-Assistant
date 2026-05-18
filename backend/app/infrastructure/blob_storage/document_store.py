from __future__ import annotations

from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

from app.core.config import Settings
from app.core.exceptions import DependencyUnavailableError
from app.rag.models import BlobDocument


class AzureBlobDocumentStore:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def load_blob(
        self,
        *,
        container_name: str,
        blob_name: str,
        content_type: str | None = None,
    ) -> BlobDocument:
        service_client = self._create_service_client()
        async with service_client:
            blob_client = service_client.get_blob_client(container=container_name, blob=blob_name)
            properties = await blob_client.get_blob_properties()
            downloader = await blob_client.download_blob()
            content = await downloader.readall()

        return BlobDocument(
            container_name=container_name,
            blob_name=blob_name,
            content=content,
            content_type=content_type or properties.content_settings.content_type,
            size_bytes=properties.size,
            etag=properties.etag,
            last_modified=properties.last_modified,
            metadata=dict(properties.metadata or {}),
        )

    def _create_service_client(self) -> BlobServiceClient:
        if (
            self._settings.azure_storage_connection_string
            and self._settings.azure_storage_connection_string.get_secret_value()
        ):
            return BlobServiceClient.from_connection_string(
                self._settings.azure_storage_connection_string.get_secret_value()
            )
        if not self._settings.azure_storage_account_url:
            raise DependencyUnavailableError(
                "AZURE_STORAGE_ACCOUNT_URL or AZURE_STORAGE_CONNECTION_STRING is required.",
                code="blob_storage_not_configured",
            )
        return BlobServiceClient(
            account_url=self._settings.azure_storage_account_url,
            credential=DefaultAzureCredential(),
        )
