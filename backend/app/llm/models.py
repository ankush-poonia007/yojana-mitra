"""Model tier enumeration and data structures for centralized Gemini routing."""
from __future__ import annotations

from enum import Enum


class ModelTier(str, Enum):
    """The three approved Gemini model tiers per Phase 3.2 §3.1."""

    HIGH = "high"  # Supervisor, complex verification
    MID = "mid"    # Scheme knowledge, conversational reasoning
    LITE = "lite"  # Intent detection, scheme identification, response formatting

