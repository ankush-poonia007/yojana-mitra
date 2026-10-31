"""Prompts package for Yojana Mitra LLM interactions."""
from __future__ import annotations

from app.llm.prompts.intent_scheme import (
    INTENT_SCHEME_SYSTEM_INSTRUCTION,
    INTENT_SCHEME_USER_PROMPT_TEMPLATE,
)
from app.llm.prompts.response_formatting import (
    RESPONSE_FORMATTING_SYSTEM_INSTRUCTION,
    RESPONSE_FORMATTING_USER_PROMPT_TEMPLATE,
)

__all__ = [
    "INTENT_SCHEME_SYSTEM_INSTRUCTION",
    "INTENT_SCHEME_USER_PROMPT_TEMPLATE",
    "RESPONSE_FORMATTING_SYSTEM_INSTRUCTION",
    "RESPONSE_FORMATTING_USER_PROMPT_TEMPLATE",
]

