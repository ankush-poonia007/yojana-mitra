"""Centralized Google GenAI / Gemini client with three-tier model routing."""
from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any

from app.core.config import settings
from app.llm.exceptions import (
    LLMConfigurationError,
    LLMFormattingError,
    LLMProviderError,
    LLMQuotaExceededError,
)
from app.llm.models import ModelTier

logger = logging.getLogger(__name__)


class GeminiClient:
    """Centralized client for all Gemini model interactions."""

    def __init__(self, client: Any | None = None) -> None:
        self._client = client

    def _get_sdk_client(self) -> Any:
        """Lazily initialize Google GenAI Client using server-side settings."""
        if self._client is not None:
            return self._client

        api_key = settings.gemini_api_key
        if not api_key:
            raise LLMConfigurationError(
                "GEMINI_API_KEY is not configured on the server."
            )

        try:
            from google.genai import Client
            self._client = Client(api_key=api_key)
            return self._client
        except Exception as exc:
            logger.error("Failed to initialize Google GenAI client: %s", type(exc).__name__)
            raise LLMConfigurationError(
                "Failed to initialize Gemini client with server credentials."
            ) from None

    def get_model_id(self, tier: ModelTier) -> str:
        """Retrieve the configured model identifier for a given tier."""
        if tier == ModelTier.HIGH:
            model_id = settings.gemini_model_high
        elif tier == ModelTier.MID:
            model_id = settings.gemini_model_mid
        elif tier == ModelTier.LITE:
            model_id = settings.gemini_model_lite
        else:
            raise LLMConfigurationError(f"Unsupported model tier: {tier}")

        if not model_id:
            raise LLMConfigurationError(
                f"Model identifier for tier '{tier.value}' is not configured. "
                f"Set GEMINI_MODEL_{tier.name} in environment."
            )
        return model_id

    async def generate(
        self,
        tier: ModelTier,
        prompt: str,
        system_instruction: str | None = None,
        temperature: float = 0.2,
    ) -> str:
        """Generate text using the specified model tier."""
        client = self._get_sdk_client()
        model_id = self.get_model_id(tier)

        config_dict: dict[str, Any] = {
            "temperature": temperature,
        }
        if system_instruction:
            config_dict["system_instruction"] = system_instruction

        timeout = settings.gemini_timeout_seconds

        try:
            response = await asyncio.wait_for(
                client.aio.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config=config_dict,
                ),
                timeout=timeout,
            )
            return response.text or ""
        except asyncio.TimeoutError:
            logger.warning("Gemini generation timed out after %.1fs on model %s", timeout, model_id)
            raise LLMProviderError(f"Gemini API timed out after {timeout} seconds.") from None
        except Exception as exc:
            err_str = str(exc)
            if "429" in err_str or "quota" in err_str.lower() or "resource_exhausted" in err_str.lower():
                logger.warning("Gemini quota exceeded or rate limit reached: %s", type(exc).__name__)
                raise LLMQuotaExceededError("Gemini API rate limit or quota exceeded.") from None
            logger.error("Gemini provider error: %s", type(exc).__name__)
            raise LLMProviderError("Gemini provider error occurred.") from None

    async def generate_json(
        self,
        tier: ModelTier,
        prompt: str,
        system_instruction: str | None = None,
        temperature: float = 0.0,
    ) -> dict[str, Any]:
        """Generate and parse structured JSON output from Gemini."""
        raw_text = await self.generate(
            tier=tier,
            prompt=prompt,
            system_instruction=system_instruction,
            temperature=temperature,
        )

        cleaned = raw_text.strip()
        # Sanitize markdown code fences if present
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
            cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except Exception as exc:
            logger.warning("Failed to parse Gemini structured JSON: %s", str(exc)[:100])
            raise LLMFormattingError("Provider output could not be parsed as valid JSON.") from None


gemini_client = GeminiClient()

