# Antigravity Build Guide — Aditya

**Role:** Frontend, voice/text interface, result/card presentation and demo experience  
**Companion documents:** `YOJANA_MITRA_MASTER_BRIEF.md`, `PHASE_4.2_PERSONAL_BRIEFS.md`, `ui_userflow.md`, `DECISIONS.md`, `docs/PHASE_5_IMPLEMENTATION_PLAN.md`, `docs/FEATURE_BOARD.md`, `shared/INTEGRATION_CONTRACTS.md`, `docs/TEST_ACCEPTANCE_MATRIX.md`, `docs/BUILD_EVIDENCE_LOG.md`  
**Schedule:** Confirm actual event times. Historical checkpoints are templates only.

## Mission

Build the user-facing React/TypeScript client for the approved Yojana Mitra flow. Start against a clearly labeled mock that matches the frozen API contract, then connect to the real API. Make the PMUY interview, uncertainty, sources, disclaimer, result and take-away card understandable on desktop and mobile. Preserve text as a usable fallback when speech fails.

## Read before editing

1. Read root `AGENTS.md`; all files under `sources/` are read-only.
2. Read `YOJANA_MITRA_MASTER_BRIEF.md`, `PHASE_4.2_PERSONAL_BRIEFS.md`, `ui_userflow.md`, `DECISIONS.md`, and all five Phase 5 documents.
3. Inspect the actual frontend tree, framework, design assets, package scripts, current state and existing work before editing. Do not assume Vite/Tailwind or replace an established setup without evidence.
4. Locate the frozen Phase 3.3 API response and reviewed H1 details. The project copy has only a summary; exact schemas, error examples and mock fixture path remain OPEN unless available in the repository.

## Ownership

**You own:** `frontend/` and its UI, client-side state, user-accessible error/loading/fallback states, and demo/presentation assets where the team confirms their path. Shared API examples or fixtures are shared work: coordinate with Ankush before changing them.

**Do not edit:** `sources/`, backend routes/schemas/graph/database, eligibility rules/data, or frozen H1/API shapes. Ask Ankush for H1/API/mock questions and Anamika for verified rule/source/card content. Do not call internal H2–H4 services directly from the client.

## Frozen product and UX constraints

- Hindi and English are v1; the user manually selects response language. Do not add automatic switching as a requirement.
- Full eligibility is PMUY only. Other scheme chips, if present, must clearly say “coming soon” or show validated information-only content; never imply other scheme eligibility is implemented.
- Results are indicative, not official. Display the approved disclaimer on every result.
- Show evidence/source information from the API; never invent or hardcode a citation as if retrieved. If source metadata is absent, show a safe unavailable state and report the mismatch.
- The deterministic engine is authoritative. Do not calculate eligibility or reinterpret reasons in browser code. Present `cannot_determine`/“cannot tell yet” without nudging the user toward a favorable answer.
- Keep eligibility, readiness and official verification distinct wherever surfaced.
- Voice and typed turns share session/workflow behavior. If STT fails, typed input remains usable; if TTS fails, the written answer remains visible.
- Preserve all H1 endpoint and payload shapes. Exact mapping is OPEN until verified against Phase 3.3.
- Do not expose server credentials in frontend environment variables. Use only approved public configuration such as the verified API base URL and mock switch.
- Do not send live AI requests from scripted onboarding/demo screens if the existing brief says the demo is scripted.

## Build sequence

### 1. Baseline and plan

- Identify current routes, components, styles, language handling, session state and API client. Preserve useful existing work.
- Map tasks to Feature Board IDs. Confirm whether presentation/deck assets belong in this repository and get the agreed path before adding them.
- Confirm actual checkpoints and demo constraints with the team; do not treat old timestamps as current deadlines.
- Report your proposed files, API dependencies and blockers before implementation. If a frozen response field is missing, do not invent it; provide a clearly labeled mock only after verifying the approved contract source.

### 2. Core journey

Implement the existing UX flow in dependency order, adapting to the current project: language selection → welcome/start → mode choice → conversation → result and take-away card → error/retry states. Map start to session creation; text and voice to their H1 endpoints; history/reopen behavior only when supported by the frozen API. The scripted welcome/demo must not accidentally invoke live AI.

### 3. API client and mock mode

- Use the exact H1 request/response/error schemas from the frozen artifact.
- Coordinate with Ankush on the shared response fixture and mock/real switch. Do not duplicate or drift the schema in a separate local mock.
- Label mock content as sample in development/demo context. Never present mock source evidence or assessment as a real result.
- Handle loading, network, validation, unavailable service and retry states without losing user input unnecessarily. Match the frozen error envelope and only display safe, user-relevant content.

### 4. Conversation, voice and accessibility

- Maintain one session across voice and typed turns according to the API contract. Preserve the conversation when switching modes if that behavior is supported by the agreed H1/session semantics.
- Make microphone permission and recording state explicit. Provide typed fallback if permission/STT fails and keep written answers available if TTS fails.
- Do not persist audio in frontend storage. Avoid showing transcripts or personal content in debug logs.
- Support keyboard use, visible focus, readable contrast, clear controls and mobile layouts. Do not claim accessibility compliance without a defined and run check.

