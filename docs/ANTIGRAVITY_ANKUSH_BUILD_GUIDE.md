# Antigravity Build Guide — Ankush

**Role:** Team lead, backend orchestration, integration and database wiring  
**Companion documents:** `YOJANA_MITRA_MASTER_BRIEF.md`, `PHASE_4.2_PERSONAL_BRIEFS.md`, `DECISIONS.md`, `docs/PHASE_5_IMPLEMENTATION_PLAN.md`, `docs/FEATURE_BOARD.md`, `shared/INTEGRATION_CONTRACTS.md`, `docs/TEST_ACCEPTANCE_MATRIX.md`, `docs/BUILD_EVIDENCE_LOG.md`  
**Schedule:** Confirm actual event times with the team. All times from older prompts are historical templates only.

## Mission

Build the backend path that connects the frozen API to the approved workflow and integrates PMUY eligibility, persistence, speech, and official-source retrieval through agreed seams. Deliver a working, honest vertical slice first. Keep all frozen architecture, API, eligibility and privacy decisions unchanged. Ankush owns backend database wiring.

## Read before editing

1. Read the root `AGENTS.md` and treat every file under `sources/` as read-only.
2. Read `DECISIONS.md`, `PHASE_4.2_PERSONAL_BRIEFS.md`, `YOJANA_MITRA_MASTER_BRIEF.md`, `ui_userflow.md`, and all five Phase 5 documents listed above.
3. Locate the actual Phase 3.2 architecture, Phase 3.3 API contract, reviewed H1–H4 artifacts, PMUY Knowledge Base and PMUY-T01–T12. Their exact artifacts were not present in the inspected project copy. If absent, do not invent their contents. Record each missing artifact as OPEN and continue only with work whose behavior is completely specified by available sources.
4. Inspect the real repository tree, current code, environment templates, dependencies, and existing run instructions before choosing paths or libraries. Do not assume a folder layout or add a competing implementation.

## Ownership

**You own:** `backend/` API routes, schemas, graph/orchestration, backend services and integration, retrieval integration, eligibility integration, and **backend database wiring**; shared contract/mock work only by coordination; `docs/`; root `.env.example`, `.gitignore`, and `README` as assigned.

**Do not edit:** `sources/`, Aditya’s `frontend/`, Anamika’s `data/` or owned modules without a coordinated handoff, or frozen decisions/contracts without explicit amendment approval. Do not treat the Phase 4.5 prompt assignment of `backend/app/database` to Anamika as controlling; preserve Phase 4.2 and Phase 5 ownership.

## Frozen product and engineering constraints

- Full eligibility assessment is PMUY only. PM-KISAN and PM-JAY 70+ are information-only only after current official-source validation; do not implement eligibility for them.
- Keep eligibility outputs indicative, not official. Keep eligibility, verification and application readiness distinct.
- Implement the frozen deterministic PMUY rules only from the authoritative Knowledge Base. Do not reconstruct unavailable rule values. Preserve R01–R06; use D01–D12; evaluate D13 once through R03; keep R07 in readiness/verification outside eligibility. Unknown, unclear, contradictory and missing answers must not become “No” or a pass. Apply the frozen R05 behavior.
- Preserve official-source-only retrieval and provenance: source ID, page/section, version and retrieval date. Refuse unsupported claims.
- Preserve Hindi and English v1 with user-selected response language and shared voice/text workflow.
- Preserve Phase 3.3 endpoints, response/error shapes and `speech.audio_base64`. No silent contract changes.
- Do not persist raw audio by default. Minimize session data. Retention/deletion details must be settled before deployment.
- Keep mocks labeled and separate from real evaluation. A mock is not a test result or real assessment.
- Keep secrets and private information out of source, logs, fixtures and commits.

## Build sequence

### 1. Baseline and plan

- Report current branch/revision and relevant existing files; never overwrite unreviewed work.
- Map your planned file changes to Feature Board IDs. Identify untouched shared files and ownership overlaps.
- Confirm actual schedule and checkpoints with the team; do not use historical clock times as current deadlines.
- Before coding, provide a concise plan listing files, dependencies, commands you propose to run, and blockers. If an OPEN detail affects a frozen boundary or correctness, pause that portion and ask the team for the authoritative artifact.

### 2. H1 API and mock vertical slice

- Implement or align only the four documented routes after checking the authoritative Phase 3.3 contract: `POST /api/v1/sessions`, `GET /api/v1/sessions/{session_id}`, `POST /api/v1/turns`, `POST /api/v1/voice/turns`.
- Match the frozen standard response keys and error envelope exactly. Master Brief §8 is a summary; it is not permission to fill missing details by guessing.
- Establish a mock path only if it uses the same contract shape and is clearly labeled. Do not score mock assessment/source data as real.
- Coordinate response examples and fixture paths with Aditya. H1 schemas and the exact mock switch/fixture path are OPEN until verified.

### 3. H2 graph orchestration

- Implement the API-to-workflow call using the reviewed H2 invoke function, input/output/shared-state schemas, node list, and error behavior.
- The Master Brief lists candidate state keys, while node names/order and assignment of model tiers versus deterministic Python work are OPEN. Do not convert a summary into a new contract. If the authoritative H2 artifact is missing, implement only a clearly bounded shell that does not claim the missing behavior, or pause the dependent portion.
- Keep deterministic eligibility authoritative. Generated text may explain but must not override the assessment.

### 4. H3 eligibility and persistence integration

