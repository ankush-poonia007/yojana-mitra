# Yojana Mitra — Build and Evidence Log

**Purpose:** Record observed build state and evidence. This log contains verified results from executed builds, tests, and integration runs.

## Current record

| Item | Status | Evidence / notes |
| --- | --- | --- |
| Phase 5 application implementation | PARTIAL | Anamika-owned components implemented through TASK-ANAMIKA-07D. See evidence entries EV-01 through EV-09. |
| Tests / acceptance runs | 244 PASSED | python -m pytest from backend/ on branch anamika/backend. See EV-01 through EV-07. |
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
| PMUY deterministic eligibility | BUILT | EV-02 | 28 tests pass on branch anamika/backend |
| PMUY question bank (21 questions) | BUILT | EV-03 | 12 tests pass on branch anamika/backend |
| Conversational answer normalizer | BUILT | EV-05 | 165 tests pass on branch anamika/backend |
| Ingestion scaffold (stubs + models) | PARTIAL | EV-06 | Model tests pass; extractor/chunker pending H4 + sources |
| Official-source retrieval and refusal | OPEN | — | Frozen requirement only; H4 OPEN |
| Hindi/English text and voice path | PARTIAL | EV-05 | Normalizer bilingual; full voice path not built |
| Result and take-away card | OPEN | — | Planned acceptance only |
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

## Evidence entries (TASK-ANAMIKA-01 through TASK-ANAMIKA-06C)

### EV-01 -- TASK-ANAMIKA-01: Backend scaffold

```text
Entry ID: EV-01
Date/time and timezone: 2026-10-31, IST (UTC+05:30)
Owner / independent runner: Anamika Shah
Repository revision or artifact version: 39a8a90, branch anamika/backend
Feature / acceptance IDs: TASK-ANAMIKA-01 -- backend scaffold
Environment and device/network: Windows 11, Python 3.11.9, pytest 9.1.1, sandboxed (no network)
Mode: REAL
Steps and inputs:
  cd C:\Users\Lenovo\yojana-mitra\backend
  python -m pytest tests/test_smoke.py -v
Expected result: 3 smoke tests pass
Observed result: 3 passed in 0.08s
Outcome: PASS
Evidence link or repository path: backend/tests/test_smoke.py
Files created: backend/app/__init__.py, backend/app/eligibility/__init__.py,
  backend/pytest.ini, backend/requirements.txt,
  backend/tests/conftest.py, backend/tests/test_smoke.py
Limitations / follow-up: None.
```

### EV-02 -- TASK-ANAMIKA-02: PMUY deterministic eligibility engine

```text
Entry ID: EV-02
Date/time and timezone: 2026-10-31, IST (UTC+05:30)
Owner / independent runner: Anamika Shah
Repository revision or artifact version: 39a8a90, branch anamika/backend
Feature / acceptance IDs: TASK-ANAMIKA-02 -- PMUY eligibility engine (rules R01-R07, disqualifiers D01-D12)
Environment and device/network: Windows 11, Python 3.11.9, pytest 9.1.1, sandboxed (no network)
Mode: REAL
Steps and inputs:
  cd C:\Users\Lenovo\yojana-mitra\backend
  python -m pytest tests/test_eligibility.py -v
Expected result: 28 eligibility tests pass (T01-T12, R04 variants, age, schema, workflow, repeatability)
Observed result: 28 passed in 0.15s
Outcome: PASS
Evidence link or repository path: backend/tests/test_eligibility.py
Files created: backend/app/eligibility/models.py, backend/app/eligibility/rules.py,
  backend/app/eligibility/engine.py, backend/app/eligibility/__init__.py,
  backend/tests/test_eligibility.py
Limitations / follow-up:
  applies_in_own_name later added as explicit field in models.py (see EV-05 fix note).
```

### EV-03 -- TASK-ANAMIKA-03: PMUY question bank

```text
Entry ID: EV-03
Date/time and timezone: 2026-10-31, IST (UTC+05:30)
Owner / independent runner: Anamika Shah
Repository revision or artifact version: 39a8a90, branch anamika/backend
Feature / acceptance IDs: TASK-ANAMIKA-03 -- PMUY question bank (21 questions, 4 stages)
Environment and device/network: Windows 11, Python 3.11.9, pytest 9.1.1, sandboxed (no network)
Mode: REAL
Steps and inputs:
  cd C:\Users\Lenovo\yojana-mitra\backend
  python -m pytest tests/test_question_bank.py -v
Expected result: 12 question-bank tests pass
Observed result: 12 passed in 0.06s
Outcome: PASS
Evidence link or repository path: backend/tests/test_question_bank.py
Files created: data/schemes/pmuy/questions.json (21 questions),
  backend/app/eligibility/question_bank.py,
  backend/tests/test_question_bank.py
Limitations / follow-up:
  Stale __pydantic_extra__ guard for applies_in_own_name removed in dead-code cleanup
  (2026-10-31, same session -- see EV-07).
```

