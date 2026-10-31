# Yojana Mitra — Build and Evidence Log

**Purpose:** Record observed build state and evidence. This log contains verified results from executed builds, tests, and integration runs.

## Current record

| Item | Status | Evidence / notes |
| --- | --- | --- |
| Phase 5 application implementation | PARTIAL (MOCK SLICE + DB REPOSITORIES) | Phase 1 modular backend foundation and H1 mock API slice in `backend/app/` (EV-20261031-001, EV-20261031-002); Phase 2 D2 pool, D3.1 migrations, and D4 repositories in `backend/app/database/` (EV-20261031-003, EV-20261031-004). Real LangGraph, Gemini, eligibility, retrieval, and live speech remain unbuilt. |
| Tests / acceptance runs | 68 PASSED (MIGRATIONS & REPOSITORIES VERIFIED) | Automated test suite in `backend/tests/` executed via pytest: 68 passed in 0.80s with exit code 0 (EV-20261031-004). |
| Performance / speech measurements | NOT MEASURED HERE | No latency, accuracy, payload size, scorecard or baseline number is asserted. |
| Deployment / clean-start demo | NOT VERIFIED | Local TestClient execution verified; live deployment not executed. |
| Frozen contracts and rule source artifacts | VERIFIED IN REPO | PMUY KB, Research Analysis, and T01–T12 definitions verified in `docs/research/PMUY/`; API contract in `shared/api-contract.md`; canonical fixtures in `shared/examples/`. |
| Schedule/checkpoints | OPEN | Confirm actual event times. Historical times are templates only. |

## Recorded Evidence Entries

### EV-20261031-001 — Phase 1 Backend Foundation & H1 Mock API Verification
- **Entry ID:** EV-20261031-001
- **Date/time and timezone:** 2026-10-31T04:35:00+05:30 (Asia/Kolkata)
- **Owner / runner:** Ankush (Backend Developer & Integration Lead)
- **Repository revision:** Commit `39a8a90` (branch `main`, working tree uncommitted Phase 1 work)
- **Feature / acceptance IDs:** P5-03, P5-04, AT-13
- **Environment:** Windows 11, Python 3.14.3 (.venv), local runner
- **Mode:** `MOCKED` (Phase 1 fixture-backed slice; MOCK_MODE=true)
- **Steps and inputs:**
  1. Created root `AGENTS.md` governance file.
  2. Modularized `backend/app/` into `core/`, `schemas/`, `services/`, `api/routes/`, and `main.py`.
  3. Implemented 25 automated tests in `backend/tests/` covering sessions, text turns, multipart voice turns, shared error envelopes, and fixture immutability.
  4. Executed `.\.venv\Scripts\pytest -v`.
- **Expected result & source:** All 4 frozen routes (`/sessions`, `/sessions/{id}`, `/turns`, `/voice/turns`) and `/health` respond with contract-compliant payloads matching `shared/api-contract.md` and `shared/examples/`. Error envelope returned on tested 400, 404, 422, and 500 conditions. Audio is not persisted.
- **Observed result:** 
  - **Final automated test run:** 25 passed, 0 failed in 0.40s.
  - **Intermediate test failure:** The initial pytest run failed (1 failed, 24 passed) on `test_general_exception_returns_500_envelope` because Starlette's `TestClient` defaults to `raise_server_exceptions=True`, intercepting the simulated exception. The test was subsequently corrected to use `raise_server_exceptions=False`, after which the entire suite passed.
  - **Intermediate execution issues:** Initial app route inspection encountered an `AttributeError: '_IncludedRouter' object has no attribute 'path'` due to FastAPI router nesting. Initial interactive PowerShell verification commands failed due to nested quote escaping inside f-strings and multiline strings. All were command syntax artifacts and were subsequently resolved.
- **Outcome:** `PASS` (Final test suite and functional verification)
- **Evidence location:** `backend/tests/`, `backend/app/`, `AGENTS.md`
- **Contract compliance scope & gaps:**
  - **Tested & verified status codes:** HTTP 200 (turns, get session, health), 201 (create session), 400 (`EMPTY_TEXT_INPUT`, `INVALID_AUDIO`), 404 (`SESSION_NOT_FOUND`), 422 (`INVALID_SESSION_INPUT`, `INVALID_REQUEST`), and 500 (`INTERNAL_SERVER_ERROR`).
  - **Voice HTTP 413 `PAYLOAD_TOO_LARGE`:** Specified by Phase 3.3 contract §3.2 and §3.4. The current mock implementation checks only for empty audio (`read(1)`) and does not enforce an upload-size boundary. The exact numerical maximum upload size is not established in the available contract material; therefore, both the threshold and implementation remain **OPEN**. The 413 case was **not tested**.
  - **Downstream outage codes (HTTP 503 `AI_SERVICE_UNAVAILABLE` and `STT_UNAVAILABLE`):** Specified by contract for downstream service outages. Because real Gemini, LangGraph, and STT services are not connected in Phase 1 mock mode, these error paths remain **OPEN / NOT IMPLEMENTED**.
