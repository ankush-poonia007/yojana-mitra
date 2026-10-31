"""Unit tests for PostgreSQL connection foundation, lifecycle management, and runtime matrix."""
from __future__ import annotations

import logging
import traceback
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from psycopg_pool import AsyncConnectionPool
from starlette.testclient import TestClient

from app.database.connection import (
    DatabaseManager,
    _mask_db_url,
    _sanitize_db_error_message,
    close_db,
    db_manager,
    get_connection,
    get_db_pool,
    init_db,
)
from app.main import create_app


def test_mask_db_url_removes_credentials():
    """Verify that credentials in connection strings are masked for logging."""
    url = "postgresql://dbuser:supersecretpass@db.example.com:5432/proddb"
    masked = _mask_db_url(url)
    assert "supersecretpass" not in masked
    assert "dbuser:***@db.example.com:5432/proddb" in masked

    assert _mask_db_url(None) == "[NOT SET]"
    assert _mask_db_url("") == "[NOT SET]"


def test_get_db_pool_raises_when_uninitialized():
    """Verify get_db_pool raises RuntimeError if called before initialization."""
    manager = DatabaseManager()
    with pytest.raises(RuntimeError, match="Database connection pool is not initialized"):
        manager.get_pool()


def test_mock_mode_missing_database_url_startup(monkeypatch):
    """Scenario 1: MOCK_MODE=true and DATABASE_URL is missing.

    App starts in mock mode without creating or waiting for a database pool.
    """
    monkeypatch.setattr("app.main.settings.mock_mode", True)
    monkeypatch.setattr("app.main.settings.database_url", None)

    with patch("app.database.connection.AsyncConnectionPool") as mock_pool_cls:
        app = create_app()
        with TestClient(app) as client:
            resp = client.get("/health")
            assert resp.status_code == 200
            assert resp.json() == {"status": "ok", "mode": "mock"}
            assert db_manager.is_initialized is False
        mock_pool_cls.assert_not_called()


def test_mock_mode_configured_database_url_takes_precedence(monkeypatch):
    """Scenario 2: MOCK_MODE=true with DATABASE_URL configured.

    Mock mode takes precedence; database pool is ignored and not initialized.
    """
    monkeypatch.setattr("app.main.settings.mock_mode", True)
    monkeypatch.setattr("app.main.settings.database_url", "postgresql://user:pass@localhost:5432/mockdb")

    with patch("app.database.connection.AsyncConnectionPool") as mock_pool_cls:
        app = create_app()
        with TestClient(app) as client:
            resp = client.get("/health")
            assert resp.status_code == 200
            assert resp.json() == {"status": "ok", "mode": "mock"}
            assert db_manager.is_initialized is False
        mock_pool_cls.assert_not_called()


def test_persistent_mode_missing_database_url_fails_startup(monkeypatch):
    """Scenario 3: MOCK_MODE=false and DATABASE_URL is missing.

    Startup must fail immediately with a clear configuration error.
    """
    monkeypatch.setattr("app.main.settings.mock_mode", False)
    monkeypatch.setattr("app.main.settings.database_url", None)

    app = create_app()
    with pytest.raises(RuntimeError, match="DATABASE_URL must be configured when MOCK_MODE=false"):
        with TestClient(app):
            pass


def test_persistent_mode_successful_pool_initialization(monkeypatch):
    """Scenario 4: MOCK_MODE=false with valid DATABASE_URL and reachable database.

    Pool opens during startup, waits for readiness, and closes cleanly on shutdown.
    """
    fake_url = "postgresql://user:pass@localhost:5432/yojana_db"
    monkeypatch.setattr("app.main.settings.mock_mode", False)
    monkeypatch.setattr("app.main.settings.database_url", fake_url)

    mock_pool = MagicMock(spec=AsyncConnectionPool)
    mock_pool.closed = False
    mock_pool.open = AsyncMock()
    mock_pool.wait = AsyncMock()
    mock_pool.close = AsyncMock()

    app = create_app()

    with patch("app.database.connection.AsyncConnectionPool", return_value=mock_pool):
        with TestClient(app) as client:
            assert db_manager.is_initialized is True
            mock_pool.open.assert_awaited_once()
            mock_pool.wait.assert_awaited_once()

            resp = client.get("/health")
            assert resp.status_code == 200
            assert resp.json() == {"status": "ok", "mode": "real"}

        # On exiting TestClient context, shutdown closes the pool cleanly
        mock_pool.close.assert_awaited_once()
        assert db_manager.is_initialized is False


