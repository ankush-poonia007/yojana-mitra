"""Unit tests for SessionRepository and TurnRepository persistence operations."""
from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from app.database.repositories import (
    ConcurrencyConflictError,
    SessionNotFoundError,
    SessionRecord,
    TurnRecord,
    session_repository,
    turn_repository,
)


@pytest.fixture
def mock_db_connection():
    """Create a mock connection and cursor with async context managers."""
    mock_cur = AsyncMock()
    mock_tx = MagicMock()
    mock_tx.__aenter__ = AsyncMock(return_value=mock_tx)
    mock_tx.__aexit__ = AsyncMock(return_value=None)

    mock_conn = MagicMock()
    mock_conn.transaction.return_value = mock_tx
    mock_conn.cursor.return_value.__aenter__ = AsyncMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__aexit__ = AsyncMock(return_value=None)

    @asynccontextmanager
    async def fake_get_connection():
        yield mock_conn

    return fake_get_connection, mock_conn, mock_cur, mock_tx


@pytest.mark.asyncio
async def test_create_session_success(mock_db_connection):
    """Verify session creation returns a SessionRecord and parameterizes query."""
    fake_get_conn, _, mock_cur, _ = mock_db_connection
    now = datetime.now(timezone.utc)
    mock_cur.fetchone.return_value = ("sess_abc123", "active", "hi", "voice", now, now, 1)

    with patch("app.database.repositories.session_repository.get_connection", fake_get_conn):
        session = await session_repository.create_session(
            session_id="sess_abc123",
            language="hi",
            mode="voice",
        )

    assert isinstance(session, SessionRecord)
    assert session.session_id == "sess_abc123"
    assert session.status == "active"
    assert session.language == "hi"
    assert session.mode == "voice"
    assert session.version == 1

    # Verify query and parameters
    call_args = mock_cur.execute.call_args
    sql = call_args[0][0]
    params = call_args[0][1]
    assert "INSERT INTO sessions" in sql
    assert params == ("sess_abc123", "active", "hi", "voice")


@pytest.mark.asyncio
async def test_create_session_generates_prefixed_uuid(mock_db_connection):
    """Verify automatic generation of prefixed UUID4 session_id when omitted."""
    fake_get_conn, _, mock_cur, _ = mock_db_connection
    now = datetime.now(timezone.utc)

    # Intercept query to verify generated ID format
    async def fake_execute(query, params):
        generated_id = params[0]
        assert generated_id.startswith("sess_")
        assert len(generated_id) > 10
        mock_cur.fetchone.return_value = (generated_id, "active", "en", "text", now, now, 1)

    mock_cur.execute.side_effect = fake_execute

    with patch("app.database.repositories.session_repository.get_connection", fake_get_conn):
        session = await session_repository.create_session(language="en", mode="text")

    assert session.session_id.startswith("sess_")
    assert session.language == "en"
    assert session.mode == "text"


@pytest.mark.asyncio
async def test_get_session_found(mock_db_connection):
    """Verify get_session returns SessionRecord when session exists."""
    fake_get_conn, _, mock_cur, _ = mock_db_connection
    now = datetime.now(timezone.utc)
    mock_cur.fetchone.return_value = ("sess_found", "active", "hi", "voice", now, now, 2)

    with patch("app.database.repositories.session_repository.get_connection", fake_get_conn):
        session = await session_repository.get_session("sess_found")

    assert session is not None
    assert session.session_id == "sess_found"
    assert session.version == 2
    mock_cur.execute.assert_called_once()
    assert mock_cur.execute.call_args[0][1] == ("sess_found",)


@pytest.mark.asyncio
async def test_get_session_not_found(mock_db_connection):
    """Verify get_session returns None when session does not exist."""
    fake_get_conn, _, mock_cur, _ = mock_db_connection
    mock_cur.fetchone.return_value = None

    with patch("app.database.repositories.session_repository.get_connection", fake_get_conn):
        session = await session_repository.get_session("sess_missing")

    assert session is None


@pytest.mark.asyncio
async def test_session_exists(mock_db_connection):
    """Verify session_exists returns True when found, False otherwise."""
    fake_get_conn, _, mock_cur, _ = mock_db_connection

    mock_cur.fetchone.return_value = (1,)
    with patch("app.database.repositories.session_repository.get_connection", fake_get_conn):
        assert await session_repository.session_exists("sess_exists") is True

    mock_cur.fetchone.return_value = None
    with patch("app.database.repositories.session_repository.get_connection", fake_get_conn):
        assert await session_repository.session_exists("sess_does_not_exist") is False


@pytest.mark.asyncio
async def test_update_session_version(mock_db_connection):
    """Verify update_session_version increments version and reports success/conflict."""
    fake_get_conn, _, mock_cur, _ = mock_db_connection

    # Success: row updated
    mock_cur.fetchone.return_value = (2,)
    with patch("app.database.repositories.session_repository.get_connection", fake_get_conn):
        updated = await session_repository.update_session_version("sess_1", expected_version=1)
        assert updated is True

    # Conflict or not found: 0 rows updated
    mock_cur.fetchone.return_value = None
    with patch("app.database.repositories.session_repository.get_connection", fake_get_conn):
        updated = await session_repository.update_session_version("sess_1", expected_version=1)
        assert updated is False


