# Antigravity Prompt Sequence — Ankush

**Purpose:** Copy these prompts into one Antigravity conversation in order to implement Ankush’s Phase 5 work from repository inspection through integration and handoff. Keep the same conversation so later prompts can use the actual outputs from earlier stages.

**Role guide:** `docs/ANTIGRAVITY_ANKUSH_BUILD_GUIDE.md`  
**Project invariants:** frozen decisions/contracts; PMUY only for full eligibility; Ankush owns backend database wiring; `sources/` is read-only.  
**Important:** Reports may describe a different checkout or repository snapshot. Before acting, identify the active project root and use the files that actually exist there. Never fabricate missing files or report summaries as source artifacts.

## How to use this sequence

1. Paste Prompt A and review the repository map and blockers.
2. Confirm Prompt B’s plan and the shared H1/H3/H4 handoffs with the teammates.
3. Run Prompts C–G one at a time. Review each result before asking for the next stage.
4. Do not skip a stop condition because a later prompt assumes a schema or approval.
5. Use Prompt H for final verification and handoff. Do not commit or push unless separately authorized.

---

## Prompt A — Repository and source preflight (read-only)

```text
You are Ankush, responsible for Yojana Mitra backend orchestration, integration, and database wiring. Follow docs/ANTIGRAVITY_ANKUSH_BUILD_GUIDE.md and root AGENTS.md. This stage is READ ONLY: do not edit, create, move, delete, install, deploy, or run migrations.

Identify the active repository root and current branch/revision if available. List relevant existing backend, shared, docs, fixture, configuration, and research files. Read the frozen Phase 3.2 architecture, Phase 3.3 API contract, H1–H4 definitions, PMUY Knowledge Base and T01–T12 cases if present. Treat sources/ as read-only. Distinguish documents you inspected from summaries or references to missing documents.

Return: (1) repository identity; (2) a concise file map; (3) authoritative source files actually found; (4) existing code and current status; (5) discrepancies between the files in this checkout and the Phase 5 guides; (6) exact OPEN inputs; (7) safe work that can start without resolving OPEN items. Explicitly confirm that Ankush owns backend database wiring and that Anamika owns data/eligibility/speech implementation and agreed handoff modules. Do not infer approval from a proposed file path.
```

## Prompt B — Implementation plan and teammate agreements (no code)

```text
Using the inspected repository and the Ankush guide, prepare a file-by-file implementation plan. PLAN ONLY; do not edit files or run migrations.

Organize the backend sequence around: (1) settings/config and standard error handling; (2) H1 mock API vertical slice using the actual frozen contract and canonical fixtures; (3) database/persistence wiring owned by Ankush; (4) H2 orchestration using the reviewed graph contract; (5) H3 eligibility adapter; (6) H4 retrieval integration; (7) speech integration; (8) acceptance and handoff.

For each step list exact existing/new files, dependencies, acceptance evidence, and what must be agreed first. Do not create or propose invented request fields, callable names, node names, tables, vector dimensions, RLS policies, timeouts, or error semantics.

Call out these agreements explicitly for team review: (a) H3 module path, callable signature, input type, return type and errors; (b) who owns the engine file versus Ankush’s adapter; (c) STT/TTS provider wrapper file paths and signatures versus Ankush’s orchestration adapter; (d) H4 chunk metadata and database schema/DDL; (e) migration and retention/deletion decisions; (f) shared fixtures and tests ownership. Mark each undecided item OPEN. Recommend the smallest implementation slice that can begin immediately without depending on them. End with a short approval checklist. No code in this stage.
```

## Prompt C — Backend foundation and H1 mock API

```text
Implement only the backend foundation and H1 mock/API slice approved from the plan. Before editing, restate the exact approved files and their contract sources. If the frozen Phase 3.3 contract or fixtures are missing or contradictory in this checkout, stop the affected endpoint work and report OPEN.

Inspect current conventions first. Build the minimum configuration, app entry point, request/response models, routes, CORS and standard error handling needed by the existing project. Use the exact four approved route contracts: POST /api/v1/sessions, GET /api/v1/sessions/{session_id}, POST /api/v1/turns, POST /api/v1/voice/turns. Follow actual repository paths rather than assumptions in an old report. Use the canonical fixtures for mock behavior if they exist. Keep MOCKED data clearly distinguishable and never score it as a real assessment.

Do not add a second API contract, alter frozen fixture shapes, invent validation rules, change the frozen error envelope, or implement hidden eligibility logic. Keep secrets server-side. Do not edit frontend, data, sources, or unrelated docs.

After the slice, run only relevant available checks. Report exact files changed, exact commands and observed results, endpoints exercised, mock/real state, deviations, and OPEN items. Do not claim success for an unrun check. Wait before proceeding to persistence/graph work.
```

## Prompt D — Ankush-owned persistence foundation

