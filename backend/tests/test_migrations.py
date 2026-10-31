"""Unit tests for native SQL migration runner, advisory locking, and checksum validation."""
from __future__ import annotations

import hashlib
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from app.database.migrations import (
    MIGRATION_ADVISORY_LOCK_ID,
    cli,
    compute_checksum,
    discover_migration_files,
    run_migrations,
)


def test_compute_checksum_deterministic():
    """Verify SHA-256 checksum computation is deterministic."""
    sql = "CREATE TABLE test (id INT);"
    expected = hashlib.sha256(sql.encode("utf-8")).hexdigest()
    assert compute_checksum(sql) == expected


def test_discover_migration_files_sorting(tmp_path: Path):
    """Verify discovery finds SQL files and orders them naturally by filename."""
    (tmp_path / "002_add_indexes.sql").write_text("SELECT 2;", encoding="utf-8")
    (tmp_path / "001_initial.sql").write_text("SELECT 1;", encoding="utf-8")
    (tmp_path / "ignored.txt").write_text("ignored", encoding="utf-8")

    files = discover_migration_files(tmp_path)
    assert len(files) == 2
    assert files[0].name == "001_initial.sql"
    assert files[1].name == "002_add_indexes.sql"


def test_discover_migration_files_nonexistent_dir(tmp_path: Path):
    """Verify nonexistent directory returns empty list without error."""
    nonexistent = tmp_path / "missing_dir"
    assert discover_migration_files(nonexistent) == []


@pytest.mark.asyncio
async def test_mock_mode_blocks_migrations(monkeypatch):
    """Verify migrations refuse to run when MOCK_MODE is true and no URL is provided."""
    monkeypatch.setattr("app.database.migrations.settings.mock_mode", True)
    monkeypatch.setattr("app.database.migrations.settings.database_url", None)

    with patch("psycopg.AsyncConnection.connect", new_callable=AsyncMock) as mock_connect:
        with pytest.raises(RuntimeError, match="Migrations cannot run in MOCK_MODE"):
            await run_migrations()
        mock_connect.assert_not_called()


@pytest.mark.asyncio
async def test_mock_mode_blocks_migrations_even_with_explicit_url(monkeypatch):
    """Verify migrations refuse to run and do not connect when MOCK_MODE is true, even with explicit URL."""
    monkeypatch.setattr("app.database.migrations.settings.mock_mode", True)
    monkeypatch.setattr("app.database.migrations.settings.database_url", "postgresql://configured:pw@localhost:5432/db")

    with patch("psycopg.AsyncConnection.connect", new_callable=AsyncMock) as mock_connect:
        with pytest.raises(RuntimeError, match="Migrations cannot run in MOCK_MODE"):
            await run_migrations(database_url="postgresql://explicit:pw@localhost:5432/db")
        mock_connect.assert_not_called()


@pytest.mark.asyncio
async def test_missing_database_url_blocks_migrations(monkeypatch):
    """Verify migrations fail clearly when DATABASE_URL is missing in persistent mode."""
    monkeypatch.setattr("app.database.migrations.settings.mock_mode", False)
    monkeypatch.setattr("app.database.migrations.settings.database_url", None)

    with pytest.raises(RuntimeError, match="DATABASE_URL must be configured"):
        await run_migrations()


