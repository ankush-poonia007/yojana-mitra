"""Turn service managing text and voice turn interactions in mock mode."""
from __future__ import annotations

from fastapi import UploadFile
from app.core.errors import raise_api_error
from app.schemas.turn import TextTurn
from app.services.fixture_service import fixture_service
from app.services.session_service import session_service


class TurnService:
    """Processes text and voice conversation turns against canonical fixtures."""

    async def process_text_turn(self, payload: TextTurn) -> dict:
        """Process a text turn using turn_awaiting_response.json fixture."""
        settings = session_service.get_session_settings(payload.session_id)
        if settings is None:
            raise_api_error(
                404,
                "SESSION_NOT_FOUND",
                "The requested conversation session was not found.",
            )

        if not payload.text.strip():
            raise_api_error(400, "EMPTY_TEXT_INPUT", "Text input cannot be empty.")

        turn = fixture_service.load_fixture("turn_awaiting_response.json")
        turn.update(
            session_id=payload.session_id,
            language=settings["language"],
        )
        return turn

    async def process_voice_turn(
        self,
        session_id: str,
        audio: UploadFile,
        language: str | None = None,
    ) -> dict:
        """Process a voice turn using voice_turn_response.json fixture."""
        settings = session_service.get_session_settings(session_id)
        if settings is None:
            raise_api_error(
                404,
                "SESSION_NOT_FOUND",
                "The requested conversation session was not found.",
            )

        # Validate optional language parameter if provided
        lang = language.strip() if language else None
        if lang and lang not in {"hi", "en"}:
            raise_api_error(
                422,
                "INVALID_REQUEST",
                "The selected language is not supported.",
            )

        # Read only 1 byte to reject empty audio uploads without persisting raw audio
        if not await audio.read(1):
            raise_api_error(400, "INVALID_AUDIO", "The uploaded audio is empty.")

        turn = fixture_service.load_fixture("voice_turn_response.json")
        turn.update(
            session_id=session_id,
            language=lang or settings["language"],
        )
        return turn


turn_service = TurnService()

