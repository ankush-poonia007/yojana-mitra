"""PostgreSQL asynchronous connection pooling and lifecycle management."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator
from urllib.parse import unquote, urlparse

from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


def _mask_db_url(url: str | None) -> str:
    """Return a masked database URL safe for logging without exposing credentials."""
    if not url:
        return "[NOT SET]"
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not (parsed.hostname or parsed.netloc):
            return "[CONFIGURED]"
        netloc = parsed.hostname or ""
        if parsed.port:
            netloc += f":{parsed.port}"
        if parsed.username:
            netloc = f"{parsed.username}:***@{netloc}"
        elif parsed.password:
            netloc = f":***@{netloc}"
        return f"{parsed.scheme}://{netloc}{parsed.path}"
    except Exception:
        return "[CONFIGURED]"


def _sanitize_db_error_message(exc: Exception, raw_url: str | None = None) -> str:
    """Sanitize exception messages to prevent credentials or connection URLs from leaking."""
    msg = str(exc) or type(exc).__name__
    if not raw_url:
        return msg
    try:
        parsed = urlparse(raw_url)
        # 1. Replace entire raw_url if present
        if raw_url in msg:
            msg = msg.replace(raw_url, "[REDACTED_DATABASE_URL]")

        # 2. Replace base URL (without query params)
        if parsed.scheme and parsed.netloc:
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if base_url in msg:
                msg = msg.replace(base_url, "[REDACTED_DATABASE_URL]")

        # 3. Scrub passwords (raw and unquoted)
        if parsed.password:
            msg = msg.replace(parsed.password, "***")
            unquoted = unquote(parsed.password)
            if unquoted and unquoted != parsed.password:
                msg = msg.replace(unquoted, "***")
        if parsed.netloc and "@" in parsed.netloc:
            userinfo = parsed.netloc.split("@")[0]
            if ":" in userinfo:
                pw_part = userinfo.split(":", 1)[1]
                if pw_part:
                    msg = msg.replace(pw_part, "***")

        # 4. Scrub masked URL if present in error message
        masked = _mask_db_url(raw_url)
        if masked not in ("[NOT SET]", "[CONFIGURED]") and masked in msg:
            msg = msg.replace(masked, "[REDACTED_DATABASE_URL]")
    except Exception:
        if raw_url in msg:
            msg = msg.replace(raw_url, "[REDACTED_DATABASE_URL]")
    return msg


class DatabaseManager:
    """Manages the application-wide AsyncConnectionPool lifecycle."""

    def __init__(self) -> None:
        self._pool: AsyncConnectionPool | None = None

    @property
    def is_initialized(self) -> bool:
        """Return True if connection pool is open and active."""
        return self._pool is not None and not self._pool.closed

    async def initialize(
        self,
        database_url: str,
        min_size: int = 1,
        max_size: int = 10,
        timeout: float = 10.0,
    ) -> AsyncConnectionPool:
        """Initialize and open the asynchronous connection pool.

        Verifies connectivity by waiting for readiness. If connection fails,
        resources are cleanly released and a RuntimeError is raised.
        """
        if self._pool is not None:
            if not self._pool.closed:
                logger.warning("Database pool is already initialized. Reusing existing pool.")
                return self._pool
            self._pool = None

        masked_url = _mask_db_url(database_url)
        logger.info("Initializing PostgreSQL connection pool (%s)", masked_url)

        pool = AsyncConnectionPool(
            conninfo=database_url,
            min_size=min_size,
            max_size=max_size,
            open=False,
        )

        init_error_msg: str | None = None
        try:
            await pool.open()
            # Wait for readiness to verify database is reachable
            await pool.wait(timeout=timeout)
            self._pool = pool
            logger.info("PostgreSQL connection pool initialized and verified successfully.")
            return self._pool
        except Exception as exc:
            init_error_msg = _sanitize_db_error_message(exc, database_url)
            logger.error("Failed to initialize database connection pool (%s): %s", masked_url, init_error_msg)
            # Ensure no partially initialized resources remain
            try:
                await pool.close()
            except Exception:
                pass
            self._pool = None
            del exc
        finally:
            # Scrub credential-bearing objects from local frame
            del pool
            del database_url

        if init_error_msg is not None:
            err = RuntimeError(f"Database connection failed: {init_error_msg}")
            err.__cause__ = None
            err.__context__ = None
            err.__suppress_context__ = True
            raise err

    async def close(self) -> None:
        """Cleanly close the asynchronous connection pool and release resources."""
        if self._pool is not None:
            logger.info("Closing PostgreSQL connection pool.")
            try:
                if not self._pool.closed:
                    await self._pool.close()
            except Exception as exc:
                logger.warning("Error while closing database pool: %s", exc)
            finally:
                self._pool = None

    def get_pool(self) -> AsyncConnectionPool:
        """Retrieve the active AsyncConnectionPool instance.

        Raises RuntimeError if pool is not initialized.
        """
        if not self.is_initialized:
            raise RuntimeError(
                "Database connection pool is not initialized. "
                "Ensure MOCK_MODE=false and DATABASE_URL is configured."
            )
        assert self._pool is not None
        return self._pool

    async def check_health(self) -> bool:
        """Verify active database connectivity by executing a lightweight query."""
        if not self.is_initialized:
            return False
        try:
            async with self.get_pool().connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT 1;")
                    result = await cur.fetchone()
                    return result is not None and result[0] == 1
        except Exception as exc:
            logger.warning("Database health check failed: %s", exc)
            return False


db_manager = DatabaseManager()


async def init_db(database_url: str) -> AsyncConnectionPool:
    """Helper to initialize the database manager with a database URL."""
    try:
        return await db_manager.initialize(database_url)
    finally:
        del database_url


async def close_db() -> None:
    """Helper to close the database manager."""
    await db_manager.close()


def get_db_pool() -> AsyncConnectionPool:
    """Helper to retrieve the active AsyncConnectionPool instance."""
    return db_manager.get_pool()


@asynccontextmanager
async def get_connection() -> AsyncIterator[AsyncConnection]:
    """Context manager yielding an AsyncConnection from the active pool."""
    pool = get_db_pool()
    async with pool.connection() as conn:
        yield conn

