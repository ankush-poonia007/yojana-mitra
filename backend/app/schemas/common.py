"""Shared sub-schemas for speech, assessment, card, sources, and transcription."""
from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class SpeechPayload(BaseModel):
    """Audio speech payload preserving Base64 delivery."""

    status: str
    content_type: str
    audio_base64: str


class AnswerPayload(BaseModel):
    """Assistant textual answer payload."""

    text: str


class TranscriptionPayload(BaseModel):
    """Speech-to-text transcription result."""

    text: str
    confidence: float | None = None


class AssessmentPayload(BaseModel):
    """Deterministic eligibility assessment structure."""

    scheme_id: str
    result: str
    reasons: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)


class CardPayload(BaseModel):
    """Take-away action card structure."""

    scheme_name: str
    documents: list[str] = Field(default_factory=list)
    where_to_apply: list[str] = Field(default_factory=list)
    disclaimer: str


class SourceReference(BaseModel):
    """Grounded source document reference."""

    document_id: str
    title: str
    url: str | None = None
    page: int | None = None
    section: str | None = None