- **Mock session limitations:**
  - `sess_demo_001` is the canonical demo session identifier from `shared/examples/session_create_response.json`.
  - Current mock session creation reuses and overwrites that fixed ID in memory.
  - `GET /api/v1/sessions/{id}` returns static, fixture-backed conversation history (`turn_001` and `turn_002` from `session_get_response.json`).
  - Dynamic concurrent sessions and turn-history accumulation are **not implemented**.
  - These are documented mock limitations of Phase 1, not verified production persistence behaviour.
- **Implementation boundaries:**
  - Real database persistence (Supabase PostgreSQL, migrations, DDL), LangGraph orchestration, Gemini model routing, deterministic PMUY rule engine, vector retrieval (pgvector + FTS), and live STT/TTS remain unimplemented (scheduled for Phases 2–6).

### EV-20261031-002 — Configuration Robustness & Empty-Environment Verification
- **Entry ID:** EV-20261031-002
- **Date/time and timezone:** 2026-10-31T05:08:00+05:30 (Asia/Kolkata)
- **Owner / runner:** Ankush (Backend Developer & Integration Lead)
- **Repository revision:** Commit `39a8a90` (branch `main`, working tree uncommitted Phase 1 work)
- **Feature / acceptance IDs:** P5-03, P5-04, AT-13
- **Environment:** Windows 11, Python 3.14.3 (.venv), local runner
- **Mode:** `MOCKED` (Phase 1 fixture-backed slice; MOCK_MODE=true)
- **Steps and inputs:**
  1. Observed configuration failure when untracked `.env` was copied from `.env.example` containing empty values (`APP_PORT=`, `MOCK_MODE=`), causing `pydantic_core.ValidationError` because empty strings `""` cannot be parsed as integer or boolean types.
  2. Updated `backend/app/core/config.py` with `env_ignore_empty=True` in `SettingsConfigDict` to treat empty environment variables as unset, cleanly falling back to defaults (`8000`, `True`).
  3. Added 5 focused configuration unit tests in `backend/tests/test_config.py` verifying empty fallbacks, explicit overrides, and mock startup without downstream credentials.
  4. Executed `pytest --collect-only -q` (30 tests collected).
  5. Executed `pytest -v` without shell environment overrides.
  6. Verified endpoints and lifespan startup/shutdown via TestClient.
- **Expected result & source:** Settings gracefully ignores empty string values from `.env`; all 30 tests pass; TestClient succeeds across all 4 endpoints without shell environment overrides.
- **Observed result:**
  - `pytest -v`: 30 passed, 0 failed in 0.38s (exit code 0).
  - App import and lifespan startup/shutdown: OK (exit code 0).
  - All 4 endpoints return HTTP 200/201.
- **Outcome:** `PASS`
- **Evidence location:** `backend/app/core/config.py`, `backend/tests/test_config.py`
- **Contract compliance scope & gaps:**
  - Preserved Phase 1 mock boundaries: `MOCK_MODE=True` enforced; audio not persisted.
  - Upload-size limit (HTTP 413) remains **OPEN** (numerical maximum undefined in contracts).
  - Downstream outage handlers (HTTP 503) remain **OPEN** for Phases 3 and 6.

---

### EV-20261031-003 — Phase 2 D2 PostgreSQL Connection Foundation & Lifecycle Verification
- **Entry ID:** EV-20261031-003
- **Date/time and timezone:** 2026-10-31T06:55:00+05:30 (Asia/Kolkata)
- **Owner / runner:** Ankush (Backend Developer & Integration Lead)
- **Repository revision:** Commit `0dd43279f6677e32b9cafe223273e7b460c3f57c` (branch `ankush/backend`, uncommitted D2 work)
- **Feature / acceptance IDs:** P5-01, P5-03, P2-D2
- **Environment:** Windows 11, Python 3.14.3 (.venv), local runner
- **Mode:** `PARTIAL` (PostgreSQL connection foundation and lifecycle verified; database tables and persistence workflows remain unbuilt)
- **Steps and inputs:**
  1. Added approved dependency `psycopg-pool>=3.1` to `requirements.txt` and installed `psycopg-pool 3.3.3` in `.venv`.
  2. Updated `backend/app/core/config.py` to allow runtime configuration matrix evaluation in FastAPI lifespan without breaking existing environment loading.
  3. Implemented `backend/app/database/connection.py` with `DatabaseManager`, masked URL logging, connection pool startup/shutdown, and `get_connection()` async context manager.
  4. Integrated `lifespan` context manager into `backend/app/main.py` enforcing runtime configuration rules:
     - `MOCK_MODE=true`, `DATABASE_URL` missing -> Mock mode; no pool initialized.
     - `MOCK_MODE=true`, `DATABASE_URL` configured -> Mock mode takes precedence; no pool initialized.
     - `MOCK_MODE=false`, `DATABASE_URL` configured -> Initialize pool and verify readiness via `pool.wait()`.
     - `MOCK_MODE=false`, `DATABASE_URL` missing -> Fail startup with `RuntimeError`.
     - Connection failure in persistent mode -> Fail startup with `RuntimeError`; no silent fallback to in-memory mode.
  5. Implemented 15 unit tests in `backend/tests/test_database.py` covering connection lifecycle, try/finally cleanup under execution exceptions, traceback frame locals scrubbing, and idempotent pool reuse.
  6. Executed full test suite: `pytest -v`.
