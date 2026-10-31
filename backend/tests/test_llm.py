"""Unit tests for the centralized Gemini LLM client and model routing."""
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.config import settings
from app.llm.client import GeminiClient
from app.llm.exceptions import (
    LLMConfigurationError,
    LLMFormattingError,
    LLMProviderError,
    LLMQuotaExceededError,
)
from app.llm.models import ModelTier


@pytest.mark.asyncio
async def test_gemini_client_missing_key_raises_configuration_error():
    """Verify LLMConfigurationError is raised when GEMINI_API_KEY is missing."""
    client = GeminiClient()
    with patch.object(settings, "gemini_api_key", ""):
        with pytest.raises(LLMConfigurationError, match="GEMINI_API_KEY is not configured"):
            await client.generate(ModelTier.LITE, "Test prompt")


def test_gemini_model_tier_resolution_defaults():
    """Verify tier routing resolves to approved configuration defaults."""
    client = GeminiClient()
    assert client.get_model_id(ModelTier.HIGH) == "gemini-3.8-flash"
    assert client.get_model_id(ModelTier.MID) == "gemini-3.6-flash"
    assert client.get_model_id(ModelTier.LITE) == "gemini-3.5-flash-lite"


def test_gemini_model_tier_resolution_override():
    """Verify tier routing respects settings overrides without hardcoded fallback."""
    client = GeminiClient()
    with patch.object(settings, "gemini_model_high", "custom-high-model"), \
         patch.object(settings, "gemini_model_mid", "custom-mid-model"), \
         patch.object(settings, "gemini_model_lite", "custom-lite-model"):
        assert client.get_model_id(ModelTier.HIGH) == "custom-high-model"
        assert client.get_model_id(ModelTier.MID) == "custom-mid-model"
        assert client.get_model_id(ModelTier.LITE) == "custom-lite-model"


def test_gemini_model_tier_unconfigured_raises():
    """Verify error when a model tier is set to an empty string."""
    client = GeminiClient()
    with patch.object(settings, "gemini_model_high", ""):
        with pytest.raises(LLMConfigurationError, match="Model identifier for tier 'high' is not configured"):
            client.get_model_id(ModelTier.HIGH)


@pytest.mark.asyncio
async def test_gemini_generate_text_success():
    """Verify generate text calls SDK correctly and returns response text."""
    mock_sdk = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "नमस्ते! मैं आपकी क्या सहायता कर सकता हूँ?"
    mock_sdk.aio.models.generate_content = AsyncMock(return_value=mock_response)

    client = GeminiClient(client=mock_sdk)
    with patch.object(settings, "gemini_model_mid", "gemini-3.6-flash"):
        result = await client.generate(
            tier=ModelTier.MID,
            prompt="Hello",
            system_instruction="Be helpful",
            temperature=0.3,
        )

    assert result == "नमस्ते! मैं आपकी क्या सहायता कर सकता हूँ?"
    mock_sdk.aio.models.generate_content.assert_awaited_once_with(
        model="gemini-3.6-flash",
        contents="Hello",
        config={"temperature": 0.3, "system_instruction": "Be helpful"},
    )


@pytest.mark.asyncio
async def test_gemini_generate_json_success():
    """Verify generate_json cleanly parses valid JSON response."""
    mock_sdk = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"scheme_id": "pmuy", "is_eligible": true}'
    mock_sdk.aio.models.generate_content = AsyncMock(return_value=mock_response)

    client = GeminiClient(client=mock_sdk)
    result = await client.generate_json(tier=ModelTier.LITE, prompt="Evaluate")
    assert result == {"scheme_id": "pmuy", "is_eligible": True}


@pytest.mark.asyncio
async def test_gemini_generate_json_markdown_fences_stripped():
    """Verify markdown fences (```json ... ```) are cleanly stripped and parsed."""
    mock_sdk = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '```json\n{"intent": "scheme_query", "scheme": "pmuy"}\n```'
    mock_sdk.aio.models.generate_content = AsyncMock(return_value=mock_response)

    client = GeminiClient(client=mock_sdk)
    result = await client.generate_json(tier=ModelTier.LITE, prompt="Classify")
    assert result == {"intent": "scheme_query", "scheme": "pmuy"}


@pytest.mark.asyncio
async def test_gemini_generate_json_invalid_syntax_raises():
    """Verify LLMFormattingError is raised when response is unparseable JSON."""
    mock_sdk = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is not JSON: {invalid"
    mock_sdk.aio.models.generate_content = AsyncMock(return_value=mock_response)

    client = GeminiClient(client=mock_sdk)
    with pytest.raises(LLMFormattingError, match="could not be parsed as valid JSON"):
        await client.generate_json(tier=ModelTier.LITE, prompt="Classify")


@pytest.mark.asyncio
async def test_gemini_generate_timeout_error_handling():
    """Verify asyncio.TimeoutError maps to LLMProviderError."""
    mock_sdk = MagicMock()
    mock_sdk.aio.models.generate_content = AsyncMock(side_effect=asyncio.TimeoutError)

    client = GeminiClient(client=mock_sdk)
    with pytest.raises(LLMProviderError, match="timed out"):
        await client.generate(ModelTier.HIGH, "Slow query")


@pytest.mark.asyncio
async def test_gemini_generate_quota_exceeded_error_handling():
    """Verify 429 / quota exceeded error maps to LLMQuotaExceededError."""
    mock_sdk = MagicMock()
    mock_sdk.aio.models.generate_content = AsyncMock(
        side_effect=Exception("429 Resource has been exhausted (e.g. check quota).")
    )

    client = GeminiClient(client=mock_sdk)
    with pytest.raises(LLMQuotaExceededError, match="rate limit or quota exceeded"):
        await client.generate(ModelTier.MID, "High volume prompt")


@pytest.mark.asyncio
async def test_gemini_generate_generic_provider_error_handling():
    """Verify unexpected provider exceptions map to LLMProviderError without leaking internals."""
    mock_sdk = MagicMock()
    mock_sdk.aio.models.generate_content = AsyncMock(
        side_effect=RuntimeError("Internal Google server RPC failure details")
    )

    client = GeminiClient(client=mock_sdk)
    with pytest.raises(LLMProviderError, match="Gemini provider error occurred"):
        await client.generate(ModelTier.MID, "Prompt")
