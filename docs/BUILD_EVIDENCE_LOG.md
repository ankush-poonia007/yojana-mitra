# Yojana Mitra — Build and Evidence Log

**Purpose:** Record observed build state and evidence. This log contains verified results from executed builds, tests, and integration runs.

## Current record

| Item | Status | Evidence / notes |
| --- | --- | --- |
| Phase 5 application implementation | PARTIAL (MOCK SLICE) | Phase 1 modular backend foundation and H1 mock API slice implemented in `backend/app/` (EV-20261031-001, EV-20261031-002). Real database, LangGraph, Gemini, eligibility, retrieval, and live speech remain unbuilt. |
| Tests / acceptance runs | 30 PASSED (CONFIG ROBUSTNESS VERIFIED) | Automated test suite in `backend/tests/` executed via pytest: 30 passed in 0.38s with exit code 0 without manual environment overrides (EV-20261031-002). |
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
| H1 Mock API vertical slice | MOCKED | EV-20261031-001, EV-20261031-002 | 4 frozen endpoints and error envelope verified in mock mode with documented session/413 limitations |
| PMUY deterministic eligibility | OPEN | — | Planned scope only; no build/test claim |
| Official-source retrieval and refusal | OPEN | — | Frozen requirement only; no runtime claim |
| Hindi/English text and voice path | MOCKED | EV-20261031-001, EV-20261031-002 | Mock slice response verified; live speech OPEN |
| Result and take-away card | MOCKED | EV-20261031-001, EV-20261031-002 | Fixture-backed only |
| Database persistence | OPEN | — | Ankush ownership confirmed; implementation not verified |
| Speech wrappers/benchmark | OPEN | — | Benchmark required; provider/result not selected |
| Deployment / demo path | OPEN | — | No deployment claim |

## Known limitations and open evidence

- The declaration revision currency and domestic PNG interpretation require the confirmations recorded in frozen `DECISIONS.md`.
- No test result, score, latency, STT accuracy, impact, or deployment status is asserted until an evidence entry supports it.
- Eligibility outputs remain indicative; only official authorities decide eligibility and application acceptance.
- Raw audio must not be persisted by default. Retention/deletion policy must be defined before deployment.
