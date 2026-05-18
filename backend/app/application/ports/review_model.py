from __future__ import annotations

from typing import Protocol, TypeVar

from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class StructuredReviewModel(Protocol):
    async def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[ModelT],
        schema_name: str,
        temperature: float = 0.1,
    ) -> ModelT:
        """Call a chat model and validate the JSON response against a Pydantic schema."""