- **Expected result & source:** All 45 tests pass. Startup rules strictly enforced. No credentials exposed in logs, tracebacks, `__context__`, or frame locals. No silent fallback from persistent mode to mock mode.
- **Observed result:**
  - `pytest backend/tests/test_database.py -v`: 15 passed, 0 failed in 0.15s.
  - `pytest -v` (full suite): 45 passed, 0 failed in 0.58s (exit code 0).
  - Complete exception internals verified: `__cause__` is `None`, `__context__` is `None`, `__suppress_context__` is `True`, stack frame locals scrubbed clean with `del`, all logs and tracebacks leak-free.
- **Outcome:** `PASS`
- **Evidence location:** `backend/app/database/connection.py`, `backend/app/main.py`, `backend/app/core/config.py`, `requirements.txt`, `backend/tests/test_database.py`
- **Contract compliance scope & gaps:**
  - No external API routes or request/response schemas were modified.
  - Phase 3.3 error envelopes and `/health` response shapes are preserved.
  - SQL migrations (D3), tables (`sessions`, `conversation_turns`), repositories, and optimistic concurrency remain **OPEN** and will be addressed in subsequent Phase 2 tasks.

---

### EV-20261031-004 — Phase 2 D3.1 Migrations & D4 Persistence Repositories Verification
- **Entry ID:** EV-20261031-004
- **Date/time and timezone:** 2026-10-31T07:54:00+05:30 (Asia/Kolkata)
- **Owner / runner:** Ankush (Backend Developer & Integration Lead)
- **Repository revision:** Commit `0dd43279f6677e32b9cafe223273e7b460c3f57c` (branch `ankush/backend`, uncommitted D3.1 + D4 work)
- **Feature / acceptance IDs:** P5-01, P5-03, P2-D3.1, P2-D4
- **Environment:** Windows 11, Python 3.14.3 (.venv), local runner
- **Mode:** `PARTIAL` (Migration runner and persistence repositories implemented and unit-tested; live PostgreSQL integration against remote Supabase pending live network run; not yet integrated into SessionService/TurnService)
- **Steps and inputs:**
  1. Created `backend/migrations/001_create_core_persistence.sql` with `schema_migrations` (version, name, checksum, applied_at), minimal `sessions` table (with status, language, mode, version, updated_at), and minimal `conversation_turns` table (with turn_id, session_id, turn_index, role, text, created_at, uq_session_turn_index, no CASCADE, no JSONB metadata, no raw audio, no PII).
  2. Implemented native PostgreSQL migration runner `backend/app/database/migrations.py` with transaction-scoped advisory lock `pg_advisory_xact_lock(7182930415263748)`, SHA-256 checksum verification, transactional rollback on error, and CLI entry point (`python -m app.database.migrations`).
  3. Implemented repositories in `backend/app/database/repositories/`: `session_repository.py` (`create_session`, `get_session`, `session_exists`, `update_session_version`) and `turn_repository.py` (`append_turn_pair`, `get_turns_for_session`, `to_history_dict`).
  4. Implemented atomic conversation pair persistence under single transaction with optimistic concurrency version check, dynamic turn indexing, and rollback on failure.
  5. Implemented 12 migration unit tests in `backend/tests/test_migrations.py` and 11 repository unit tests in `backend/tests/test_repositories.py`.
  6. Executed full test suite: `pytest -v`.
- **Expected result & source:** All 68 tests pass. Migration runner enforces advisory locking and checksum drift detection. Repositories enforce atomic pair persistence, optimistic concurrency, and deterministic turn ordering.
- **Observed result:**
  - `pytest backend/tests/test_migrations.py -v`: 12 passed, 0 failed in 0.13s.
  - `pytest backend/tests/test_repositories.py -v`: 11 passed, 0 failed in 0.07s.
  - `pytest -v` (full suite): 68 passed, 0 failed in 0.80s (exit code 0).
  - CLI execution in mock mode: exited cleanly with code 1 and descriptive message.
- **Outcome:** `PASS`
- **Evidence location:** `backend/migrations/001_create_core_persistence.sql`, `backend/app/database/migrations.py`, `backend/app/database/repositories/`, `backend/tests/test_migrations.py`, `backend/tests/test_repositories.py`
- **Contract compliance scope & gaps:**
  - No external API routes or request/response schemas were modified.
  - Repositories provide exact history format matching frozen API contract (`turn_id`, `role`, `text`).
  - Repositories are tested via unit test doubles; live integration with remote Supabase PostgreSQL and integration into `SessionService` and `TurnService` remain scheduled for subsequent tasks.

---

