"""Centralized backend configuration using Pydantic Settings."""
from __future__ import annotations

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    # Application settings
    app_env: str = "development"
    app_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    log_level: str = "INFO"
    mock_mode: bool = True

    # Downstream service settings (Phase 2+; optional in Phase 1)
    gemini_api_key: str | None = None
    gemini_model_high: str = "gemini-3.8-flash"
    gemini_model_mid: str = "gemini-3.6-flash"
    gemini_model_lite: str = "gemini-3.5-flash-lite"
    gemini_timeout_seconds: float = 15.0
    stt_provider: str | None = None
    stt_api_key: str | None = None
    stt_model: str | None = None
    tts_provider: str | None = None
    tts_api_key: str | None = None
    tts_model: str | None = None
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_role_key: str | None = None
    database_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=str(REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list of cleaned strings."""
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


settings = Settings()
