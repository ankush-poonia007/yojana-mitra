# Yojana Mitra — Phase 5 Implementation Plan

**Status:** Approved documentation baseline; implementation status is not asserted here.  
**Scope:** Phase 5 build planning for the frozen Yojana Mitra v1.  
**Schedule:** **OPEN — confirm actual event start, remaining time, checkpoints, freeze, demo and submission deadlines with the team.** Historical checkpoint times below are planning prompts only.

## Authority and change control

Use `DECISIONS.md` (frozen Phase 4.1), `PHASE_4.2_PERSONAL_BRIEFS.md` (documented ownership), `YOJANA_MITRA_MASTER_BRIEF.md`, `ui_userflow.md`, the Phase 3.2 architecture record, Phase 3.3 API contract, reviewed H1–H4 contract artifacts, and the PMUY Knowledge Base as applicable. The Phase 4.1 record says some of those source artifacts were referenced but are absent from this local copy; retrieve them before implementing exact rule details or test expectations. `sources/` is read-only.

Do not change frozen architecture, API shapes, eligibility rules, language behavior, privacy policy, or approved integration boundaries as part of routine implementation. If a source conflict requires a change, stop at that boundary and record a proposed amendment with evidence and approval; do not silently revise a freeze.

## Product and scope

Build the approved voice and text scheme assistant. PMUY is the only scheme with full eligibility assessment. PM-KISAN and PM-JAY 70+ are information-only only after their official sources are validated. Eligibility is indicative, never an official determination. Hindi and English are v1 languages; the user chooses the response language. Text and voice share workflow logic. Preserve Phase 3.3 response contracts, including `speech.audio_base64`.

The core path is session start → Hindi/English text or voice turn → PMUY ask-back interview → deterministic eligibility result with reasons → grounded explanation and source references or refusal → take-away card and disclaimer. Readiness and official verification remain distinct from eligibility.

### Protected P0 path

- Session creation and text turns through the frozen API.
- PMUY ask-back interview and deterministic R01–R06 evaluation using D01–D12; D13 is evaluated once through R03; R07 remains readiness/verification only.
- Unknown, unclear, contradictory, or missing answers are not coerced to “No” or a pass. R05 clear failure and uncertain outcomes follow D3.
- Official-source-grounded answers, provenance, and refusal when evidence is insufficient.
- Hindi and English text, result/card, indicative-not-official disclaimer, and usable typed fallback.
- Baseline PMUY-T01–T12 and integration verification; actual results recorded only after execution.

Voice input/output, deployment, and richer card behavior are included in the approved plan where feasible; their exact acceptance details and delivery state remain unverified until evidenced. Apply the Phase 4.5 cut order only after the team confirms priorities against the actual event schedule. Never silently cut protected P0 behavior, testing, rehearsal, or submission buffer.

### P1 / P2 boundary

Candidate P1/P2 items from the project brief include secondary scheme chips marked “coming soon,” My Conversations, Settings, Guest User, interactive demo screens, image/PDF card export, visual polish/animation, and broader scheme support. Exact priority per feature is **OPEN — team confirmation**. Do not imply PM-KISAN or PM-JAY eligibility assessment is in scope.

## Ownership and working boundaries

| Owner | Owns | Boundary |
| --- | --- | --- |
| Ankush | Backend API/routes, schemas, graph/orchestration, services/integration, retrieval integration, **backend database wiring**, deployment coordination, `docs/`, root project configuration | Frozen API/architecture stay unchanged; coordinate data and rule handoffs. |
| Anamika | `data/` artifacts, verified scheme data, deterministic eligibility and question-bank handoff, ingestion/data artifacts, speech STT/TTS wrappers, benchmark and evaluation artifacts, agreed backend modules | Does not own backend database wiring, routes, graph, API schemas, or unagreed files. Coordinate persistence/data handoffs with Ankush. |
| Aditya | `frontend/`, UI flow, client integration and presentation/demo materials as assigned | Follow Phase 3.3 API and shared examples; typed path remains available if speech fails. |

**Conflict resolved:** a Phase 4.5 kickoff block assigns `backend/app/database` to Anamika. This conflicts with the Phase 4.2 personal brief and the explicit Phase 5 ownership instruction. Preserve Phase 4.2 ownership: Ankush owns backend database wiring; Anamika supplies data/eligibility/speech and agreed handoff modules. Any future change needs explicit team approval and an ownership record update.

## Sequence and gates

Work in dependency order: (1) confirm source artifacts, repo baseline, schedule and owners; (2) verify shared mock and frozen H1 API; (3) establish a mock vertical slice; (4) connect real deterministic eligibility and persistence through agreed seams; (5) connect official-source retrieval and grounded/refusal behavior; (6) connect voice wrappers and client playback/fallback; (7) run acceptance matrix, deployment/clean-start checks, rehearsal and evidence capture. Exact functions, schemas, migrations and node names remain **OPEN** where the reviewed artifacts are unavailable.

| Gate (historical template) | Intended review | Status |
| --- | --- | --- |
| Thin slice (historically 2:30 AM) | Mock session/turn/standard response across API and client | Actual time **OPEN**; no result asserted |
| First real end-to-end (historically 5:30 AM) | Real typed PMUY path with deterministic result and official evidence | Actual time **OPEN**; no result asserted |
| Basic P0 (historically 8:00 AM) | Confirm protected path, Hindi/English text, voice/fallback and card status | Actual time **OPEN**; no result asserted |
| Feature freeze (historically 6:00 AM / 9:00 AM tested gate in source prompts) | Confirm one actual freeze time and post-freeze bug policy | **OPEN — team confirmation** |
| Demo/submission (historically 1:00 PM target) | Confirm event deadline; reserve test, rehearsal and recovery buffer | **OPEN — event rules/team confirmation** |

These are gate definitions, not a schedule commitment. Historical timestamps are templates only and must not be treated as current local time or remaining time.

## Definition of Done

A feature is DONE only when its owner, dependencies and contract are clear; implementation follows frozen decisions; acceptance criteria in `TEST_ACCEPTANCE_MATRIX.md` have actual recorded outcomes; failures and limitations are documented; and the evidence log links to reproducible evidence. Until then use NOT STARTED, IN PROGRESS, BLOCKED, PARTIAL, MOCKED, or OPEN as appropriate. Do not mark DONE from a plan or a mock-only path.

## Unresolved before implementation

- Exact Phase 3.2 architecture record, Phase 3.3 API artifact, detailed H1–H4 artifacts, PMUY Knowledge Base and T01–T12 case definitions are not present in the inspected editable project copy: **OPEN — retrieve and verify**.
- H2/H3/H4 exact callable names, inputs/outputs, error behavior, persistence boundaries and mock/real switching: **OPEN**; see `shared/INTEGRATION_CONTRACTS.md`.
- Exact database schema/DDL, retention/deletion implementation and agreed session fields: **OPEN**; preserve privacy decisions and Ankush ownership.
- Declaration revision currency and R06 domestic PNG distributor confirmation: **OPEN** per frozen decisions.
- Actual checkpoint/deadline times and acceptance details beyond the frozen baseline: **OPEN**.
- STT provider selection and measured audio size/latency: **OPEN**; benchmark rather than assume.