def test_persistent_mode_failed_pool_initialization_fails_startup(monkeypatch):
    """Scenario 5: MOCK_MODE=false with unreachable database.

    Startup must fail with an error and leave zero partially initialized resources.
    """
    fake_url = "postgresql://user:pass@unreachable.host:5432/yojana_db"
    monkeypatch.setattr("app.main.settings.mock_mode", False)
    monkeypatch.setattr("app.main.settings.database_url", fake_url)

    mock_pool = MagicMock(spec=AsyncConnectionPool)
    mock_pool.closed = False
    mock_pool.open = AsyncMock()
    mock_pool.wait = AsyncMock(side_effect=Exception("Connection refused"))
    mock_pool.close = AsyncMock()

    app = create_app()

    with patch("app.database.connection.AsyncConnectionPool", return_value=mock_pool):
        with pytest.raises(RuntimeError, match="Database connection failed: Connection refused"):
            with TestClient(app):
                pass

        # Verify pool was cleaned up and not left open
        assert db_manager.is_initialized is False
        mock_pool.close.assert_awaited_once()


def test_no_silent_fallback_when_persistent_mode_cannot_connect(monkeypatch):
    """Scenario 6: Verify no silent fallback to in-memory mode when connection fails."""
    monkeypatch.setattr("app.main.settings.mock_mode", False)
    monkeypatch.setattr("app.main.settings.database_url", "postgresql://invalid-url")

    mock_pool = MagicMock(spec=AsyncConnectionPool)
    mock_pool.open = AsyncMock()
    mock_pool.wait = AsyncMock(side_effect=Exception("TCP timeout"))
    mock_pool.close = AsyncMock()

    app = create_app()

    with patch("app.database.connection.AsyncConnectionPool", return_value=mock_pool):
        # Must raise exception; must NOT silently continue running in mock mode
        with pytest.raises(RuntimeError, match="Database connection failed: TCP timeout"):
            with TestClient(app):
                pass

    # Ensure application state was not converted to mock mode
    from app.core.config import settings
    assert settings.mock_mode is False


@pytest.mark.asyncio
async def test_get_connection_context_manager():
    """Verify get_connection context manager yields connection from active pool."""
    mock_conn = AsyncMock()
    mock_pool = MagicMock(spec=AsyncConnectionPool)
    mock_pool.closed = False

    @asynccontextmanager
    async def fake_connection():
        yield mock_conn

    mock_pool.connection = fake_connection

    manager = DatabaseManager()
    manager._pool = mock_pool

    with patch("app.database.connection.db_manager", manager):
        async with get_connection() as conn:
            assert conn is mock_conn


def test_sanitize_db_error_message_scrubs_passwords_and_urls():
    """Verify error messages scrub raw credentials and connection URLs."""
    raw_url = "postgresql://myadmin:topsecret123@db.prod.internal:5432/yojanadb"

    # Message containing password
    exc1 = Exception("Authentication failed for password topsecret123 on database")
    sanitized1 = _sanitize_db_error_message(exc1, raw_url)
    assert "topsecret123" not in sanitized1
    assert "***" in sanitized1

    # Message containing entire raw URL
    exc2 = Exception(f"Connection to {raw_url} timed out")
    sanitized2 = _sanitize_db_error_message(exc2, raw_url)
    assert raw_url not in sanitized2
    assert "topsecret123" not in sanitized2
    assert "[REDACTED_DATABASE_URL]" in sanitized2

    # Normal message
    exc3 = Exception("Connection reset by peer")
    sanitized3 = _sanitize_db_error_message(exc3, raw_url)
    assert sanitized3 == "Connection reset by peer"


