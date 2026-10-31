-- 001_create_core_persistence.sql
-- Yojana Mitra: Core Conversation Persistence (Scope A)
-- Creates schema_migrations, sessions, and conversation_turns tables.

-- 1. Schema Migrations Bookkeeping Table
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(32) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Sessions Table
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    language VARCHAR(10) NOT NULL,
    mode VARCHAR(16) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    version INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT chk_sessions_status CHECK (status IN ('active', 'completed')),
    CONSTRAINT chk_sessions_language CHECK (language IN ('hi', 'en')),
    CONSTRAINT chk_sessions_mode CHECK (mode IN ('voice', 'text', 'combined')),
    CONSTRAINT chk_sessions_version CHECK (version >= 1)
);

CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at DESC);

-- 3. Conversation Turns Table
-- Note: No ON DELETE CASCADE, no JSONB metadata, no raw audio, no PII.
CREATE TABLE IF NOT EXISTS conversation_turns (
    turn_id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL REFERENCES sessions(session_id),
    turn_index INTEGER NOT NULL,
    role VARCHAR(16) NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_session_turn_index UNIQUE (session_id, turn_index),
    CONSTRAINT chk_turn_role CHECK (role IN ('user', 'assistant')),
    CONSTRAINT chk_turn_index CHECK (turn_index >= 0)
);

CREATE INDEX IF NOT EXISTS idx_conversation_turns_session_id ON conversation_turns(session_id, turn_index ASC);