- Integrate Anamika’s agreed eligibility module through the exact reviewed H3 handoff. Exact callable name, arguments and return schema are OPEN until verified.
- Own backend database wiring, migrations/schema application and connection configuration. Coordinate exact schema, allowed fields, session lifecycle and data retention with Anamika; do not take over her data/rule artifacts.
- Implement only the persistence operations and fields agreed at the seam. Never persist raw audio by default; do not collect/store Aadhaar or bank numbers.
- Ensure service/database errors follow the frozen API failure behavior and cannot be reported as successful persistence.

### 5. H4 retrieval and grounded response

- Integrate official-source retrieval using the reviewed H4 request/response contract. Exact function, tables/DDL, ranking and error behavior are OPEN until the artifact is available.
- Coordinate source ingestion and chunk handoff with Anamika. Preserve required provenance and distinguish loaded/validated sources from placeholders or samples.
- If retrieval has no qualifying evidence or fails, do not generate an unsupported factual answer. Return the approved unknown/refusal path.

### 6. Speech and deployment wiring

- Integrate Anamika’s STT/TTS wrappers at the agreed boundary; exact wrapper names, formats, timeouts and retry semantics remain OPEN until agreed.
- Preserve the API response contract, including `speech.audio_base64`. Do not switch to a URL or alter response shape without formal amendment.
- Keep typed input and visible written response usable when speech services fail.
- Configure deployment only from verified repo instructions and approved environment names. Never expose server secrets to frontend variables.

### 7. Verification and handoff

- Use `docs/TEST_ACCEPTANCE_MATRIX.md`; retrieve PMUY-T01–T12 exact definitions before claiming baseline completion.
- Record actual commands, environment, revision, expected source, observed output, failures and evidence in `docs/BUILD_EVIDENCE_LOG.md`. Do not invent a pass, metric or deployment.
- Check clean start, error envelope, source references/refusal, mock-vs-real labeling, no raw-audio persistence, and ownership boundaries.
- Give the team a concise handoff: files changed, working path, mock/real boundaries, actual checks and results, unresolved OPEN items, run/reset instructions, and next owner.

## Acceptance for your assignment

- API routes and error behavior match the frozen Phase 3.3 artifact.
- H2/H3/H4 calls match reviewed handshakes; no invented function names or payload fields.
- Ankush owns database wiring; Anamika’s rules/data/speech work connects through agreed interfaces.
- Frozen deterministic eligibility and provenance/refusal behavior are preserved.
- Hindi/English response language and voice/text shared flow remain as frozen.
- Actual results are recorded honestly; no mock is described as real.
- Another teammate can follow the documented clean-start path or the blocker is precisely recorded OPEN.

## Ready-to-paste Antigravity prompt

```text
You are implementing Ankush’s assigned Yojana Mitra Phase 5 backend and integration work. Follow docs/ANTIGRAVITY_ANKUSH_BUILD_GUIDE.md as the role guide and read root AGENTS.md, DECISIONS.md, PHASE_4.2_PERSONAL_BRIEFS.md, YOJANA_MITRA_MASTER_BRIEF.md, ui_userflow.md, docs/PHASE_5_IMPLEMENTATION_PLAN.md, docs/FEATURE_BOARD.md, shared/INTEGRATION_CONTRACTS.md, docs/TEST_ACCEPTANCE_MATRIX.md, and docs/BUILD_EVIDENCE_LOG.md before editing.

Treat sources/ as read-only. Inspect the actual repository and existing code first. Do not assume paths, overwrite existing work, add application code outside your owned area, or begin with a broad refactor. First report a concise implementation plan with files, dependencies, checks, and blockers. Then implement the assigned backend path in small, reviewable steps.

Ownership: Ankush owns backend API/routes, schemas, graph/orchestration, backend services/integration, retrieval integration, eligibility integration, and backend database wiring. Anamika owns data, eligibility implementation/handoff, speech wrappers, evaluation artifacts and agreed modules. Aditya owns frontend. Do not take over another person’s files without an agreed handoff. The conflicting Phase 4.5 assignment of backend/app/database to Anamika is superseded by the Phase 4.2 ownership preserved in the Phase 5 instructions: Ankush owns database wiring.

Frozen constraints: PMUY is the only full eligibility assessment; any PM-KISAN/PM-JAY 70+ content is information-only after official-source validation. Preserve the frozen Phase 3.2 architecture, Phase 3.3 API and response/error shapes including speech.audio_base64, D1–D14 and reviewed H1–H4 boundaries. The deterministic engine owns eligibility; unknown/missing/unclear/contradictory answers never become No/pass. Use official sources with provenance and refuse unsupported claims. Do not persist raw audio by default. Hindi and English are v1; user selects response language. Keep mock and real data separate and label mocks.

Do not guess missing schemas, exact functions, graph nodes, database fields, error semantics, PMUY rule values, T01–T12 cases, retention policy or provider choices. If an authoritative artifact is absent, mark the dependent detail OPEN and continue only with independent work that cannot violate it. Do not silently change a frozen decision; present any necessary amendment for explicit approval.

Build order: (1) inspect/plan; (2) H1 mock/API vertical slice against the actual contract; (3) H2 orchestration against its reviewed contract; (4) H3 eligibility and Ankush-owned persistence wiring through agreed seams; (5) H4 official-source retrieval/refusal; (6) speech wrapper wiring and typed/written fallback; (7) acceptance checks and handoff. Adapt the order only when repository dependencies require it, and explain the dependency.

Before finishing, inspect your own diff and file ownership. Run only checks that are available and appropriate; report the exact commands and actual outcomes. Update docs/BUILD_EVIDENCE_LOG.md only with observed facts. Never claim a test, metric, deployment, or feature passed if it did not. Finish with files changed, how to run, what is MOCKED versus REAL, checks/results, remaining OPEN items, and the next handoff. Do not commit or push unless separately asked.
```
