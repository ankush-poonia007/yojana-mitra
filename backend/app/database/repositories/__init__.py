"""Database repositories for Yojana Mitra persistence foundation."""
from __future__ import annotations


class RepositoryError(Exception):
    """Base exception for all database repository errors."""


class SessionNotFoundError(RepositoryError):
    """Raised when a requested session does not exist in persistence."""


class ConcurrencyConflictError(RepositoryError):
    """Raised when an optimistic concurrency version conflict occurs."""


from app.database.repositories.session_repository import (
    SessionRecord,
    SessionRepository,
    session_repository,
)
from app.database.repositories.turn_repository import (
    TurnRecord,
    TurnRepository,
    turn_repository,
)

__all__ = [
    "RepositoryError",
    "SessionNotFoundError",
    "ConcurrencyConflictError",
    "SessionRecord",
    "SessionRepository",
    "session_repository",
    "TurnRecord",
    "TurnRepository",
    "turn_repository",
]