def test_lifespan_closes_pool_on_application_exception(monkeypatch):
    """Verify pool is closed in finally block if an exception occurs during app lifespan."""
    fake_url = "postgresql://user:pass@localhost:5432/yojana_db"
    monkeypatch.setattr("app.main.settings.mock_mode", False)
    monkeypatch.setattr("app.main.settings.database_url", fake_url)

    mock_pool = MagicMock(spec=AsyncConnectionPool)
    mock_pool.closed = False
    mock_pool.open = AsyncMock()
    mock_pool.wait = AsyncMock()
    mock_pool.close = AsyncMock()

    app = create_app()

    with patch("app.database.connection.AsyncConnectionPool", return_value=mock_pool):
        # Lifespan enters, then an exception occurs inside the context
        with pytest.raises(ZeroDivisionError):
            with TestClient(app):
                assert db_manager.is_initialized is True
                raise ZeroDivisionError("Simulated server crash during execution")

        # Verify finally block ran close() despite the exception
        mock_pool.close.assert_awaited_once()
        assert db_manager.is_initialized is False


@pytest.mark.asyncio
async def test_pool_idempotent_close_and_reuse():
    """Verify repeated close() does not fail and re-initialization cleanly succeeds."""
    manager = DatabaseManager()
    mock_pool = MagicMock(spec=AsyncConnectionPool)
    mock_pool.closed = False
    mock_pool.open = AsyncMock()
    mock_pool.wait = AsyncMock()
    mock_pool.close = AsyncMock()

    with patch("app.database.connection.AsyncConnectionPool", return_value=mock_pool):
        # First initialization
        pool1 = await manager.initialize("postgresql://u:p@localhost/db")
        assert pool1 is mock_pool
        assert manager.is_initialized is True

        # Second initialization while active reuses existing pool without recreating
        pool2 = await manager.initialize("postgresql://u:p@localhost/db")
        assert pool2 is mock_pool
        mock_pool.open.assert_awaited_once()

        # First close
        await manager.close()
        mock_pool.close.assert_awaited_once()
        assert manager.is_initialized is False

        # Repeated close does not error
        await manager.close()
        assert manager.is_initialized is False


def test_persistent_mode_initialization_failure_sanitizes_credentials(monkeypatch):
    """Verify initialization failure does not leak password in raised exception or logs."""
    fake_url = "postgresql://user:super_secret_pw@host:5432/db"
    monkeypatch.setattr("app.main.settings.mock_mode", False)
    monkeypatch.setattr("app.main.settings.database_url", fake_url)

    mock_pool = MagicMock(spec=AsyncConnectionPool)
    mock_pool.closed = False
    mock_pool.open = AsyncMock()
    mock_pool.wait = AsyncMock(side_effect=Exception(f"Connection failed for {fake_url}"))
    mock_pool.close = AsyncMock()

    app = create_app()

    with patch("app.database.connection.AsyncConnectionPool", return_value=mock_pool):
        with pytest.raises(RuntimeError) as exc_info:
            with TestClient(app):
                pass

        err_msg = str(exc_info.value)
        # Ensure raw password and raw URL are scrubbed
        assert "super_secret_pw" not in err_msg
        assert fake_url not in err_msg
        assert "[REDACTED_DATABASE_URL]" in err_msg
        # Ensure exception chaining is suppressed to prevent traceback leakage
        assert exc_info.value.__cause__ is None
        assert exc_info.value.__suppress_context__ is True