@pytest.mark.asyncio
async def test_append_turn_pair_success(mock_db_connection):
    """Verify atomic append of user and assistant turns with deterministic ordering."""
    fake_get_conn, _, mock_cur, mock_tx = mock_db_connection
    now = datetime.now(timezone.utc)

    # Sequence of fetchone results:
    # 1. UPDATE sessions -> returns (2,) [version incremented]
    # 2. SELECT MAX(turn_index) -> returns (1,) [existing last index is 1]
    # 3. INSERT user turn -> returns TurnRecord tuple
    # 4. INSERT assistant turn -> returns TurnRecord tuple
    mock_cur.fetchone.side_effect = [
        (2,),  # version update success
        (1,),  # last turn_index was 1
        ("turn_u1", "sess_demo", 2, "user", "User question", now),
        ("turn_a1", "sess_demo", 3, "assistant", "Assistant reply", now),
    ]

    with patch("app.database.repositories.turn_repository.get_connection", fake_get_conn):
        u_turn, a_turn = await turn_repository.append_turn_pair(
            session_id="sess_demo",
            expected_version=1,
            user_text="User question",
            assistant_text="Assistant reply",
            user_turn_id="turn_u1",
            assistant_turn_id="turn_a1",
        )

    assert u_turn.turn_id == "turn_u1"
    assert u_turn.turn_index == 2
    assert u_turn.role == "user"
    assert u_turn.text == "User question"

    assert a_turn.turn_id == "turn_a1"
    assert a_turn.turn_index == 3
    assert a_turn.role == "assistant"
    assert a_turn.text == "Assistant reply"

    # Verify transaction context was entered
    mock_tx.__aenter__.assert_awaited_once()


@pytest.mark.asyncio
async def test_append_turn_pair_concurrency_conflict(mock_db_connection):
    """Verify ConcurrencyConflictError is raised when session version does not match."""
    fake_get_conn, _, mock_cur, _ = mock_db_connection

    # 1. UPDATE sessions returns None (version mismatch)
    # 2. SELECT version returns (5,) [actual version is 5, expected was 1]
    mock_cur.fetchone.side_effect = [
        None,
        (5,),
    ]

    with patch("app.database.repositories.turn_repository.get_connection", fake_get_conn):
        with pytest.raises(ConcurrencyConflictError, match="expected version 1, but found version 5"):
            await turn_repository.append_turn_pair(
                session_id="sess_stale",
                expected_version=1,
                user_text="Stale user text",
                assistant_text="Stale reply",
            )


@pytest.mark.asyncio
async def test_append_turn_pair_unknown_session(mock_db_connection):
    """Verify SessionNotFoundError is raised when session does not exist at all."""
    fake_get_conn, _, mock_cur, _ = mock_db_connection

    # 1. UPDATE sessions returns None
    # 2. SELECT version returns None (session not found)
    mock_cur.fetchone.side_effect = [
        None,
        None,
    ]

    with patch("app.database.repositories.turn_repository.get_connection", fake_get_conn):
        with pytest.raises(SessionNotFoundError, match="was not found in persistence"):
            await turn_repository.append_turn_pair(
                session_id="sess_nonexistent",
                expected_version=1,
                user_text="User text",
                assistant_text="Reply",
            )


@pytest.mark.asyncio
async def test_append_turn_pair_atomic_rollback_on_second_insert_failure(mock_db_connection):
    """Verify transaction rolls back if assistant insert fails after user turn inserted."""
    fake_get_conn, _, mock_cur, mock_tx = mock_db_connection
    now = datetime.now(timezone.utc)

    # Mock execute side effects:
    # 1. UPDATE sessions: success
    # 2. SELECT MAX(turn_index): success
    # 3. INSERT user turn: success
    # 4. INSERT assistant turn: raises database exception
    mock_cur.fetchone.side_effect = [
        (2,),
        (-1,),
        ("turn_u1", "sess_atomic", 0, "user", "User text", now),
    ]

    async def fake_execute(query, params=None):
        if "INSERT INTO conversation_turns" in query and params and params[3] == "assistant":
            raise Exception("Disk write failure during assistant turn insert")

    mock_cur.execute.side_effect = fake_execute

    with patch("app.database.repositories.turn_repository.get_connection", fake_get_conn):
        with pytest.raises(Exception, match="Disk write failure during assistant turn insert"):
            await turn_repository.append_turn_pair(
                session_id="sess_atomic",
                expected_version=1,
                user_text="User text",
                assistant_text="Reply",
            )

    # Verify transaction context exited with exception (triggering rollback)
    mock_tx.__aexit__.assert_awaited_once()
    assert mock_tx.__aexit__.call_args[0][0] is not None


@pytest.mark.asyncio
async def test_get_turns_for_session_ordered(mock_db_connection):
    """Verify get_turns_for_session returns chronologically ordered TurnRecords."""
    fake_get_conn, _, mock_cur, _ = mock_db_connection
    now = datetime.now(timezone.utc)

    mock_cur.fetchall.return_value = [
        ("turn_001", "sess_history", 0, "user", "Hello", now),
        ("turn_002", "sess_history", 1, "assistant", "Welcome", now),
        ("turn_003", "sess_history", 2, "user", "Am I eligible?", now),
    ]

    with patch("app.database.repositories.turn_repository.get_connection", fake_get_conn):
        turns = await turn_repository.get_turns_for_session("sess_history")

    assert len(turns) == 3
    assert [t.turn_index for t in turns] == [0, 1, 2]
    assert [t.role for t in turns] == ["user", "assistant", "user"]

    # Verify history export format matches frozen contract
    history_items = [t.to_history_dict() for t in turns]
    assert history_items == [
        {"turn_id": "turn_001", "role": "user", "text": "Hello"},
        {"turn_id": "turn_002", "role": "assistant", "text": "Welcome"},
        {"turn_id": "turn_003", "role": "user", "text": "Am I eligible?"},
    ]

