"""Turn request and response schemas."""
from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field

from app.schemas.common import (
    AnswerPayload,
    AssessmentPayload,
    CardPayload,
    SourceReference,
    SpeechPayload,
    TranscriptionPayload,
)


class TextTurn(BaseModel):
    """Input payload for a text conversation turn."""

    session_id: str
    text: str


class TurnResponse(BaseModel):
    """Standard turn response structure matching Phase 3.3."""

    session_id: str
    turn_id: str
    status: str
    language: str
    answer: AnswerPayload
    transcription: TranscriptionPayload | None = None
    assessment: AssessmentPayload | None = None
    card: CardPayload | None = None
    sources: list[SourceReference] = Field(default_factory=list)
    speech: SpeechPayload