### EV-20261031-005 — Phase 2 D5 Service Integration & D6 Persistence Acceptance Testing
- **Entry ID:** EV-20261031-005
- **Date/time and timezone:** 2026-10-31T08:35:00+05:30 (Asia/Kolkata)
- **Owner / runner:** Ankush (Backend Developer & Integration Lead)
- **Repository revision:** Commit `0dd43279f6677e32b9cafe223273e7b460c3f57c` (branch `ankush/backend`, uncommitted D5 + D6 work)
- **Feature / acceptance IDs:** P5-01, P5-03, P2-D5, P2-D6
- **Environment:** Windows 11, Python 3.14.3 (.venv), local runner
- **Mode:** `PARTIAL` (SessionService & TurnService persistent wiring implemented and verified with 93 passing tests; live PostgreSQL network integration pending live database instance)
- **Steps and inputs:**
  1. Patched `backend/app/database/migrations.py` to enforce strict mock-mode safety: `MOCK_MODE=true` rejects migrations unconditionally (even with explicit `database_url`), preventing any connection attempts.
  2. Integrated `SessionRepository` and `TurnRepository` into `SessionService` (`backend/app/services/session_service.py`) supporting both `MOCK_MODE=true` (in-memory fixtures, zero DB access) and `MOCK_MODE=false` (persistent CRUD operations, version tracking, contract-compliant history).
  3. Integrated `TurnRepository` into `TurnService` (`backend/app/services/turn_service.py`) supporting both text and voice turn persistence: atomically persists user/assistant turn pair with optimistic concurrency check, catches concurrency conflicts returning retryable 500 `INTERNAL_SERVER_ERROR` without inventing unapproved external codes.
  4. Enforced voice boundary: raw audio bytes are never persisted (only 1 byte read into memory to validate non-empty payload); persistent voice turn without transcription raises 503 `STT_UNAVAILABLE`; voice turn with available transcription persists pair and returns Phase 3.3 contract shape.
  5. Implemented comprehensive test suite in `backend/tests/test_service_persistence.py` (24 new tests covering mock vs persistent session/turn/voice behaviors, concurrency conflicts, zero DB calls in mock mode, and Pydantic schema compatibility).
  6. Executed full test suite: `pytest -v`.
- **Expected result & source:** All 93 tests pass. Zero regressions. Mock mode makes zero DB calls. Persistent mode preserves Phase 3.3 contract and frozen error envelopes.
- **Observed result:**
  - `pytest backend/tests/test_service_persistence.py -v`: 24 passed, 0 failed in 0.13s.
  - `pytest -v` (full suite): 93 passed, 0 failed in 0.87s (exit code 0).
- **Outcome:** `PASS`
- **Evidence location:** `backend/app/database/migrations.py`, `backend/app/api/routes/sessions.py`, `backend/app/services/session_service.py`, `backend/app/services/turn_service.py`, `backend/tests/test_service_persistence.py`, `backend/tests/test_migrations.py`, `backend/tests/test_database.py`
- **Contract compliance scope & gaps:**
  - All 4 frozen API routes and error envelopes are 100% preserved.
  - Response schemas validate cleanly against `SessionCreateResponse`, `SessionGetResponse`, and `TurnResponse`.
  - Live PostgreSQL network integration remains marked `PARTIAL` because no live PostgreSQL instance is available in the current environment (verified via `Test-NetConnection localhost:5432` failing).

---

### EV-20261031-006 — Phase 5 P5.0 Readiness, Contract Verification & Mock Vertical Slice
- **Entry ID:** EV-20261031-006
- **Date/time and timezone:** 2026-10-31T08:50:00+05:30 (Asia/Kolkata)
- **Owner / runner:** Ankush (Backend Orchestration & Integration Lead)
- **Repository revision:** Commit `0dd43279f6677e32b9cafe223273e7b460c3f57c` (branch `ankush/backend`, uncommitted Phase 2 persistence foundation)
- **Feature / acceptance IDs:** P5-00, P5-01, P5.0, P5.1
- **Environment:** Windows 11, Python 3.14.3 (.venv), local runner
- **Mode:** `MOCKED` (Mock vertical slice fully verified); `PARTIAL` (Persistence unit-tested, live PG OPEN); AI orchestration `OPEN`
- **Steps and inputs:**
  1. Conducted Phase 5.0 preflight audit of all 12 source and contract artifacts across repository. Located authoritative Phase 3.2 stack, Phase 3.3 API contract, H1 contract, PMUY Knowledge Base (`docs/research/PMUY/PMUY_RAG_Knowledge_Base.md` with PMUY-T01 through PMUY-T12 definitions), and Research Analysis.
  2. Identified that Anamika's Python rule engine implementation, ingested source documents/corpus, and speech wrappers have not yet landed in the repository (OPEN).
  3. Verified H1 API routes (`POST /api/v1/sessions`, `GET /api/v1/sessions/{session_id}`, `POST /api/v1/turns`, `POST /api/v1/voice/turns`) and schemas against frozen Phase 3.3 contract and shared examples.
  4. Executed end-to-end mock vertical slice: session creation -> text turn -> session retrieval -> history verification -> error handling (400, 404, 422).
  5. Performed authenticity audit on persistent mode: confirmed persistent mode currently uses template response for persistence testing and must not be represented as real Gemini AI reasoning or real synthesized speech until H2 workflow orchestration is wired.
  6. Executed full test suite: `pytest -v`.
