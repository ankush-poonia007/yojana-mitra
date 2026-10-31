"""Boundary adapters package for external seams (Rules, Retrieval, Speech)."""
from __future__ import annotations

from app.adapters.eligibility import EligibilityAdapter, eligibility_adapter
from app.adapters.retrieval import RetrievalAdapter, RetrievalServiceError, retrieval_adapter
from app.adapters.speech import STTUnavailableError, SpeechAdapter, speech_adapter

__all__ = [
    "EligibilityAdapter",
    "eligibility_adapter",
    "RetrievalAdapter",
    "retrieval_adapter",
    "RetrievalServiceError",
    "SpeechAdapter",
    "speech_adapter",
    "STTUnavailableError",
]

