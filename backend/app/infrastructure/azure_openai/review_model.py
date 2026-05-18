from __future__ import annotations

import json
from typing import TypeVar

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import APIError, AsyncAzureOpenAI
from pydantic import BaseModel, ValidationError

from app.application.ports.review_model import StructuredReviewModel
from app.core.config import Settings
from app.core.exceptions import DependencyUnavailableError
from app.review_engine.schemas.json_schema import openai_json_schema

ModelT = TypeVar("ModelT", bound=BaseModel)


class AzureOpenAIStructuredReviewModel(StructuredReviewModel):
    def __init__(self, settings: Settings) -> None:
        if not settings.azure_openai_endpoint:
            raise DependencyUnavailableError(
                "AZURE_OPENAI_ENDPOINT is required for the AI review engine.",
                code="azure_openai_not_configured",
            )

        client_kwargs: dict[str, object] = {
            "azure_endpoint": settings.azure_openai_endpoint,
            "api_version": settings.azure_openai_api_version,
        }
        if settings.azure_openai_api_key and settings.azure_openai_api_key.get_secret_value():
            client_kwargs["api_key"] = settings.azure_openai_api_key.get_secret_value()
        else:
            client_kwargs["azure_ad_token_provider"] = get_bearer_token_provider(
                DefaultAzureCredential(),
                "https://cognitiveservices.azure.com/.default",
            )

        self._client = AsyncAzureOpenAI(**client_kwargs)
        self._deployment = settings.azure_openai_chat_deployment

    async def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[ModelT],
        schema_name: str,
        temperature: float = 0.1,
    ) -> ModelT:
        try:
            response = await self._client.chat.completions.create(
                model=self._deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                response_format=openai_json_schema(response_model, name=schema_name),
            )
        except APIError as exc:
            raise DependencyUnavailableError(
                "Azure OpenAI review model call failed.",
                code="azure_openai_review_call_failed",
                details={"schema_name": schema_name},
            ) from exc

        content = response.choices[0].message.content
        if not isinstance(content, str) or not content.strip():
            raise DependencyUnavailableError(
                "Azure OpenAI returned an empty structured review response.",
                code="azure_openai_empty_review_response",
                details={"schema_name": schema_name},
            )

        try:
            return response_model.model_validate_json(content)
        except ValidationError as exc:
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError:
                parsed = {"raw_content": content[:2000]}
            raise DependencyUnavailableError(
                "Azure OpenAI response did not match the expected review schema.",
                code="azure_openai_review_schema_validation_failed",
                details={"schema_name": schema_name, "response": parsed},
            ) from exc