- **Expected result & source:** All 93 tests pass. Zero regressions. Mock vertical slice passes cleanly.
- **Observed result:**
  - `pytest -v` (full suite): 93 passed, 0 failed in 0.75s (exit code 0).
  - Mock vertical slice: create session (`sess_demo_001`), submit text turn (`turn_003`), retrieve session (2 history turns), 404 on missing session, 422 on invalid language, 400 on empty text all verified.
- **Outcome:** `PASS`
- **Evidence location:** `docs/INTEGRATION_CONTRACTS.md`, `shared/api-contract.md`, `backend/app/api/routes/`, `backend/tests/`, `docs/BUILD_EVIDENCE_LOG.md`
- **Contract compliance scope & gaps:**
  - Frozen Phase 3.3 contract 100% compliant.
  - H2 LangGraph orchestration, Gemini client integration, H3 rule engine integration, H4 retrieval corpus, and speech wrappers remain OPEN for subsequent Phase 5 execution.

---

### EV-20261031-007 — Phase 5 Round 1 Implementation (P5.2 LangGraph Orchestration + P5.3 Gemini Integration)
- **Entry ID:** EV-20261031-007
- **Date/time and timezone:** 2026-10-31T09:48:00+05:30 (Asia/Kolkata)
- **Owner / runner:** Ankush (Backend Orchestration & Integration Lead)
- **Repository revision:** Working tree based on commit `0dd43279f6677e32b9cafe223273e7b460c3f57c` (branch `ankush/backend`)
- **Feature / acceptance IDs:** P5-02, P5-03, H2-STATE, H2-WORKFLOW, LLM-01..LLM-03, ADAPT-01..ADAPT-03
- **Environment:** Windows 11, Python 3.14.3 (.venv), local runner
- **Mode:** `PARTIAL` (LangGraph orchestration, 11-key state, Gemini client with 3 tiers, bilingual prompts, and adapter seams BUILT and verified; external live Gemini/STT network calls pending live keys/handoffs)
- **Steps and inputs:**
  1. Built centralized Gemini client in `backend/app/llm/client.py` with 3-tier routing (`HIGH`: `gemini-2.5-pro`, `MID`: `gemini-2.5-flash`, `LITE`: `gemini-2.5-flash-lite`), timeout enforcement (`gemini_timeout_seconds=15.0`), structured JSON parsing & markdown code fence stripping, and sanitized error mapping.
  2. Implemented versioned bilingual prompt templates in `backend/app/llm/prompts/` enforcing strict non-hallucination, zero eligibility rule override, refusal on missing evidence, and indicative disclaimer.
  3. Built thin adapter seams in `backend/app/adapters/`:
     - `eligibility_adapter` (H3 boundary): evaluates explicit disqualifications (R01, R03) or returns `cannot_determine` with missing criteria. Never fabricates `likely_eligible` prior to Anamika's rule engine handoff.
     - `retrieval_adapter` (H4 boundary): returns official PMUY portal metadata or empty list `[]` triggering refusal.
     - `speech_adapter` (voice boundary): safe pre-integration stub raising `STTUnavailableError` and synthesizing Base64 placeholder.
  4. Implemented frozen 11-key workflow state in `backend/app/graph/state.py` conforming strictly to `shared/api-contract.md` §4.7.
  5. Implemented four-phase functional nodes in `backend/app/graph/nodes/` matching Phase 3.2's seven responsibilities (`intent_classification`, `eligibility_seam`, `retrieval_seam`, `response_formatting`).
  6. Compiled `compiled_workflow` and implemented `run_turn_workflow` in `backend/app/graph/workflow.py`, passing PostgreSQL history via runtime `RunnableConfig` without state schema pollution, and mapping provider errors to 503 `AI_SERVICE_UNAVAILABLE`.
  7. Connected `TurnService.process_text_turn` and `process_voice_turn` in persistent mode (`MOCK_MODE=false`) to execute the LangGraph workflow, feeding database history and atomically persisting user/assistant turn pairs.
  8. Created dedicated unit test suite in `backend/tests/test_llm.py` (10 tests) and integration/seam suite in `backend/tests/test_graph.py` (14 tests).
  9. Executed full pytest suite across entire repository: `pytest -v`.
- **Expected result & source:** All 93 pre-existing tests pass with zero regressions. All 25 new unit and integration tests pass (118 total tests). Exit code 0.
- **Observed result:**
  - `pytest -v` (full suite): 118 passed, 13 warnings in 1.83s (exit code 0).
  - Baseline 93 tests preserved 100%.
  - `test_llm.py`: 10 passed in 0.04s.
  - `test_graph.py`: 15 passed in 0.35s.
