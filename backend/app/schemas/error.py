"""Standard error envelope Pydantic schema."""
from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Detailed error object matching Phase 3.3 specification."""

    code: str
    message: str
    retryable: bool = False
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorEnvelope(BaseModel):
    """Top-level error response envelope."""

    error: ErrorDetail

