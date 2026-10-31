"""Session service managing session lifecycle in mock and persistent modes."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any
from app.core.config import settings
from app.core.errors import raise_api_error
from app.schemas.session import SessionCreate
from app.services.fixture_service import fixture_service

if TYPE_CHECKING:
    from app.database.repositories.session_repository import SessionRepository
    from app.database.repositories.turn_repository import TurnRepository

DEFAULT_SEEDED_SESSION: dict[str, dict[str, Any]] = {
    "sess_demo_001": {
        "session_id": "sess_demo_001",
        "language": "hi",
        "mode": "voice",
        "status": "active",
        "version": 1,
    }
}


class SessionService:
    """Manages session creation, retrieval, and state validation in mock and persistent modes."""

    def __init__(
        self,
        session_repository: SessionRepository | None = None,
        turn_repository: TurnRepository | None = None,
    ) -> None:
        self._session_repo = session_repository
        self._turn_repo = turn_repository
        self._sessions: dict[str, dict[str, Any]] = {}
        self.reset_store()

    @property
    def session_repo(self) -> SessionRepository:
        """Lazily load default SessionRepository if not injected."""
        if self._session_repo is None:
            from app.database.repositories.session_repository import session_repository
            self._session_repo = session_repository
        return self._session_repo

    @property
    def turn_repo(self) -> TurnRepository:
        """Lazily load default TurnRepository if not injected."""
        if self._turn_repo is None:
            from app.database.repositories.turn_repository import turn_repository
            self._turn_repo = turn_repository
        return self._turn_repo

    def reset_store(self) -> None:
        """Reset the in-memory mock session store to default seeded state."""
        self._sessions = {
            session_id: dict(data)
            for session_id, data in DEFAULT_SEEDED_SESSION.items()
        }

    async def session_exists(self, session_id: str) -> bool:
        """Check whether a session exists."""
        if settings.mock_mode:
            return session_id in self._sessions
        return await self.session_repo.session_exists(session_id)

    async def get_session_settings(self, session_id: str) -> dict[str, Any] | None:
        """Retrieve stored settings and concurrency version for a session."""
        if settings.mock_mode:
            return self._sessions.get(session_id)

        record = await self.session_repo.get_session(session_id)
        if record is None:
            return None
        return {
            "session_id": record.session_id,
            "status": record.status,
            "language": record.language,
            "mode": record.mode,
            "version": record.version,
        }

    async def create_session(self, payload: SessionCreate) -> dict[str, Any]:
        """Create a new consultation session."""
        if settings.mock_mode:
            session = fixture_service.load_fixture("session_create_response.json")
            session_id = session["session_id"]
            session.update(language=payload.language, mode=payload.mode)
            self._sessions[session_id] = {
                "session_id": session_id,
                "language": payload.language,
                "mode": payload.mode,
                "status": session.get("status", "active"),
                "version": 1,
            }
            return session

        record = await self.session_repo.create_session(
            language=payload.language,
            mode=payload.mode,
        )
        return {
            "session_id": record.session_id,
            "status": record.status,
            "language": record.language,
            "mode": record.mode,
            "created_at": (
                record.created_at.isoformat()
                if hasattr(record.created_at, "isoformat")
                else str(record.created_at)
            ),
        }

    async def get_session(self, session_id: str) -> dict[str, Any]:
        """Retrieve an existing session and turn history."""
        if settings.mock_mode:
            s_data = self._sessions.get(session_id)
            if s_data is None:
                raise_api_error(
                    404,
                    "SESSION_NOT_FOUND",
                    "The requested conversation session was not found.",
                )
            session = fixture_service.load_fixture("session_get_response.json")
            session.update(
                session_id=session_id,
                language=s_data["language"],
                mode=s_data["mode"],
                status=s_data.get("status", "active"),
            )
            return session

        record = await self.session_repo.get_session(session_id)
        if record is None:
            raise_api_error(
                404,
                "SESSION_NOT_FOUND",
                "The requested conversation session was not found.",
            )

        turn_records = await self.turn_repo.get_turns_for_session(session_id)
        return {
            "session_id": record.session_id,
            "status": record.status,
            "language": record.language,
            "mode": record.mode,
            "turns": [t.to_history_dict() for t in turn_records],
        }


session_service = SessionService()
