"""Session creation and retrieval schemas."""
from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Payload to create a new session."""

    language: Literal["hi", "en"]
    mode: Literal["voice", "text", "combined"]


class SessionCreateResponse(BaseModel):
    """Response returned upon session creation."""

    session_id: str
    status: str
    language: Literal["hi", "en"]
    mode: Literal["voice", "text", "combined"]
    created_at: str


class TurnHistoryItem(BaseModel):
    """Historical conversation turn item."""

    turn_id: str
    role: Literal["user", "assistant"]
    text: str
    created_at: str | None = None


class SessionGetResponse(BaseModel):
    """Session details and turn history response."""

    session_id: str
    status: str
    language: Literal["hi", "en"]
    mode: Literal["voice", "text", "combined"]
    turns: list[TurnHistoryItem] = Field(default_factory=list)