def test_traceback_and_logger_exception_do_not_leak_credentials(monkeypatch, caplog):
    """Verify complete formatted traceback and logger.exception output do not leak credentials."""
    synthetic_user = "demo_db_user"
    synthetic_pw = "ultra_sensitive_password_9876"
    synthetic_url = f"postgresql://{synthetic_user}:{synthetic_pw}@db.secure.cloud:5432/production"

    monkeypatch.setattr("app.main.settings.mock_mode", False)
    monkeypatch.setattr("app.main.settings.database_url", synthetic_url)

    mock_pool = MagicMock(spec=AsyncConnectionPool)
    mock_pool.closed = False
    mock_pool.open = AsyncMock()
    # Driver failure containing the raw URL with embedded password
    driver_exc = Exception(f"psycopg.OperationalError: could not connect to {synthetic_url}: connection timeout")
    mock_pool.wait = AsyncMock(side_effect=driver_exc)
    mock_pool.close = AsyncMock()

    app = create_app()

    with patch("app.database.connection.AsyncConnectionPool", return_value=mock_pool):
        with caplog.at_level(logging.DEBUG):
            with pytest.raises(RuntimeError) as exc_info:
                with TestClient(app):
                    pass

        caught_err = exc_info.value

        # 1. Check str(exception)
        err_str = str(caught_err)
        assert synthetic_pw not in err_str
        assert synthetic_url not in err_str

        # 2. Check exception.__cause__ and exception.__context__
        assert caught_err.__cause__ is None
        assert caught_err.__context__ is None
        assert caught_err.__suppress_context__ is True

        # 3. Check traceback.format_exception(...)
        tb_lines = traceback.format_exception(caught_err)
        formatted_tb = "".join(tb_lines)
        assert synthetic_pw not in formatted_tb
        assert synthetic_url not in formatted_tb

        # 4. Check logger.exception simulation
        simulated_logger = logging.getLogger("startup_crash_reporter")
        try:
            raise caught_err
        except Exception:
            simulated_logger.exception("Startup crashed during lifespan")

        # 5. Check captured log output
        all_logs = caplog.text
        assert synthetic_pw not in all_logs
        assert synthetic_url not in all_logs
        # Masked URL is permissible in info/error logs, but raw password must NEVER appear
        assert f"{synthetic_user}:***@db.secure.cloud:5432/production" in all_logs


def test_exception_context_and_traceback_locals_scrubbed_clean(monkeypatch):
    """Verify __context__ is None and initialization traceback frame locals contain no secrets."""
    synthetic_user = "sec_test_user"
    synthetic_pw = "super_classified_pw_4321"
    synthetic_url = f"postgresql://{synthetic_user}:{synthetic_pw}@cluster.db.internal:5432/secure_app"

    monkeypatch.setattr("app.main.settings.mock_mode", False)
    monkeypatch.setattr("app.main.settings.database_url", synthetic_url)

    mock_pool = MagicMock(spec=AsyncConnectionPool)
    mock_pool.closed = False
    mock_pool.open = AsyncMock()
    mock_pool.wait = AsyncMock(
        side_effect=Exception(f"FATAL: auth failed for {synthetic_url}: invalid credentials")
    )
    mock_pool.close = AsyncMock()

    app = create_app()

    with patch("app.database.connection.AsyncConnectionPool", return_value=mock_pool):
        with pytest.raises(RuntimeError) as exc_info:
            with TestClient(app):
                pass

        err = exc_info.value

        # 1. str(exception) is sanitized
        assert synthetic_pw not in str(err)
        assert synthetic_url not in str(err)
        assert "[REDACTED_DATABASE_URL]" in str(err)

        # 2. Exception context and cause are explicitly suppressed and cleared
        assert err.__cause__ is None
        assert err.__context__ is None
        assert err.__suppress_context__ is True

        # 3. TracebackException inspects frame locals across the stack
        tb_exc = traceback.TracebackException.from_exception(err, capture_locals=True)
        for frame in tb_exc.stack:
            if frame.name in ("initialize", "init_db"):
                locs = frame.locals or {}
                for k, v in locs.items():
                    assert synthetic_pw not in str(v), f"Credential leaked in frame {frame.name}, var {k}"
                    assert synthetic_url not in str(v), f"Raw URL leaked in frame {frame.name}, var {k}"