@pytest.mark.asyncio
async def test_fresh_migration_execution(tmp_path: Path, monkeypatch):
    """Verify fresh migration executes advisory lock, schema table, and inserts bookkeeping."""
    monkeypatch.setattr("app.database.migrations.settings.mock_mode", False)

    sql_file = tmp_path / "001_create_core_persistence.sql"
    sql_file.write_text("CREATE TABLE test_tab (id INT);", encoding="utf-8")

    mock_cur = AsyncMock()
    # First fetchall returns empty list (no applied migrations)
    mock_cur.fetchall.return_value = []

    mock_tx = MagicMock()
    mock_tx.__aenter__ = AsyncMock(return_value=mock_tx)
    mock_tx.__aexit__ = AsyncMock(return_value=None)

    mock_conn = MagicMock()
    mock_conn.closed = False
    mock_conn.transaction.return_value = mock_tx
    mock_conn.cursor.return_value.__aenter__ = AsyncMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_conn.close = AsyncMock()

    with patch("psycopg.AsyncConnection.connect", new_callable=AsyncMock, return_value=mock_conn):
        applied = await run_migrations(
            database_url="postgresql://user:pass@localhost:5432/testdb",
            migrations_dir=tmp_path,
        )

    assert applied == ["001"]

    # Verify transaction-scoped advisory lock was called with the approved key
    mock_cur.execute.assert_any_call(
        "SELECT pg_advisory_xact_lock(%s);",
        (MIGRATION_ADVISORY_LOCK_ID,),
    )
    # Verify migration file SQL was executed
    mock_cur.execute.assert_any_call("CREATE TABLE test_tab (id INT);")
    # Verify bookkeeping record was inserted
    expected_checksum = compute_checksum("CREATE TABLE test_tab (id INT);")
    mock_cur.execute.assert_any_call(
        "INSERT INTO schema_migrations (version, name, checksum) VALUES (%s, %s, %s);",
        ("001", "001_create_core_persistence", expected_checksum),
    )


@pytest.mark.asyncio
async def test_idempotent_repeated_migration_execution(tmp_path: Path, monkeypatch):
    """Verify already-applied migration with matching checksum is cleanly skipped."""
    monkeypatch.setattr("app.database.migrations.settings.mock_mode", False)

    content = "CREATE TABLE test_tab (id INT);"
    sql_file = tmp_path / "001_create_core_persistence.sql"
    sql_file.write_text(content, encoding="utf-8")
    checksum = compute_checksum(content)

    mock_cur = AsyncMock()
    # Migration 001 already recorded in schema_migrations
    mock_cur.fetchall.return_value = [("001", checksum)]

    mock_tx = MagicMock()
    mock_tx.__aenter__ = AsyncMock(return_value=mock_tx)
    mock_tx.__aexit__ = AsyncMock(return_value=None)

    mock_conn = MagicMock()
    mock_conn.closed = False
    mock_conn.transaction.return_value = mock_tx
    mock_conn.cursor.return_value.__aenter__ = AsyncMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_conn.close = AsyncMock()

    with patch("psycopg.AsyncConnection.connect", new_callable=AsyncMock, return_value=mock_conn):
        applied = await run_migrations(
            database_url="postgresql://user:pass@localhost:5432/testdb",
            migrations_dir=tmp_path,
        )

    # Idempotent: 0 new migrations applied
    assert applied == []
    # Verify content was NOT re-executed
    for call_args in mock_cur.execute.call_args_list:
        assert call_args[0][0] != content


@pytest.mark.asyncio
async def test_checksum_mismatch_halts_migration(tmp_path: Path, monkeypatch):
    """Verify checksum mismatch raises error and halts execution before running subsequent scripts."""
    monkeypatch.setattr("app.database.migrations.settings.mock_mode", False)

    sql_file = tmp_path / "001_create_core_persistence.sql"
    sql_file.write_text("ALTERED CONTENT;", encoding="utf-8")

    mock_cur = AsyncMock()
    # Recorded checksum in DB does not match the altered file
    mock_cur.fetchall.return_value = [("001", "old_different_hash_12345")]

    mock_tx = MagicMock()
    mock_tx.__aenter__ = AsyncMock(return_value=mock_tx)
    mock_tx.__aexit__ = AsyncMock(return_value=None)

    mock_conn = MagicMock()
    mock_conn.closed = False
    mock_conn.transaction.return_value = mock_tx
    mock_conn.cursor.return_value.__aenter__ = AsyncMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_conn.close = AsyncMock()

    with patch("psycopg.AsyncConnection.connect", new_callable=AsyncMock, return_value=mock_conn):
        with pytest.raises(RuntimeError, match="Checksum mismatch for migration 001_create_core_persistence.sql"):
            await run_migrations(
                database_url="postgresql://user:pass@localhost:5432/testdb",
                migrations_dir=tmp_path,
            )


