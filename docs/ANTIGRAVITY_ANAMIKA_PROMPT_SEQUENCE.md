# Antigravity Prompt Sequence — Anamika

**Purpose:** Copy these prompts into one Antigravity conversation in order to implement Anamika’s Phase 5 data, eligibility, speech and evaluation work. Use each prompt only after reviewing the prior stage’s output.

**Role guide:** `docs/ANTIGRAVITY_ANAMIKA_BUILD_GUIDE.md`  
**Ownership rule:** Anamika owns data, eligibility, speech wrappers and agreed handoff modules. Ankush owns backend database wiring, API routes/schemas and orchestration. `sources/` is read-only.

## How to use this sequence

1. Start with Prompt A, which audits authoritative PMUY materials and owned files without edits.
2. Use Prompt B to prepare and agree module interfaces with Ankush before shared backend work.
3. Run Prompts C–G in order where applicable. Rule/data work can proceed while speech inputs are pending.
4. Do not write an unresolved policy or interface as if it were approved.
5. Use Prompt H to record evidence and hand off completed modules.

---

## Prompt A — Source and repository audit (read-only)

```text
You are Anamika, responsible for Yojana Mitra data, deterministic PMUY eligibility, speech wrappers, ingestion handoffs and evaluation. Follow docs/ANTIGRAVITY_ANAMIKA_BUILD_GUIDE.md and root AGENTS.md. This stage is READ ONLY: do not edit, create, move, delete, install, or run provider calls.

Identify the active repository root. Inspect the PMUY Knowledge Base, research analysis, official source register, frozen decisions, test cases T01–T12, current data tree, existing code and relevant API/H3/H4 contract files. Treat sources/ as read-only. Verify which source artifacts actually exist in this checkout; distinguish the source documents from summaries.

Return: authoritative files and source versions found; PMUY rules/tests available; existing owner-controlled code/data; missing sources or confirmations; proposed owned paths; dependency and privacy risks; and work safe to start immediately. Confirm that Ankush owns backend database wiring and that you will not edit database connection, migrations or repository wiring. Do not infer any rule or source currency not stated by inspected evidence.
```

## Prompt B — Interface agreement and work plan (no code)

```text
Using the repository audit and Anamika guide, write a file-by-file plan. PLAN ONLY; no code or data files yet.

Separate work into: (1) source/rule/question artifacts; (2) pure deterministic eligibility engine and tests; (3) official document extraction/provenance handoff; (4) STT/TTS wrappers; (5) benchmark/evaluation and evidence. For each task list output, exact source, file ownership, dependencies, and acceptance evidence.

Prepare interface questions for Ankush, without inventing answers: exact H3 module path/callable/input/return/error behavior; engine file versus Ankush adapter ownership; H4 chunk and provenance fields plus approved database schema; STT/TTS wrapper paths/signatures/audio formats/errors; who owns component test locations; and mock/real labeling. Treat each unanswered item as OPEN. Recommend an implementation order that allows isolated rule work to begin without database wiring. End with the exact decisions Ankush must confirm. No files edited.
```

## Prompt C — Rule, question and scheme artifacts

```text
Implement the PMUY rule/question/source metadata artifacts only from the authoritative Knowledge Base and approved decision record. First list the exact source sections used and the target owned files. If the source is missing or a definition conflicts with the frozen decisions, stop that item and report OPEN.

Represent only the approved PMUY scope. Preserve R01–R06, D01–D12, evaluate D13 once through R03, and keep R07 in readiness/verification outside eligibility. Preserve exact source wording/threshold meaning, language strings, question order and uncertainty distinctions from the authoritative material. Do not create eligibility rules for PM-KISAN or PM-JAY 70+. Do not claim declaration revision currency or resolve the R06 distributor question without evidence.

Keep source IDs, page/section, version and retrieval date traceable. Do not place secrets or real personal data in fixtures. Do not alter frozen project documents. After editing, report each rule/question and its source reference, changed files, unresolved source questions and checks actually performed. Do not report a test pass unless executed.
```

## Prompt D — Pure deterministic eligibility engine and baseline cases

```text
Implement the PMUY eligibility engine in the agreed Anamika-owned module/path. First confirm in the conversation the H3 callable name, input representation, result type and error behavior agreed with Ankush. If there is no agreement, implement a pure internal engine only if it can remain isolated from that public seam; do not invent the integration contract.

Use the authoritative PMUY Knowledge Base and preserve the frozen decision record. The deterministic engine alone determines eligibility. Unknown, unclear, contradictory and missing answers must never become “No”, a favorable answer or a pass. A clear R05 failure versus an uncertain R05 answer follows D3. D13 is evaluated once through R03. R07 must not affect eligibility; missing documents affect readiness, not eligibility. Keep eligibility, verification and application readiness distinct, but do not invent output schema or extra dimensions beyond approved sources/contracts.

Transcribe PMUY-T01–T12 exactly from their authoritative definitions and preserve expected outcomes. Do not replace, paraphrase or supplement these cases as if frozen. New edge checks must be clearly labeled additional engineering tests. Run focused tests if dependencies are available and appropriate. Report commands and actual results, source traceability, limitations and any unresolved conflict. Do not touch Ankush’s database wiring or graph.
```

