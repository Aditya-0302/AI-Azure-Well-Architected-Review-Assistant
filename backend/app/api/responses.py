from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiEnvelope(BaseModel, Generic[T]):
    data: T
    meta: dict[str, object] = Field(default_factory=dict)


class PageMeta(BaseModel):
    limit: int
    offset: int
    total: int | None = None


class PagedEnvelope(BaseModel, Generic[T]):
    data: list[T]
    meta: PageMeta

