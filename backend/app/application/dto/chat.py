from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ChatSessionCreateRequest(BaseModel):
    project_id: str | None = None
    review_id: str | None = None
    title: str | None = Field(default=None, max_length=200)


class ChatSessionResponse(BaseModel):
    id: str
    project_id: str | None
    review_id: str | None
    title: str
    created_at: datetime


class ChatMessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=16000)


class ChatMessageResponse(BaseModel):
    session_id: str
    message_id: str
    role: str
    content: str
    citations: list[dict[str, str]]
    created_at: datetime