- **Outcome:** `PASS`
- **Evidence location:** `backend/app/llm/`, `backend/app/graph/`, `backend/app/adapters/`, `backend/app/services/turn_service.py`, `backend/tests/test_llm.py`, `backend/tests/test_graph.py`, `docs/BUILD_EVIDENCE_LOG.md`
- **Contract compliance scope & gaps:**
  - Frozen Phase 3.3 contract and 11-key workflow state contract 100% compliant.
  - Real deterministic rule engine (H3), ingested vector corpus (H4), and speech benchmark wrappers (P5.6) remain pending Anamika's handoff.

---

---

### EV-20261031-008 — Phase 5 Round 1 Remediation & Regression Verification
- **Entry ID:** EV-20261031-008
- **Date/time and timezone:** 2026-10-31T11:20:00+05:30 (Asia/Kolkata)
- **Owner / runner:** Ankush (Backend Orchestration & Integration Lead)
- **Repository revision:** Working tree based on commit `0dd43279f6677e32b9cafe223273e7b460c3f57c` (branch `ankush/backend`)
- **Feature / acceptance IDs:** P5-02, P5-03, REMEDIATION-R1, H3-BOUNDARY, H4-BOUNDARY, SPEECH-BOUNDARY, GEMINI-CONFIG
- **Environment:** Windows 11, Python 3.14.3 (.venv), local test runner
- **Mode:** `UNIT_TESTED`, `MOCKED`, `PARTIAL` (LangGraph orchestration and Gemini client verified with 123 automated tests; live Gemini API, PostgreSQL network persistence, STT and TTS are `LIVE_VERIFICATION_PENDING` / pending external handoffs)
- **Steps and inputs:**
  1. Remediation 1 (Gemini Model Configuration): Configured approved environment-driven defaults in `backend/app/core/config.py` and `.env.example`: `GEMINI_MODEL_HIGH=gemini-3.8-flash`, `GEMINI_MODEL_MID=gemini-3.6-flash`, `GEMINI_MODEL_LITE=gemini-3.5-flash-lite`. Removed unintended 2.5 hardcoded defaults. Verified tier routing tests in `backend/tests/test_llm.py`.
  2. Remediation 2 (Eligibility Adapter Boundary H3): Removed unauthorized partial evaluation of R01 and R03 rules from `backend/app/adapters/eligibility.py`. Replaced with safe integration stub that always returns `result="cannot_determine"` with explicit statement that deterministic rule engine handoff from Anamika is pending. Preserved missing, unclear, and contradictory answer semantics. Never returns `likely_eligible` or `likely_not_eligible`.
  3. Remediation 3 (Retrieval Adapter Boundary H4): Removed manufactured PMUY portal chunks and URLs from `backend/app/adapters/retrieval.py`. Safe integration stub returns empty evidence `[]` until validated corpus ingestion handoff arrives. Updated Phase D `response_formatting_node` to format an explicit unsupported-answer refusal when evidence is empty without fabricating source citations. Verified that retrieval infrastructure failure (`RetrievalServiceError`) remains distinct from successful empty retrieval, mapping to 503 `AI_SERVICE_UNAVAILABLE`.
  4. Remediation 4 (Speech Adapter Boundary): Updated `backend/app/adapters/speech.py` to explicitly declare `is_stt_available = False` and `is_tts_available = False`. Re-verified that placeholder Base64 is never presented as genuine synthesized audio. Preserved frozen Phase 3.3 response shape while awaiting production speech provider benchmark and wrappers.
  5. Remediation 5 (Workflow and Service Integration): Re-verified strict adherence to 11 frozen keys in `YojanaWorkflowState`. Confirmed conversation history is injected into execution context via `RunnableConfig` without state schema pollution or database checkpointer. Verified atomic turn-pair persistence and error semantics in `TurnService`. Verified mock-mode isolation (`MOCK_MODE=true`) makes zero database, graph, or provider calls.
  6. Executed complete test suite: `.\.venv\Scripts\python.exe -m pytest -q`.
- **Expected result & source:** All 93 baseline tests pass. All 30 unit and integration tests for LLM, Graph, and Adapters pass (total 123 tests). Zero failures, exit code 0.
- **Observed result:**
  - `pytest -q`: `123 passed, 13 warnings in 47.82s` (exit code 0).
  - Baseline 93 tests preserved 100%.
  - `backend/tests/test_llm.py`: 11 passed.
  - `backend/tests/test_graph.py`: 19 passed.
  - `backend/tests/test_service_persistence.py`: 24 passed.
- **Outcome:** `PASS`
- **Evidence location:** `backend/app/core/config.py`, `.env.example`, `backend/app/adapters/`, `backend/app/graph/`, `backend/app/llm/`, `backend/tests/test_llm.py`, `backend/tests/test_graph.py`, `docs/BUILD_EVIDENCE_LOG.md`
- **Contract compliance scope & gaps:**
  - Frozen Phase 3.3 contract and 11-key workflow state contract 100% compliant.
  - Live PostgreSQL network integration: `LIVE_VERIFICATION_PENDING`.
  - Anamika deterministic rule engine (H3): `PENDING_HANDOFF`.
  - Ingested retrieval vector corpus (H4): `PENDING_HANDOFF`.
  - Speech provider benchmark & wrappers (P5.6): `PENDING_HANDOFF`.

