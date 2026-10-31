"""Conversation turn repository providing atomic pair persistence and ordered retrieval."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
import logging

from app.database.connection import get_connection
from app.database.repositories import ConcurrencyConflictError, SessionNotFoundError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TurnRecord:
    """Relational conversation turn record representation."""

    turn_id: str
    session_id: str
    turn_index: int
    role: str
    text: str
    created_at: datetime

    def to_dict(self) -> dict:
        """Convert turn record to dictionary representation."""
        return {
            "turn_id": self.turn_id,
            "session_id": self.session_id,
            "turn_index": self.turn_index,
            "role": self.role,
            "text": self.text,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
        }

    def to_history_dict(self) -> dict:
        """Convert turn record to external history shape matching frozen API contract."""
        return {
            "turn_id": self.turn_id,
            "role": self.role,
            "text": self.text,
        }


class TurnRepository:
    """Asynchronous PostgreSQL repository for conversation turns."""

    async def append_turn_pair(
        self,
        session_id: str,
        expected_version: int,
        user_text: str,
        assistant_text: str,
        user_turn_id: str | None = None,
        assistant_turn_id: str | None = None,
    ) -> tuple[TurnRecord, TurnRecord]:
        """Atomically persist a user/assistant turn pair within a single database transaction.

        Enforces optimistic concurrency on the session record, determines next turn indices,
        inserts both turns, and commits atomically. Rolls back both if any operation fails.
        """
        async with get_connection() as conn:
            async with conn.transaction():
                async with conn.cursor() as cur:
                    # 1. Optimistic concurrency check & session version increment
                    await cur.execute(
                        """
                        UPDATE sessions
                        SET version = version + 1, updated_at = CURRENT_TIMESTAMP
                        WHERE session_id = %s AND version = %s
                        RETURNING version;
                        """,
                        (session_id, expected_version),
                    )
                    row = await cur.fetchone()
                    if not row:
                        # Differentiate between session missing and optimistic concurrency conflict
                        await cur.execute(
                            "SELECT version FROM sessions WHERE session_id = %s;",
                            (session_id,),
                        )
                        ver_row = await cur.fetchone()
                        if not ver_row:
                            raise SessionNotFoundError(
                                f"Session '{session_id}' was not found in persistence."
                            )
                        actual_version = ver_row[0]
                        raise ConcurrencyConflictError(
                            f"Optimistic concurrency conflict for session '{session_id}': "
                            f"expected version {expected_version}, but found version {actual_version}."
                        )

                    # 2. Determine next turn indices
                    await cur.execute(
                        "SELECT COALESCE(MAX(turn_index), -1) FROM conversation_turns WHERE session_id = %s;",
                        (session_id,),
                    )
                    max_row = await cur.fetchone()
                    last_index = max_row[0] if max_row else -1
                    user_index = last_index + 1
                    assistant_index = last_index + 2

                    # 3. Generate turn identifiers if not provided
                    u_id = user_turn_id or f"turn_{uuid.uuid4().hex}"
                    a_id = assistant_turn_id or f"turn_{uuid.uuid4().hex}"

                    # 4. Insert user turn
                    await cur.execute(
                        """
                        INSERT INTO conversation_turns (
                            turn_id,
                            session_id,
                            turn_index,
                            role,
                            text,
                            created_at
                        ) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                        RETURNING turn_id, session_id, turn_index, role, text, created_at;
                        """,
                        (u_id, session_id, user_index, "user", user_text),
                    )
                    u_row = await cur.fetchone()
                    assert u_row is not None
                    user_record = TurnRecord(*u_row)

                    # 5. Insert assistant turn
                    await cur.execute(
                        """
                        INSERT INTO conversation_turns (
                            turn_id,
                            session_id,
                            turn_index,
                            role,
                            text,
                            created_at
                        ) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                        RETURNING turn_id, session_id, turn_index, role, text, created_at;
                        """,
                        (a_id, session_id, assistant_index, "assistant", assistant_text),
                    )
                    a_row = await cur.fetchone()
                    assert a_row is not None
                    assistant_record = TurnRecord(*a_row)

                    logger.debug(
                        "Atomically persisted turn pair for session %s (indices %d, %d)",
                        session_id,
                        user_index,
                        assistant_index,
                    )
                    return (user_record, assistant_record)

    async def get_turns_for_session(self, session_id: str) -> list[TurnRecord]:
        """Retrieve all conversation turns for a session in strictly increasing turn_index order."""
        query = """
            SELECT turn_id, session_id, turn_index, role, text, created_at
            FROM conversation_turns
            WHERE session_id = %s
            ORDER BY turn_index ASC;
        """
        async with get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (session_id,))
                rows = await cur.fetchall()
                return [TurnRecord(*row) for row in rows]


turn_repository = TurnRepository()
