"""Frozen LangGraph workflow state contract matching shared/api-contract.md §4.7."""
from __future__ import annotations

from typing import Any, TypedDict


class YojanaWorkflowState(TypedDict):
    """The frozen 11-key internal workflow state for Yojana Mitra.

    Strictly conforms to shared/api-contract.md §4.7. No additional keys may be added.
    """

    session_id: str
    language: str
    input_type: str
    user_text: str
    intent: str
    scheme_id: str | None
    eligibility_answers: dict[str, Any]
    retrieved_evidence: list[dict[str, Any]]
    assessment: dict[str, Any] | None
    response: dict[str, Any]
    error: dict[str, Any] | None