### EV-04 -- TASK-ANAMIKA-04: PMUY source-manifest and ingestion audit (planning only)

```text
Entry ID: EV-04
Date/time and timezone: 2026-10-31, IST (UTC+05:30)
Owner / independent runner: Anamika Shah
Repository revision or artifact version: 39a8a90, branch anamika/backend
Feature / acceptance IDs: TASK-ANAMIKA-04 -- PMUY source-manifest and ingestion audit (planning only)
Environment and device/network: Windows 11, sandboxed (no network)
Mode: REAL (read-only audit)
Steps and inputs: Read-only inspection of docs/, data/schemes/pmuy/. No application files modified.
Expected result: Audit report produced; no code written
Observed result: Artifact written to brain/0deaea61-.../pmuy_ingestion_plan.md.
  data/schemes/pmuy/source_manifest.json created (provenance register, S01-S05).
Outcome: PASS (planning deliverable)
Evidence link or repository path: data/schemes/pmuy/source_manifest.json
Limitations / follow-up:
  H4 chunk schema OPEN (OPEN-01). S03 currency unverified (OPEN-02).
  S04/S05 share one PDF (OPEN-04). All 5 sources need downloading (OPEN-05, requires network approval).
```

### EV-05 -- TASK-ANAMIKA-05: Conversational answer normalizer and applies_in_own_name fix

```text
Entry ID: EV-05
Date/time and timezone: 2026-10-31, IST (UTC+05:30)
Owner / independent runner: Anamika Shah
Repository revision or artifact version: 39a8a90, branch anamika/backend
Feature / acceptance IDs: TASK-ANAMIKA-05 -- conversational answer normalizer; applies_in_own_name fix
Environment and device/network: Windows 11, Python 3.11.9, pytest 9.1.1, sandboxed (no network)
Mode: REAL
Steps and inputs:
  cd C:\Users\Lenovo\yojana-mitra\backend
  python -m pytest tests/test_normalizer.py -v
Expected result: 165 normalizer tests pass (English/Hindi boolean, negation trap, age edge cases,
  contradictory inputs, engine integration)
Observed result: 165 passed in 0.20s
Outcome: PASS
Evidence link or repository path: backend/tests/test_normalizer.py
Files created: backend/app/eligibility/normalizer.py, backend/tests/test_normalizer.py
Files modified: backend/app/eligibility/models.py -- added applies_in_own_name: Optional[bool] = None
Limitations / follow-up:
  _NON_DIGIT_RE dead-code removed in cleanup EV-07 (same session).
```

### EV-06 -- TASK-ANAMIKA-06C: Ingestion scaffold (models, stubs, tests)

```text
Entry ID: EV-06
Date/time and timezone: 2026-10-31, IST (UTC+05:30)
Owner / independent runner: Anamika Shah
Repository revision or artifact version: 39a8a90, branch anamika/backend
Feature / acceptance IDs: TASK-ANAMIKA-06C -- ingestion scaffold (models, stubs, tests)
Environment and device/network: Windows 11, Python 3.11.9, pytest 9.1.1, sandboxed (no network)
Mode: REAL
Steps and inputs:
  cd C:\Users\Lenovo\yojana-mitra\backend
  python -m pytest tests/test_ingestion_models.py -v
Expected result: 36 ingestion-model tests pass (ING-01 through ING-08 test classes)
Observed result: 36 passed in 0.11s
Outcome: PASS
Evidence link or repository path: backend/tests/test_ingestion_models.py
Files created: backend/app/ingestion/__init__.py, backend/app/ingestion/models.py,
  backend/app/ingestion/extractor.py, backend/app/ingestion/chunker.py,
  backend/app/ingestion/ingest_pmuy.py,
  backend/tests/test_ingestion_models.py
Limitations / follow-up:
  PMUYChunk model marked PROPOSED -- pending H4 schema confirmation from Ankush (OPEN-01).
  Extractor, chunker, and ingest_pmuy.py are intentional stubs. Full implementation blocked
  until H4 confirmed and PMUY source files downloaded.
```