### 5. Results and take-away card

- Render only the assessment and card fields returned by the verified API contract. Do not derive eligibility from answer state in the UI.
- Clearly distinguish likely eligible, likely not eligible, and cannot determine. Display reasons, missing information, source references and the indicative disclaimer as supplied by the approved contract.
- Ensure source labels/link/date are accessible and do not imply official endorsement beyond what the source says.
- If required content is unavailable, show a transparent empty/unavailable state and raise a contract issue rather than filling in policy.

### 6. Optional work and demo

- Protect the P0 end-to-end journey before pursuing My Conversations, Settings, Guest User, interactive demo screens, card image/PDF export, animation or visual polish. Exact priority is OPEN in the Feature Board and must be reviewed against actual schedule.
- Prepare a demo flow only from verified built/mock status. State clearly what is mocked, partial or real. Use a clean reset procedure provided by the team.

### 7. Verification and handoff

- Verify the client against the shared mock and API success/failure examples once the frozen H1 artifact is available.
- Use relevant acceptance entries in `docs/TEST_ACCEPTANCE_MATRIX.md`: Hindi and English clean starts, source/disclaimer rendering, text fallback, voice/text session continuity, service failures, mobile/network and independent reset.
- Record only actual checks and observations in `docs/BUILD_EVIDENCE_LOG.md`, with browser/device, revision, route, mode (MOCKED/REAL), expected/observed result and evidence.
- Handoff to the team with paths, run steps, API/mock configuration, what is MOCKED versus REAL, observed test results, limitations and OPEN contract gaps.

## Acceptance for your assignment

- Core user flow is understandable and follows `ui_userflow.md` and the verified H1 contract.
- Hindi and English are manually selected and rendered correctly from the API result.
- Browser code does not calculate/alter eligibility or fabricate source evidence.
- Every result carries the indicative-not-official notice and accessible source presentation.
- Typed input works when speech is unavailable; written answer stays available when TTS is unavailable.
- Mock results are visibly distinguished from real results.
- Mobile, empty/error/loading/retry states are checked and actual outcomes documented.

## Ready-to-paste Antigravity prompt

```text
You are implementing Aditya’s assigned Yojana Mitra Phase 5 frontend work. Follow docs/ANTIGRAVITY_ADITYA_BUILD_GUIDE.md and read root AGENTS.md, YOJANA_MITRA_MASTER_BRIEF.md, PHASE_4.2_PERSONAL_BRIEFS.md, ui_userflow.md, DECISIONS.md, docs/PHASE_5_IMPLEMENTATION_PLAN.md, docs/FEATURE_BOARD.md, shared/INTEGRATION_CONTRACTS.md, docs/TEST_ACCEPTANCE_MATRIX.md, and docs/BUILD_EVIDENCE_LOG.md before editing.

Treat sources/ as read-only. Inspect the real frontend and existing code first; preserve the current framework and useful work. Report a concise plan with owned files, dependencies, checks and OPEN items before coding. You own frontend/ and only confirmed presentation/demo paths. Coordinate shared API fixtures with Ankush. Do not edit backend, data/rules, database wiring or frozen API contracts. Ankush owns backend and database wiring; Anamika owns data, eligibility and speech wrappers.

Frozen behavior: Hindi and English v1 with manual language selection; PMUY only for full eligibility; other scheme options must be clearly “coming soon” or validated information-only, never presented as assessed. The backend deterministic engine owns eligibility. Do not calculate or alter results in the browser. Show the indicative-not-official disclaimer on every result. Display only real source metadata returned by the API; never invent citations. Keep eligibility, verification and application readiness distinct. Voice/text use the same session/workflow; typed input remains available on speech failure and written answer remains visible on TTS failure. Do not persist audio in browser storage or log sensitive content. Preserve frozen H1 endpoint, payload, response and error shapes.

The full Phase 3.3/H1 schema may be missing from this local copy. Do not guess field names or errors. Locate the authoritative contract and shared mock first. If absent, mark the dependent UI/API mapping OPEN, use only a clearly labeled fixture verified by Ankush, and proceed with independent layout work. Do not silently change frozen decisions.

Build order: (1) inspect and plan; (2) implement the core flow from ui_userflow.md using the agreed mock; (3) implement the API client against exact H1; (4) add conversation/session continuity, voice controls, typed fallback and service errors; (5) render assessment, reasons, source and take-away card without deriving policy; (6) complete responsive/mobile and basic accessibility checks; (7) consider optional features only after P0 is complete and the actual schedule allows; (8) document evidence and handoff. Adjust based on current repository dependencies and explain any changes.

Before finishing, inspect your own diff and ownership. Run only relevant available checks and report exact commands and observed outcomes. Update BUILD_EVIDENCE_LOG.md only with real evidence; label mock versus real. Finish with files changed, run steps, API/mock configuration, actual checks/results, limitations and OPEN details. Do not claim a test or feature is done without evidence. Do not commit or push unless separately asked.
```
