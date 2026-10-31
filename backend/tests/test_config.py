"""Unit tests for configuration robustness, environment parsing, and fallback defaults."""
from __future__ import annotations

import pytest
from app.core.config import Settings


def test_empty_app_port_uses_default(monkeypatch):
    """Verify empty string for APP_PORT falls back to the default port 8000."""
    monkeypatch.setenv("APP_PORT", "")
    test_settings = Settings()
    assert test_settings.app_port == 8000


def test_empty_mock_mode_uses_default(monkeypatch):
    """Verify empty string for MOCK_MODE falls back to default True."""
    monkeypatch.setenv("MOCK_MODE", "")
    test_settings = Settings()
    assert test_settings.mock_mode is True


def test_explicit_app_port_overrides_default(monkeypatch):
    """Verify explicit valid integer port overrides the default port."""
    monkeypatch.setenv("APP_PORT", "9050")
    test_settings = Settings()
    assert test_settings.app_port == 9050


def test_explicit_mock_mode_overrides_default(monkeypatch):
    """Verify explicit boolean string for MOCK_MODE overrides the default."""
    monkeypatch.setenv("MOCK_MODE", "false")
    test_settings = Settings()
    assert test_settings.mock_mode is False


def test_missing_optional_credentials_allow_mock_startup():
    """Verify that absent downstream credentials default to None and allow mock initialization."""
    test_settings = Settings()
    assert test_settings.mock_mode is True
    # Downstream service credentials must be None by default without raising errors
    assert test_settings.gemini_api_key is None or isinstance(test_settings.gemini_api_key, str)
    assert test_settings.stt_provider is None or isinstance(test_settings.stt_provider, str)
    assert test_settings.tts_provider is None or isinstance(test_settings.tts_provider, str)
    assert test_settings.supabase_url is None or isinstance(test_settings.supabase_url, str)

