"""Session service managing in-memory mock session lifecycle."""
from __future__ import annotations

from app.core.errors import raise_api_error
from app.schemas.session import SessionCreate
from app.services.fixture_service import fixture_service

DEFAULT_SEEDED_SESSION = {
    "sess_demo_001": {
        "language": "hi",
        "mode": "voice",
    }
}


class SessionService:
    """Manages session creation, retrieval, and state validation in mock mode."""

    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, str]] = {}
        self.reset_store()

    def reset_store(self) -> None:
        """Reset the session store to default seeded state (used for test isolation)."""
        self._sessions = {
            session_id: dict(data)
            for session_id, data in DEFAULT_SEEDED_SESSION.items()
        }

    def session_exists(self, session_id: str) -> bool:
        """Check whether a session exists."""
        return session_id in self._sessions

    def get_session_settings(self, session_id: str) -> dict[str, str] | None:
        """Retrieve stored settings for a session."""
        return self._sessions.get(session_id)

    def create_session(self, payload: SessionCreate) -> dict:
        """Create a new mock session backed by session_create_response.json fixture."""
        session = fixture_service.load_fixture("session_create_response.json")
        session_id = session["session_id"]
        session.update(language=payload.language, mode=payload.mode)
        self._sessions[session_id] = {
            "language": payload.language,
            "mode": payload.mode,
        }
        return session

    def get_session(self, session_id: str) -> dict:
        """Retrieve an existing session backed by session_get_response.json fixture."""
        settings = self._sessions.get(session_id)
        if settings is None:
            raise_api_error(
                404,
                "SESSION_NOT_FOUND",
                "The requested conversation session was not found.",
            )
        session = fixture_service.load_fixture("session_get_response.json")
        session.update(session_id=session_id, **settings)
        return session


session_service = SessionService()