```text
Implement the approved persistence foundation, with Ankush as sole owner of backend database wiring. First inspect any existing migrations/schema and the currently approved architecture/database decision. Do not assume that a proposed table list is approved DDL.

Before creating migrations or tables, verify the agreed schema, allowed session/turn/assessment fields, retention/deletion behavior, access policy, vector dimension if applicable, and environment configuration. If any item is unresolved or requires a new frozen decision, do not guess or apply a migration. You may implement an isolated configuration/connection adapter only when its behavior follows the approved architecture and does not depend on the missing schema.

Implement only agreed persistence operations and repository abstractions. Coordinate data ownership with Anamika; do not edit her source/rule data. Do not store raw audio by default; do not collect Aadhaar or bank numbers. Ensure failures cannot be reported as successful writes and do not leak connection details.

Run relevant checks that do not require unauthorized external mutation. Never connect to or modify a live database unless the environment and action are explicitly authorized. Report changed files, whether anything was applied to a database (normally no), actual checks, and unresolved schema/privacy decisions. Stop before H2/H3 integration if the interface is not approved.
```

## Prompt E — H2 graph and H3 deterministic eligibility adapter

```text
Implement H2 orchestration and the H3 adapter only against the inspected, agreed contracts. Start by restating the exact graph callable/state and the agreed eligibility module path/signature/output. If the reviewed artifacts or teammate agreement do not define them, stop and return a short proposed interface for team approval; do not write code that guesses.

Keep the graph responsible for orchestration, not for reimplementing eligibility. Call Anamika’s deterministic PMUY engine through the agreed adapter. Preserve PMUY-only assessment, frozen R01–R06/D01–D12 rules, D13 once through R03, R07 outside eligibility, and all unknown/unclear/contradictory/missing semantics. Never let generated text alter a deterministic result. Persist only agreed fields through Ankush’s repository adapter.

Match H2/H3 failure and result behavior exactly. Keep mock adapters labeled, isolated from real scoring, and replaceable without changing the public API. Do not expand scheme eligibility or alter external response shapes.

Run focused local checks against approved examples and actual PMUY test cases when available. Report actual results and wait for review before H4 integration.
```

## Prompt F — H4 official retrieval and grounded response

```text
Implement H4 retrieval integration only after confirming the approved H4 request/response contract, source/chunk metadata schema, database DDL and embedding configuration. List the exact sources and versions used. If any required field or behavior is unresolved, stop at that boundary and report OPEN instead of inventing it.

Use validated official material only. Preserve source ID, page/section, document version and retrieval date as required by the agreed contract. Keep samples/placeholders separate from real sources. Ensure missing evidence or retrieval failure produces the approved refusal/unknown behavior; never generate an unsupported factual answer or fake citation. Do not modify Anamika’s owned data/extraction files without an explicit handoff.

Do not apply schema changes to a live database. Verify retrieval with local/approved fixtures and record the exact queries, source results, observed behavior and limitations. Update evidence only with observed facts. Stop before speech work unless its interface is also agreed.
```

## Prompt G — Speech orchestration and API integration

```text
Wire speech into the backend only after the team has approved Anamika’s STT/TTS module paths, call signatures, audio formats, error behavior and retry/timeout policy. Do not choose a provider on her behalf or change her wrapper ownership.

Preserve the frozen voice-turn endpoint and response schema, including speech.audio_base64. Do not replace it with an audio URL or alter fields. Raw audio must not be persisted by default. A transcription/synthesis failure must follow the approved error/fallback behavior while keeping typed input and written response usable. Keep secrets server-side and avoid logging audio or sensitive transcripts.

Exercise only available local fixtures/stubs or explicitly approved provider calls. Report MOCKED versus REAL for each path and record actual checks. If a required format or contract detail is still OPEN, leave that adapter unconnected and report the exact agreement needed.
```

## Prompt H — Backend acceptance, evidence and handoff

```text
Perform the backend acceptance and handoff review. Do not add features or change frozen contracts during this pass.

Review your own diff for ownership, secrets, private data, raw-audio persistence, mock/real labeling, API contract drift, deterministic eligibility authority, source provenance/refusal, and error behavior. Run the relevant checks that are available and safe. Use exact authoritative PMUY-T01–T12 cases; if unavailable, leave those cases OPEN. Do not run destructive migrations or touch live services.

Update docs/BUILD_EVIDENCE_LOG.md only with observed commands, environment, revision, expected/observed behavior and evidence. Mark every path MOCKED, REAL, PARTIAL or NOT RUN. Do not invent metrics, results or deployment status.

Return: changed files; how to run locally; checks and actual results; API/graph/persistence/retrieval/speech state; outstanding OPEN items and owner; known limitations; reset/handoff steps; and next teammate action. Do not commit or push unless separately authorized.
```

## Ankush team gates

- **Before C:** repository/source inventory reviewed.
- **Before D:** schema and privacy/persistence decisions approved.
- **Before E:** H2 and H3 signatures agreed with Anamika.
- **Before F:** H4 schema and provenance handoff agreed with Anamika.
- **Before G:** speech interface agreed with Anamika and client format checked with Aditya.
- **Before completion:** evidence log reflects only actual checks; clean-start instructions reviewed by another teammate.