### EV-07 -- Dead-code cleanup (LIM-02, LIM-03)

```text
Entry ID: EV-07
Date/time and timezone: 2026-10-31, IST (UTC+05:30)
Owner / independent runner: Anamika Shah
Repository revision or artifact version: 39a8a90, branch anamika/backend
Feature / acceptance IDs: Dead-code cleanup (LIM-02, LIM-03)
Environment and device/network: Windows 11, Python 3.11.9, pytest 9.1.1, sandboxed (no network)
Mode: REAL
Steps and inputs:
  Removed _NON_DIGIT_RE from normalizer.py (defined, never used -- LIM-02).
  Removed stale __pydantic_extra__ guard for applies_in_own_name from question_bank.py -- LIM-03.
  cd C:\Users\Lenovo\yojana-mitra\backend
  python -m pytest -v --tb=short
Expected result: 244 tests pass, no regressions
Observed result: 244 passed in 0.28s
Outcome: PASS
Evidence link or repository path: backend/app/eligibility/normalizer.py,
  backend/app/eligibility/question_bank.py
Limitations / follow-up: None.
```

### EV-08 -- TASK-ANAMIKA-07B: EV-A Offline Eligibility Scorecard

```text
Entry ID: EV-08
Date/time and timezone: 2026-10-31, IST (UTC+05:30)
Owner / independent runner: Anamika Shah
Repository revision or artifact version: 39a8a90, branch anamika/backend
Feature / acceptance IDs: TASK-ANAMIKA-07B -- EV-A offline eligibility scorecard
Environment and device/network: Windows 11, Python 3.11.9, sandboxed (no network)
Mode: REAL (deterministic offline evaluation)
Steps and inputs:
  python data/evaluation/run_eligibility_scorecard.py
Expected result: 22/22 fixture cases evaluated against deterministic engine; all match expected outcome
Observed result: 22 passed, 0 failed, 0 errors, pass rate 100.0% (exit code 0)
Outcome: PASS (PROVISIONAL)
Evidence link or repository path: data/evaluation/eligibility_cases.jsonl,
  data/evaluation/run_eligibility_scorecard.py
Limitations / follow-up:
  All fixture cases marked provisional: true pending formal team sign-off.
  Deterministic engine matches rules; no LLM, database, or external network involved.
```

### EV-09 -- TASK-ANAMIKA-07D: EV-C Question-Flow and EV-D Master P0 Scorecard

```text
Entry ID: EV-09
Date/time and timezone: 2026-10-31, IST (UTC+05:30)
Owner / independent runner: Anamika Shah
Repository revision or artifact version: 39a8a90, branch anamika/backend
Feature / acceptance IDs: TASK-ANAMIKA-07D -- EV-C question-flow and EV-D master P0 scorecard
Environment and device/network: Windows 11, Python 3.11.9, sandboxed (no network)
Mode: REAL (deterministic offline evaluation)
Steps and inputs:
  python data/evaluation/run_question_flow.py
  python data/evaluation/run_scorecard.py
Expected result:
  run_question_flow.py passes 12/12 scenarios (exit code 0).
  run_scorecard.py executes EV-A and EV-C, detects EV-B as NOT IMPLEMENTED, EV-D/E/F as BLOCKED,
  and reports overall PASS WITH DOCUMENTED LIMITATIONS (exit code 0).
Observed result:
  EV-C: 12/12 passed (exit code 0).
  EV-D Master Scorecard: EV-A PROVISIONAL, EV-B NOT IMPLEMENTED, EV-C PROVISIONAL,
  EV-D BLOCKED, EV-E BLOCKED, EV-F BLOCKED. Overall: PASS WITH DOCUMENTED LIMITATIONS (exit code 0).
Outcome: PASS WITH DOCUMENTED LIMITATIONS
Evidence link or repository path: data/evaluation/question_flow_scenarios.jsonl,
  data/evaluation/run_question_flow.py, data/evaluation/run_scorecard.py
Limitations / follow-up:
  EV-A and EV-C fixtures are provisional. EV-B (normalizer runner) not yet implemented.
  EV-D (grounding/refusal) blocked by H4 chunk schema and source file acquisition.
  EV-E (LLM explanation) blocked by live Gemini API requirement.
  EV-F (STT) blocked by speech wrappers.
```