## Prompt E — Official document extraction and H4 handoff

```text
Prepare official-source data/extraction artifacts and a handoff for Ankush. First inspect the agreed H4 contract and approved chunk metadata schema. If unavailable, produce only a source inventory or extraction package whose fields are already specified by an authoritative source; do not invent a database row schema, embedding dimension or retrieval request.

Use only validated official sources for factual content. For each source/chunk preserve the approved provenance: source identifier, title/URL where available, page/section, document version and retrieval date. Clearly flag missing provenance. Keep placeholders and examples out of real retrieval datasets. Do not claim that a source is current when currency is unconfirmed. Keep PMUY-only assessment scope; other schemes may be informational only after current-source validation.

Do not create or modify backend database wiring, migrations, tables or access policies; Ankush owns them. Deliver an exact file list and handoff describing source inventory, field meanings, extraction method, known gaps, and the H4 questions still OPEN. Never fabricate a source or evidence.
```

## Prompt F — STT/TTS wrappers and benchmark

```text
Implement isolated STT/TTS wrappers only in the paths and signatures agreed with Ankush. First restate the provider interface, supported audio formats, language values, timeouts/retries and result/error models. If any are undecided, keep the wrapper isolated behind a clearly documented internal boundary and do not wire it into the API or change the frozen response schema.

Preserve Hindi/English behavior and typed/written fallback. Preserve the frozen API response including speech.audio_base64; Ankush owns API integration. Do not persist raw audio by default, place audio containing personal information in fixtures, or log raw audio/transcripts. Keep provider keys server-side.

Benchmark Gemini transcription, Whisper Large V3, and Whisper Large V3 Turbo only when an agreed comparable Hindi audio set is available. Use identical inputs and document source/consent, device, noise/accent conditions, sample count, method, failures and measured observations. Do not fabricate a result or select a winner before actual comparison. If audio samples are not available, finish independent wrapper scaffolding and report benchmark OPEN.

Run only relevant safe local checks and report exact commands/results, MOCKED versus REAL status, and unresolved integration inputs.
```

## Prompt G — Component evaluation and source/rule review

```text
Review Anamika-owned data, rule engine, questions, source chunks and speech components against authoritative source material and frozen decisions. Do not refactor unrelated modules or change frozen contracts.

For every rule R01–R06, declaration D01–D13, and baseline case T01–T12, show source reference, implementation location, test coverage and any discrepancy. Verify D13/R03 single evaluation; R07/readiness separation; unknown/missing/contradictory handling; no favorable coercion; source provenance; and no raw-audio persistence by default. Separate policy discrepancy from implementation bug. If a source itself is unclear, mark it OPEN and identify the source authority needed; do not resolve it by guessing.

Record only tests actually run in docs/BUILD_EVIDENCE_LOG.md. For scorecard measures, state the precise numerator, denominator, corpus and method before reporting values. Mark all numbers MEASURED, ESTIMATED or TARGET, with evidence. Finish with issues ranked by effect on correctness and handoff owner.
```

## Prompt H — Handoff and completion report

```text
Prepare Anamika’s Phase 5 handoff to Ankush and the team. Make no new feature changes in this stage.

List each delivered module/artifact and exact path; its authoritative source; agreed callable signature/schema; dependencies and environment needs; success/failure and unknown behavior; test command and actual result; mock/real status; provenance; and known limitations. Separate completed, partial, blocked, and not-run work.

Confirm explicitly that no backend database wiring, API routes/schemas, or graph orchestration were changed. Identify every OPEN H3/H4/speech question and who must decide it. Update the evidence log only with observed facts. Do not claim currency, benchmark winner, accuracy or passing tests without evidence. Do not commit or push unless separately authorized.
```

## Anamika team gates

- **Before C:** authoritative source inventory reviewed; only source-backed rules enter data files.
- **Before D integration:** H3 module path and types agreed with Ankush.
- **Before E import:** H4 chunk schema/database target agreed; Ankush applies database changes.
- **Before F API wiring:** wrapper signatures/audio format/error behavior agreed with Ankush; browser needs checked with Aditya.
- **Before benchmark claims:** comparable non-sensitive audio set and method exist.
- **Before completion:** frozen cases remain unchanged and evidence is actual.