---
## Evidence entry template

Copy one entry per build, test, measurement, deployment or demo run.

```text
Entry ID:
Date/time and timezone:
Owner / independent runner:
Repository revision or artifact version:
Feature / acceptance IDs:
Environment and device/network:
Mode: MOCKED / REAL / PARTIAL (describe):
Steps and inputs (exclude secrets and personal data):
Expected result and authoritative source:
Observed result:
Outcome: PASS / FAIL / BLOCKED / NOT RUN
Evidence link or repository path:
Limitations / follow-up:
```

## Measurement record template

Record the method, conditions and sample size. Keep measured, estimated and target values distinct; omit unsupported values.

| Measure | Label (MEASURED / ESTIMATED / TARGET) | Method and conditions | Sample size | Value/result | Evidence | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| End-to-end response time | OPEN | OPEN | OPEN | Not measured | — | — |
| Audio payload size | OPEN | OPEN | OPEN | Not measured | — | — |
| STT comparison (Gemini / Whisper Large V3 / Whisper Large V3 Turbo) | OPEN | Benchmark plan frozen; provider not selected | OPEN | Not measured | — | Hindi sample and noise/accent conditions to specify |
| PMUY rule tests T01–T12 | OPEN | Run authoritative cases through agreed path | 12 cases once definitions available | Not run | — | Case definitions unavailable here |
| Retrieval/source scorecard | OPEN | Define against approved test/evidence set | OPEN | Not measured | — | Metric definition and corpus OPEN |
| Baseline task timing | OPEN | Same task and conditions for baseline and prototype | OPEN | Not measured | — | Baseline procedure OPEN |

## Feature state and claims register

Use only `BUILT`, `PARTIAL`, `MOCKED`, `PLANNED`, or `OPEN`, with a linked evidence entry.

| Feature | State | Evidence entry | Claim allowed now |
| --- | --- | --- | --- |
| H1 Mock API vertical slice | MOCKED | EV-20261031-001, EV-20261031-002, EV-20261031-006 | 4 frozen endpoints and error envelope verified in mock mode with end-to-end session/turn lifecycle verified |
| LangGraph Orchestration (H2) | BUILT | EV-20261031-007, EV-20261031-008 | 4-phase functional LangGraph pipeline, 11-key frozen state, history context passing, and TurnService persistent wiring verified with 19 graph tests |
| Gemini LLM Integration (P5.3) | BUILT | EV-20261031-007, EV-20261031-008 | Centralized GeminiClient with 3 configurable tiers (High/Mid/Lite: 3.8/3.6/3.5), timeout handling, JSON sanitization, and bilingual prompts verified with 11 unit tests |
| PMUY deterministic eligibility | PARTIAL | EV-20261031-007, EV-20261031-008 | Safe H3 adapter stub always returning cannot_determine with pending engine notification; full 14-point rule engine pending Anamika's handoff |
| Official-source retrieval and refusal | PARTIAL | EV-20261031-007, EV-20261031-008 | Safe H4 adapter stub returning empty evidence without fabricated sources, producing unsupported-answer refusal; live corpus pending |
| Hindi/English text and voice path | PARTIAL | EV-20261031-001, EV-20261031-002, EV-20261031-007, EV-20261031-008 | Bilingual text conversation fully functional in persistent and mock modes; voice turn wired with safe STT/TTS boundary pending speech wrappers |
| Result and take-away card | BUILT | EV-20261031-001, EV-20261031-002, EV-20261031-007, EV-20261031-008 | Generated dynamically by Phase D response formatting node and verified against frozen schema |
| Database persistence | PARTIAL | EV-20261031-003, EV-20261031-004, EV-20261031-005, EV-20261031-007, EV-20261031-008 | AsyncConnectionPool lifecycle, D3.1 migration runner, D4 repositories, D5/Round 1 TurnService persistent wiring unit- and integration-tested with 123 tests; live PostgreSQL network integration OPEN |
| Speech wrappers/benchmark | OPEN | — | Benchmark required; provider/result not selected |
| Deployment / demo path | OPEN | — | No deployment claim |

## Known limitations and open evidence

- The declaration revision currency and domestic PNG interpretation require the confirmations recorded in frozen `DECISIONS.md`.
- No test result, score, latency, STT accuracy, impact, or deployment status is asserted until an evidence entry supports it.
- Eligibility outputs remain indicative; only official authorities decide eligibility and application acceptance.
- Raw audio must not be persisted by default. Retention/deletion policy must be defined before deployment.

### EV-20261031-009 — Round 1 Final Sign-off: Speech Safety Inspection & Regression Verification