@pytest.mark.asyncio
async def test_migration_failure_rolls_back_and_cleans_up(tmp_path: Path, monkeypatch):
    """Verify SQL error rolls back transaction and scrubs credentials from error output."""
    monkeypatch.setattr("app.database.migrations.settings.mock_mode", False)

    secret_pw = "super_classified_pw_8888"
    fake_url = f"postgresql://dbuser:{secret_pw}@db.example.com:5432/proddb"

    sql_file = tmp_path / "001_create_core_persistence.sql"
    sql_file.write_text("INVALID SQL STATEMENT;", encoding="utf-8")

    mock_cur = AsyncMock()
    mock_cur.fetchall.return_value = []
    # Fail when executing the migration file
    mock_cur.execute.side_effect = [
        None,  # advisory lock
        None,  # create schema_migrations
        None,  # select schema_migrations
        Exception(f"Syntax error near INVALID on {fake_url}"),  # execute migration fails
    ]

    mock_tx = MagicMock()
    mock_tx.__aenter__ = AsyncMock(return_value=mock_tx)
    mock_tx.__aexit__ = AsyncMock(return_value=None)

    mock_conn = MagicMock()
    mock_conn.closed = False
    mock_conn.transaction.return_value = mock_tx
    mock_conn.cursor.return_value.__aenter__ = AsyncMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_conn.close = AsyncMock()

    with patch("psycopg.AsyncConnection.connect", new_callable=AsyncMock, return_value=mock_conn):
        with pytest.raises(RuntimeError) as exc_info:
            await run_migrations(
                database_url=fake_url,
                migrations_dir=tmp_path,
            )

        err_msg = str(exc_info.value)
        assert secret_pw not in err_msg
        assert fake_url not in err_msg
        assert "[REDACTED_DATABASE_URL]" in err_msg
        assert exc_info.value.__cause__ is None
        assert exc_info.value.__context__ is None


def test_cli_execution_success(monkeypatch):
    """Verify CLI exits with code 0 on successful migration run."""
    with patch("app.database.migrations.run_migrations", new_callable=AsyncMock, return_value=["001"]):
        with pytest.raises(SystemExit) as exit_info:
            cli()
        assert exit_info.value.code == 0


def test_cli_execution_failure(monkeypatch):
    """Verify CLI exits with code 1 on migration failure."""
    with patch("app.database.migrations.run_migrations", new_callable=AsyncMock, side_effect=RuntimeError("Migration failed")):
        with pytest.raises(SystemExit) as exit_info:
            cli()
        assert exit_info.value.code == 1


@pytest.mark.asyncio
async def test_unknown_recorded_migration_version_logs_warning(tmp_path: Path, monkeypatch, caplog):
    """Verify unknown recorded migration versions log a warning and are handled safely."""
    import logging
    monkeypatch.setattr("app.database.migrations.settings.mock_mode", False)

    content = "CREATE TABLE test_tab (id INT);"
    sql_file = tmp_path / "001_create_core_persistence.sql"
    sql_file.write_text(content, encoding="utf-8")

    mock_cur = AsyncMock()
    # Recorded versions contain an unknown legacy version '000' not present on disk
    mock_cur.fetchall.return_value = [("000", "legacy_hash_abc")]

    mock_tx = MagicMock()
    mock_tx.__aenter__ = AsyncMock(return_value=mock_tx)
    mock_tx.__aexit__ = AsyncMock(return_value=None)

    mock_conn = MagicMock()
    mock_conn.closed = False
    mock_conn.transaction.return_value = mock_tx
    mock_conn.cursor.return_value.__aenter__ = AsyncMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_conn.close = AsyncMock()

    with caplog.at_level(logging.WARNING):
        with patch("psycopg.AsyncConnection.connect", new_callable=AsyncMock, return_value=mock_conn):
            applied = await run_migrations(
                database_url="postgresql://user:pass@localhost:5432/testdb",
                migrations_dir=tmp_path,
            )

    assert applied == ["001"]
    assert "Database contains recorded migration version(s) not found on disk: ['000']" in caplog.text

