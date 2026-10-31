"""Domain exceptions for centralized LLM client and provider interactions."""
from __future__ import annotations


class LLMServiceError(Exception):
    """Base exception for all LLM service failures."""


class LLMConfigurationError(LLMServiceError):
    """Raised when required credentials or model tier configurations are missing."""


class LLMProviderError(LLMServiceError):
    """Raised when the downstream provider encounters network errors or outages."""


class LLMQuotaExceededError(LLMProviderError):
    """Raised when the provider reports quota exhaustion / rate limiting (HTTP 429)."""


class LLMFormattingError(LLMServiceError):
    """Raised when provider output cannot be parsed into the expected structured schema."""

