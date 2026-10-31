"""Native PostgreSQL SQL migration runner with transaction-scoped advisory locking."""
from __future__ import annotations

import asyncio
import hashlib
import logging
import sys
from pathlib import Path
from typing import Sequence

import psycopg

from app.core.config import settings
from app.database.connection import _mask_db_url, _sanitize_db_error_message

logger = logging.getLogger(__name__)

# Documented 64-bit application constant for migration advisory locking
MIGRATION_ADVISORY_LOCK_ID: int = 7182930415263748

# Default migrations directory relative to repository layout
DEFAULT_MIGRATIONS_DIR: Path = Path(__file__).resolve().parents[2] / "migrations"

SCHEMA_MIGRATIONS_DDL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(32) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def compute_checksum(content: str) -> str:
    """Compute deterministic SHA-256 hex digest for SQL migration content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def discover_migration_files(migrations_dir: Path) -> list[Path]:
    """Discover SQL migration files in deterministic alphabetical order."""
    if not migrations_dir.exists() or not migrations_dir.is_dir():
        logger.warning("Migrations directory does not exist: %s", migrations_dir)
        return []
    return sorted(migrations_dir.glob("*.sql"), key=lambda p: p.name)


async def run_migrations(
    database_url: str | None = None,
    migrations_dir: Path | None = None,
) -> list[str]:
    """Execute pending SQL migrations inside a single locked transaction.

    Returns the list of newly applied migration versions.
    """
    # Verify execution environment rules
    if settings.mock_mode:
        raise RuntimeError(
            "Migrations cannot run in MOCK_MODE. "
            "Set MOCK_MODE=false and provide DATABASE_URL to apply migrations."
        )

    db_url = database_url or settings.database_url
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL must be configured to run migrations."
        )

    target_dir = migrations_dir or DEFAULT_MIGRATIONS_DIR
    masked_url = _mask_db_url(db_url)
    logger.info("Starting database migration preflight (%s)", masked_url)

    migration_files = discover_migration_files(target_dir)
    if not migration_files:
        logger.info("No migration files found in %s", target_dir)
        return []

    newly_applied: list[str] = []
    error_msg: str | None = None

    conn: psycopg.AsyncConnection | None = None
    try:
        conn = await psycopg.AsyncConnection.connect(db_url, autocommit=False)
        async with conn.transaction():
            async with conn.cursor() as cur:
                # 1. Acquire transaction-scoped advisory lock (released on commit/rollback)
                logger.debug("Acquiring transaction-scoped advisory lock (%s)", MIGRATION_ADVISORY_LOCK_ID)
                await cur.execute(
                    "SELECT pg_advisory_xact_lock(%s);",
                    (MIGRATION_ADVISORY_LOCK_ID,),
                )

                # 2. Ensure schema_migrations table exists
                await cur.execute(SCHEMA_MIGRATIONS_DDL)

                # 3. Read previously applied migrations
                await cur.execute("SELECT version, checksum FROM schema_migrations ORDER BY version ASC;")
                rows = await cur.fetchall()
                applied_map = {row[0]: row[1] for row in rows}

                # Check for unknown recorded versions in the database
                discovered_versions = {sql_file.name.split("_")[0] for sql_file in migration_files}
                unknown_versions = set(applied_map.keys()) - discovered_versions
                if unknown_versions:
                    logger.warning(
                        "Database contains recorded migration version(s) not found on disk: %s",
                        sorted(unknown_versions),
                    )

                # 4. Process discovered migration files in order
                for sql_file in migration_files:
                    version = sql_file.name.split("_")[0]
                    content = sql_file.read_text(encoding="utf-8")
                    checksum = compute_checksum(content)

                    if version in applied_map:
                        recorded_checksum = applied_map[version]
                        if recorded_checksum != checksum:
                            raise RuntimeError(
                                f"Checksum mismatch for migration {sql_file.name} (version {version}): "
                                f"recorded {recorded_checksum}, current {checksum}. "
                                "Halting migration runner to prevent drift."
                            )
                        logger.debug("Migration %s already applied with matching checksum.", sql_file.name)
                        continue

                    # Execute pending migration
                    logger.info("Applying migration %s (version %s)...", sql_file.name, version)
                    await cur.execute(content)

                    # Record application in schema_migrations
                    await cur.execute(
                        "INSERT INTO schema_migrations (version, name, checksum) VALUES (%s, %s, %s);",
                        (version, sql_file.stem, checksum),
                    )
                    newly_applied.append(version)
                    logger.info("Successfully applied migration %s.", sql_file.name)

        logger.info(
            "Database migrations completed successfully. %d new migration(s) applied.",
            len(newly_applied),
        )
    except Exception as exc:
        error_msg = _sanitize_db_error_message(exc, db_url)
        logger.error("Database migration failed: %s", error_msg)
        del exc
    finally:
        if conn is not None and not conn.closed:
            try:
                await conn.close()
            except Exception:
                pass
            del conn
        del db_url

    if error_msg is not None:
        err = RuntimeError(f"Migration execution failed: {error_msg}")
        err.__cause__ = None
        err.__context__ = None
        err.__suppress_context__ = True
        raise err

    return newly_applied


def cli() -> None:
    """CLI entrypoint for standalone deployment-time migration execution."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger.info("Yojana Mitra CLI: executing database migrations...")

    try:
        applied = asyncio.run(run_migrations())
        logger.info("Migration CLI finished successfully: applied %s", applied)
        sys.exit(0)
    except Exception as exc:
        logger.critical("Migration CLI execution failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    cli()

