"""Turn service managing text and voice turn interactions in mock and persistent modes."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
from fastapi import UploadFile

from app.core.config import settings
from app.core.errors import raise_api_error
from app.database.repositories import ConcurrencyConflictError, SessionNotFoundError
from app.graph import YojanaWorkflowState, run_turn_workflow
from app.schemas.turn import TextTurn
from app.services.fixture_service import fixture_service

if TYPE_CHECKING:
    from app.database.repositories.turn_repository import TurnRepository
    from app.services.session_service import SessionService

logger = logging.getLogger(__name__)


class TurnService:
    """Processes text and voice conversation turns in mock and persistent modes."""

    def __init__(
        self,
        session_service_instance: SessionService | None = None,
        turn_repository_instance: TurnRepository | None = None,
    ) -> None:
        self._session_service = session_service_instance
        self._turn_repo = turn_repository_instance

    @property
    def session_service(self) -> SessionService:
        """Lazily load default SessionService if not injected."""
        if self._session_service is None:
            from app.services.session_service import session_service
            self._session_service = session_service
        return self._session_service

    @property
    def turn_repo(self) -> TurnRepository:
        """Lazily load default TurnRepository if not injected."""
        if self._turn_repo is None:
            from app.database.repositories.turn_repository import turn_repository
            self._turn_repo = turn_repository
        return self._turn_repo

    async def process_text_turn(self, payload: TextTurn) -> dict[str, Any]:
        """Process a text conversation turn."""
        session_info = await self.session_service.get_session_settings(payload.session_id)
        if session_info is None:
            raise_api_error(
                404,
                "SESSION_NOT_FOUND",
                "The requested conversation session was not found.",
            )

        cleaned_text = payload.text.strip()
        if not cleaned_text:
            raise_api_error(400, "EMPTY_TEXT_INPUT", "Text input cannot be empty.")

        if settings.mock_mode:
            turn = fixture_service.load_fixture("turn_awaiting_response.json")
            turn.update(
                session_id=payload.session_id,
                language=session_info["language"],
            )
            return turn

        # Persistent mode: retrieve prior history from database
        history = await self.turn_repo.get_turns_for_session(payload.session_id)

        # Build initial frozen 11-key workflow state
        initial_state: YojanaWorkflowState = {
            "session_id": payload.session_id,
            "language": session_info["language"],
            "input_type": "text",
            "user_text": cleaned_text,
            "intent": "scheme_query",
            "scheme_id": None,
            "eligibility_answers": {},
            "retrieved_evidence": [],
            "assessment": None,
            "response": {},
            "error": None,
        }

        # Execute stateless per-turn LangGraph workflow with history supplied via context
        result_state = await run_turn_workflow(initial_state, history=history)

        # Check for workflow error
        if result_state.get("error"):
            err = result_state["error"]
            status_code = 503 if err.get("code") == "AI_SERVICE_UNAVAILABLE" else 500
            raise_api_error(
                status_code,
                err.get("code", "INTERNAL_SERVER_ERROR"),
                err.get("message", "Workflow processing failed."),
                retryable=err.get("retryable", False),
            )

        workflow_response = result_state.get("response") or {}
        assistant_text = (
            workflow_response.get("answer", {}).get("text")
            or "मैं आपकी पात्रता समझने में मदद करूंगा। क्या आपके घर में पहले से LPG कनेक्शन है?"
        )

        expected_version = session_info.get("version", 1)
        try:
            _user_rec, assistant_rec = await self.turn_repo.append_turn_pair(
                session_id=payload.session_id,
                expected_version=expected_version,
                user_text=cleaned_text,
                assistant_text=assistant_text,
            )
        except ConcurrencyConflictError:
            raise_api_error(
                500,
                "INTERNAL_SERVER_ERROR",
                "Concurrent session modification conflict encountered. Please retry.",
                retryable=True,
            )
        except SessionNotFoundError:
            raise_api_error(
                404,
                "SESSION_NOT_FOUND",
                "The requested conversation session was not found.",
            )

        final_response = dict(workflow_response)
        final_response["session_id"] = payload.session_id
        final_response["turn_id"] = assistant_rec.turn_id
        final_response["language"] = session_info["language"]
        return final_response

    async def process_voice_turn(
        self,
        session_id: str,
        audio: UploadFile,
        language: str | None = None,
        transcription_text: str | None = None,
    ) -> dict[str, Any]:
        """Process a spoken voice turn. Raw audio is never persisted."""
        session_info = await self.session_service.get_session_settings(session_id)
        if session_info is None:
            raise_api_error(
                404,
                "SESSION_NOT_FOUND",
                "The requested conversation session was not found.",
            )

        lang = language.strip() if language else None
        if lang and lang not in {"hi", "en"}:
            raise_api_error(
                422,
                "INVALID_REQUEST",
                "The selected language is not supported.",
            )
        effective_language = lang or session_info["language"]

        # Read only 1 byte in-memory to validate audio upload is non-empty; never persisted
        chunk = await audio.read(1)
        if not chunk:
            raise_api_error(400, "INVALID_AUDIO", "The uploaded audio is empty.")

        if settings.mock_mode:
            turn = fixture_service.load_fixture("voice_turn_response.json")
            turn.update(
                session_id=session_id,
                language=effective_language,
            )
            return turn

        # Persistent mode: check speech processing / transcription availability
        if transcription_text is None:
            raise_api_error(
                503,
                "STT_UNAVAILABLE",
                "We could not process the audio. Please try again or type your response.",
                retryable=True,
            )

        # Persistent mode with available transcription: retrieve prior history
        history = await self.turn_repo.get_turns_for_session(session_id)

        # Build initial frozen 11-key workflow state
        initial_state: YojanaWorkflowState = {
            "session_id": session_id,
            "language": effective_language,
            "input_type": "voice",
            "user_text": transcription_text,
            "intent": "scheme_query",
            "scheme_id": None,
            "eligibility_answers": {},
            "retrieved_evidence": [],
            "assessment": None,
            "response": {},
            "error": None,
        }

        # Execute stateless per-turn LangGraph workflow with history supplied via context
        result_state = await run_turn_workflow(initial_state, history=history)

        if result_state.get("error"):
            err = result_state["error"]
            status_code = 503 if err.get("code") == "AI_SERVICE_UNAVAILABLE" else 500
            raise_api_error(
                status_code,
                err.get("code", "INTERNAL_SERVER_ERROR"),
                err.get("message", "Workflow processing failed."),
                retryable=err.get("retryable", False),
            )

        workflow_response = result_state.get("response") or {}
        assistant_text = (
            workflow_response.get("answer", {}).get("text")
            or "समझ गया। क्या आवेदन करने वाली महिला की उम्र 18 वर्ष या उससे अधिक है?"
        )

        expected_version = session_info.get("version", 1)
        try:
            _user_rec, assistant_rec = await self.turn_repo.append_turn_pair(
                session_id=session_id,
                expected_version=expected_version,
                user_text=transcription_text,
                assistant_text=assistant_text,
            )
        except ConcurrencyConflictError:
            raise_api_error(
                500,
                "INTERNAL_SERVER_ERROR",
                "Concurrent session modification conflict encountered. Please retry.",
                retryable=True,
            )
        except SessionNotFoundError:
            raise_api_error(
                404,
                "SESSION_NOT_FOUND",
                "The requested conversation session was not found.",
            )

        final_response = dict(workflow_response)
        final_response["session_id"] = session_id
        final_response["turn_id"] = assistant_rec.turn_id
        final_response["language"] = effective_language
        final_response["transcription"] = {
            "text": transcription_text,
            "confidence": None,
        }
        return final_response


turn_service = TurnService()
