"""Session repository providing persistence operations for conversation sessions."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
import logging

from app.database.connection import get_connection

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SessionRecord:
    """Relational session record representation."""

    session_id: str
    status: str
    language: str
    mode: str
    created_at: datetime
    updated_at: datetime
    version: int

    def to_dict(self) -> dict:
        """Convert session record to dictionary representation."""
        return {
            "session_id": self.session_id,
            "status": self.status,
            "language": self.language,
            "mode": self.mode,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else str(self.updated_at),
            "version": self.version,
        }


class SessionRepository:
    """Asynchronous PostgreSQL repository for sessions."""

    async def create_session(
        self,
        session_id: str | None = None,
        language: str = "hi",
        mode: str = "voice",
        status: str = "active",
    ) -> SessionRecord:
        """Create and persist a new session record.

        Generates a prefixed UUID4 session_id if one is not provided.
        """
        sid = session_id or f"sess_{uuid.uuid4().hex}"
        query = """
            INSERT INTO sessions (
                session_id,
                status,
                language,
                mode,
                created_at,
                updated_at,
                version
            ) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
            RETURNING session_id, status, language, mode, created_at, updated_at, version;
        """
        async with get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (sid, status, language, mode))
                row = await cur.fetchone()
                assert row is not None
                record = SessionRecord(*row)
                logger.debug("Created session record: %s", record.session_id)
                return record

    async def get_session(self, session_id: str) -> SessionRecord | None:
        """Retrieve a session by its session_id. Returns None if not found."""
        query = """
            SELECT session_id, status, language, mode, created_at, updated_at, version
            FROM sessions
            WHERE session_id = %s;
        """
        async with get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (session_id,))
                row = await cur.fetchone()
                if row is None:
                    return None
                return SessionRecord(*row)

    async def session_exists(self, session_id: str) -> bool:
        """Check whether a session exists in the database."""
        query = "SELECT 1 FROM sessions WHERE session_id = %s;"
        async with get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (session_id,))
                row = await cur.fetchone()
                return row is not None

    async def update_session_version(
        self,
        session_id: str,
        expected_version: int,
    ) -> bool:
        """Increment session version if it matches the expected version (optimistic locking).

        Returns True if a row was updated, False if version conflict or session not found.
        """
        query = """
            UPDATE sessions
            SET version = version + 1, updated_at = CURRENT_TIMESTAMP
            WHERE session_id = %s AND version = %s
            RETURNING version;
        """
        async with get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (session_id, expected_version))
                row = await cur.fetchone()
                return row is not None


session_repository = SessionRepository()

