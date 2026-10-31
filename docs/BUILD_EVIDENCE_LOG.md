# Yojana Mitra — Build and Evidence Log

**Purpose:** Record observed build state and evidence. This is a blank log initialized before implementation; it contains no claimed test results, measurements, deployments, or performance metrics.

## Current record

| Item | Status | Evidence / notes |
| --- | --- | --- |
| Phase 5 application implementation | PARTIAL | Anamika-owned components implemented through TASK-ANAMIKA-07D. See evidence entries EV-01 through EV-09. |
| Tests / acceptance runs | 244 PASSED | python -m pytest from backend/ on branch anamika/backend. See EV-01 through EV-07. |
| Performance / speech measurements | NOT MEASURED HERE | No latency, accuracy, payload size, scorecard or baseline number is asserted. |
| Deployment / clean-start demo | NOT VERIFIED | Record actual environment and steps when run. |
| Frozen contracts and rule source artifacts | PARTIALLY AVAILABLE | See `DECISIONS.md`; linked reviewed H1–H4 artifacts, Phase 3.2/3.3 full records, PMUY KB and T01–T12 details were not available in the inspected editable copy. |
| Schedule/checkpoints | OPEN | Confirm actual event times. Historical times are templates only. |

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

Use only `BUILT`, `PARTIAL`, `MOCKED`, `PLANNED`, or `OPEN`, with a linked evidence entry. No product feature is marked BUILT by this initial record.

| Feature | State | Evidence entry | Claim allowed now |
| --- | --- | --- | --- |
| PMUY deterministic eligibility | BUILT | EV-02 | 28 tests pass on branch anamika/backend |
| PMUY question bank (21 questions) | BUILT | EV-03 | 12 tests pass on branch anamika/backend |
| Conversational answer normalizer | BUILT | EV-05 | 165 tests pass on branch anamika/backend |
| Ingestion scaffold (stubs + models) | PARTIAL | EV-06 | Model tests pass; extractor/chunker pending H4 + sources |
| Official-source retrieval and refusal | OPEN | — | Frozen requirement only; H4 OPEN |
| Hindi/English text and voice path | PARTIAL | EV-05 | Normalizer bilingual; full voice path not built |
| Result and take-away card | OPEN | — | Planned acceptance only |
| Database persistence | OPEN | — | Ankush ownership confirmed; implementation not verified |
| Speech wrappers/benchmark | OPEN | — | Benchmark required; provider/result not selected |
| Deployment / demo path | OPEN | — | No deployment claim |

## Known limitations and open evidence

- The declaration revision currency and domestic PNG interpretation require the confirmations recorded in frozen `DECISIONS.md`.
- PMUY Knowledge Base, PMUY Research Analysis, Phase 3.2/3.3 detailed records, reviewed H1–H4 schemas, and PMUY-T01–T12 exact cases were not inspectable in this repository copy; retrieve them before exact implementation/verification.
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
