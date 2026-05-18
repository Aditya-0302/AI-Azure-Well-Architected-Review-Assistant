from __future__ import annotations

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureOpenAIEmbeddings

from app.core.config import Settings
from app.core.exceptions import DependencyUnavailableError


class LangChainAzureOpenAIEmbeddingProvider:
    def __init__(self, settings: Settings) -> None:
        if not settings.azure_openai_endpoint:
            raise DependencyUnavailableError(
                "AZURE_OPENAI_ENDPOINT is required for embeddings.",
                code="azure_openai_not_configured",
            )

        kwargs: dict[str, object] = {
            "azure_endpoint": settings.azure_openai_endpoint,
            "azure_deployment": settings.azure_openai_embedding_deployment,
            "api_version": settings.azure_openai_api_version,
            "model": settings.azure_openai_embedding_deployment,
            "chunk_size": 32,
            "max_retries": 4,
        }

        if settings.azure_openai_api_key and settings.azure_openai_api_key.get_secret_value():
            kwargs["api_key"] = settings.azure_openai_api_key.get_secret_value()
        else:
            kwargs["azure_ad_token_provider"] = get_bearer_token_provider(
                DefaultAzureCredential(),
                "https://cognitiveservices.azure.com/.default",
            )

        self._embeddings = AzureOpenAIEmbeddings(**kwargs)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return await self._embeddings.aembed_documents(texts)

    async def embed_query(self, text: str) -> list[float]:
        return await self._embeddings.aembed_query(text)
