"""Speech-to-text and text-to-speech seam adapter (Voice Boundary)."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class STTUnavailableError(Exception):
    """Raised when speech-to-text processing is unavailable."""


class TTSUnavailableError(Exception):
    """Raised when text-to-speech processing is unavailable."""


class SpeechAdapter:
    """Boundary adapter for isolated speech provider wrappers.

    Round 1 Pre-Integration Boundary:
    Actual STT and TTS functionality is pending provider selection, benchmark, and wrappers.
    The placeholder Base64 string satisfies the frozen Phase 3.3 response contract shape
    and must NEVER be presented as genuine synthesized audio.
    """

    @property
    def is_stt_available(self) -> bool:
        """Indicate whether genuine STT is available (Round 1: False)."""
        return False

    @property
    def is_tts_available(self) -> bool:
        """Indicate whether genuine TTS is available (Round 1: False)."""
        return False

    async def transcribe(self, audio_bytes: bytes, language: str | None = None) -> str:
        """Transcribe uploaded audio bytes in-memory.

        In Round 1: Pre-integration boundary. Raises STTUnavailableError
        ensuring zero fake speech claims.
        """
        if not audio_bytes:
            raise ValueError("Audio bytes cannot be empty.")

        # In Round 1, provider wrappers are pending Anamika's benchmark
        raise STTUnavailableError("Speech-to-text provider integration is pending.")

    async def synthesize(self, text: str, language: str = "hi") -> str:
        """Synthesize text to Base64 audio.

        In Round 1: Safe pre-integration stub returning approved contract placeholder.
        This placeholder satisfies the API response shape but is NOT genuine synthesized audio.
        """
        return "DEMO_AUDIO_DATA"


speech_adapter = SpeechAdapter()