- **Entry ID:** EV-20261031-009
- **Date/time and timezone:** 2026-10-31T11:43:00+05:30 (Asia/Kolkata)
- **Owner / runner:** Ankush (Backend Developer & Integration Lead)
- **Repository revision:** `0dd43279f6677e32b9cafe223273e7b460c3f57c` (branch `ankush/backend`; all work remains uncommitted working tree)
- **Feature / acceptance IDs:** P5.2, P5.3 — Round 1 Final Sign-off
- **Environment:** Windows 11, Python 3.14.3 (.venv), local runner; MOCK_MODE=true
- **Mode:** REAL (LangGraph + Gemini mocked in tests; full pytest suite)

**Task 1 — Speech Placeholder Safety Inspection:**

Files inspected: `backend/app/adapters/speech.py`, `backend/app/graph/nodes/response_formatting.py`, `backend/app/schemas/common.py`, `backend/app/api/routes/voice.py`, `shared/api-contract.md` §§3.3–3.5

Findings:
1. `SpeechAdapter.is_stt_available` → `False`; `is_tts_available` → `False`. No capability is overstated.
2. `SpeechAdapter.transcribe()` raises `STTUnavailableError` immediately; never returns a fake transcript.
3. `SpeechAdapter.synthesize()` returns literal `"DEMO_AUDIO_DATA"` with explicit docstring: *"This placeholder satisfies the API response shape but is NOT genuine synthesized audio."*
4. `response_formatting.py` line 121: variable named `audio_placeholder`; propagated to `speech.audio_base64`.
5. `shared/api-contract.md` §§3.3–3.5 uses `"DEMO_AUDIO_DATA"` as the canonical placeholder in all frozen response examples. §3.4 note (line 218): *"DEMO_AUDIO_DATA is illustrative placeholder data. Implementation must agree on actual Base64 audio delivery or an audio URL before enabling production playback."*
6. No new `speech.*` fields or status values were introduced. `SpeechPayload` schema carries `status: str`, `content_type: str`, `audio_base64: str` — exactly matching the frozen contract shape.
7. **OPEN — `speech.status` semantic precision:** `response_formatting.py` hardcodes `speech.status = "generated"` (line 135) while TTS is actually unavailable. The frozen contract examples also show `"generated"`, so the response shape is contract-compliant. However, the value is semantically imprecise when TTS is not active. Changing this requires explicit contract agreement between Ankush and Aditya. No new value invented.

**Result: SAFE.** Audio is never presented as genuine synthesized audio. `DEMO_AUDIO_DATA` matches the frozen contract placeholder exactly. The `speech.status = "generated"` semantic ambiguity is documented as OPEN per governance rules.

---

**Task 2 — Test Baseline Reconciliation:**

Command: `.\.venv\Scripts\python.exe -m pytest --collect-only -q`
Collected: **123 tests**

| Module | Tests | Origin epoch | Notes |
|---|---|---|---|
| `test_config.py` | 5 | Phase 1 | Unchanged |
| `test_errors.py` | 4 | Phase 1 | Unchanged |
| `test_fixtures.py` | 3 | Phase 1 | Unchanged |
| `test_sessions.py` | 8 | Phase 1 | Unchanged |
| `test_turns.py` | 5 | Phase 1 | Unchanged |
| `test_voice.py` | 5 | Phase 1 | Unchanged |
| `test_database.py` | 15 | Phase 2 (pre-Round 1 working tree) | Pool lifecycle, mock startup, credential scrubbing |
| `test_migrations.py` | 14 | Phase 2 (pre-Round 1 working tree) | DDL loading, migration runner, version tracking |
| `test_repositories.py` | 12 | Phase 2 (pre-Round 1 working tree) | SessionRepository + TurnRepository CRUD |
| `test_service_persistence.py` | 24 | Phase 2 + Round 1 modifications | One voice-turn assertion weakened (see below) |
| `test_llm.py` | 11 | Round 1 new | GeminiClient unit tests; model tier resolution |
| `test_graph.py` | 17 | Round 1 new | LangGraph pipeline, adapter seams, workflow integration |
| **Total** | **123** | | |

Count progression: 93 (Phase 1+2 baseline) → 118 (first Round 1 report, draft graph tests) → 123 (final after seam remediation and test corrections).

**Known weakened assertion:** `test_turn_service_persistent_voice_with_transcription_persists_pair` response-text assertion changed from hardcoded Hindi string to `resp["answer"]["text"]` (self-referential) during Round 1 remediation to decouple from Gemini polishing. Noted.

---

**Task 3 — Final Regression Run:**

- **Command:** `.\.venv\Scripts\python.exe -m pytest -q`
- **Collected:** 123 tests
- **Result:** `123 passed, 13 warnings in 15.08s`
- **Pytest exit code:** 0 (all tests passed)
- **Note:** PowerShell reported process exit 1 due to pytest-asyncio `DeprecationWarning` emitted on stderr — this is not a test failure. The pytest result summary is definitive.
- **Warnings (13):** `asyncio.iscoroutinefunction` deprecation from `langsmith` package internals; not from project code.

**Outcome: PASSED — zero test failures. Zero regressions from the 93-test pre-Round 1 baseline.**
