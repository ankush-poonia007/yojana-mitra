# Antigravity Build Guide — Anamika

**Role:** Data, deterministic eligibility, speech wrappers, ingestion/evaluation artifacts and agreed handoff modules  
**Companion documents:** `YOJANA_MITRA_MASTER_BRIEF.md`, `PHASE_4.2_PERSONAL_BRIEFS.md`, `DECISIONS.md`, `docs/PHASE_5_IMPLEMENTATION_PLAN.md`, `docs/FEATURE_BOARD.md`, `shared/INTEGRATION_CONTRACTS.md`, `docs/TEST_ACCEPTANCE_MATRIX.md`, `docs/BUILD_EVIDENCE_LOG.md`  
**Schedule:** Confirm actual event times with the team. Historical times are templates only.

## Mission

Deliver verifiable PMUY rule/data artifacts, deterministic eligibility behavior, official-source ingestion handoffs, speech STT/TTS wrappers and evaluation evidence. Keep the rule engine deterministic and separate from generated explanation. Hand backend integration and persistence changes to Ankush through an agreed seam. Ankush owns backend database wiring.

## Read before editing

1. Read root `AGENTS.md`; all files under `sources/` are read-only.
2. Read `DECISIONS.md`, `PHASE_4.2_PERSONAL_BRIEFS.md`, `YOJANA_MITRA_MASTER_BRIEF.md`, `ui_userflow.md`, and all five Phase 5 documents.
3. Locate the authoritative PMUY Knowledge Base, Research Analysis, T01–T12 cases, reviewed H3/H4 contracts, and speech handoff details. The exact artifacts were not present in the inspected project copy. Do not reconstruct rule text, thresholds, questions, tests, or source claims if those files are missing.
4. Inspect the existing repo and owner boundaries before choosing files. Coordinate backend module paths with Ankush before editing outside `data/`.

## Ownership

**You own:** `data/` source documents and extracted text, scheme metadata/rule artifacts, question bank and deterministic eligibility implementation/handoff, agreed ingestion/data modules, STT/TTS wrappers, benchmark and evaluation/scorecard artifacts, and tests for these owned components.

**You do not own:** backend database wiring, backend routes, API schemas, graph/orchestration, frozen H1–H4 contracts, Aditya’s frontend, or `sources/`. The Phase 4.5 block that assigns `backend/app/database` to you conflicts with Phase 4.2 and the explicit Phase 5 decision. Do not implement or take ownership of that database wiring. Coordinate schema and persistence handoffs with Ankush.

## Frozen product and rule constraints

- PMUY is the only scheme with full eligibility assessment. Other listed schemes are information-only only after official-source validation; no additional eligibility engine is authorized.
- Use the PMUY Knowledge Base as authority for exact policy/rule language and values. The source is currently **OPEN/unavailable in this project copy**.
- Frozen decisions: rules R01–R06; declarations D01–D12; D13 evaluated once via R03; R07 belongs to application readiness/verification, not eligibility. Follow D3 for R05 clear failure versus uncertain answers. R06 domestic PNG interpretation remains subject to distributor confirmation.
- Preserve separate eligibility, verification and application-readiness dimensions. Missing documents affect readiness, not eligibility.
- Never coerce unknown, unclear, contradictory or missing answers to “No,” a favorable answer or a pass. Keep uncertain outcomes as `cannot_determine` per authoritative contract.
- The deterministic Python engine owns eligibility. LLM-generated prose cannot change it.
- Eligibility is indicative, never an official determination. Do not add private-record lookups or request/store Aadhaar or bank numbers.
- Retrieval/data artifacts must use validated official documents only and carry source ID, page/section, version and retrieval date. Never invent citations or document currency.
- Do not persist raw audio by default. Retention/deletion requirements must be documented before deployment.
- No STT provider is selected. Benchmark Gemini transcription, Whisper Large V3 and Whisper Large V3 Turbo under recorded, comparable conditions; report a winner only from actual measurements.

## Build sequence

### 1. Source and ownership audit

- List available authoritative source files, their version/date/provenance, and missing materials. Distinguish approved source from placeholder/example.
- Map work to Feature Board IDs and identify the exact files you own. Agree any backend handoff paths and public interfaces with Ankush before implementation.
- Confirm actual event schedule. Historical 1:00 AM, 2:30 AM, 5:30 AM, 8:00 AM and 9:00 AM targets are not current deadlines by themselves.
- Provide a short plan with files, dependencies and checks. Pause any rule-sensitive work when the authoritative source is missing; continue independent wrappers/fixture scaffolding only if it does not invent contract details.

### 2. PMUY data and deterministic eligibility

- Build the question bank and rule mapping directly from the authoritative source. Preserve the approved interview sequence and answer distinctions; do not create new policy.
- Implement the deterministic engine only after confirming the H3 function, argument and result schemas with Ankush from the reviewed artifact.
- Keep `likely_eligible`, `likely_not_eligible`, and `cannot_determine` semantics aligned with the frozen contract. Keep rule IDs/source IDs attached to reasons as required by the approved handoff.
- Make missing, contradictory and unclear answers explicit. Verify D13 is counted once through R03 and keep R07 out of the eligibility determination.
- Do not encode the frozen rule summary as a substitute for absent source definitions, assessment dimensions or question wording.

### 3. Official-source ingestion and evidence handoff

- Prepare source inventory and provenance data from official documents only. Capture the required source identifier, URL where available, page/section, document version and retrieval date without fabricating missing values.
- Prepare extracted text and chunk/evidence handoffs for Ankush. Coordinate chunk format, tables, embeddings, metadata and idempotency before writing integration code; exact H4/schema details are OPEN.
- Make source currency review visible. Declaration revision currency and domestic PNG interpretation are unresolved; do not claim independently verified current policy.
- Keep examples and mock evidence labeled; never mix mock sources into real evaluation.

### 4. Speech wrappers and benchmark

- Confirm the speech interface with Ankush before selecting wrapper names, audio formats, return schemas, retries or timeouts. These details are OPEN unless the reviewed contract resolves them.
- Implement STT/TTS as isolated wrappers within your agreed files. Preserve Hindi/English behavior and ensure service failure leaves typed input and written answer available.
- Benchmark Gemini transcription, Whisper Large V3, and Whisper Large V3 Turbo with the same recorded Hindi test sentences and comparable conditions. Document test material provenance, device/noise/accent conditions, sample size, method, raw observations and measured result. Do not fabricate a winner or accuracy number.
- Preserve frozen API output including `speech.audio_base64`; only Ankush changes API wiring, and neither owner changes the response contract without amendment.
- Do not save raw audio by default. Test fixtures must not contain sensitive personal data.

### 5. Tests and scorecard

- Retrieve the authoritative PMUY-T01–T12 definitions and preserve them unchanged. If missing, leave each case OPEN and do not invent replacements.
- Add component tests only for behavior defined by the authoritative KB and agreed interface. Include unknown/missing/contradictory handling only where test intent is specified; label any new engineering checks separately from frozen PMUY cases.
- Record correct-with-source, correct-refusal, card completeness, speech transcription and time-to-card only after metric definitions and actual runs are agreed. Keep target, estimate and measured values distinct.
- Record actual results, failures, environment, revision and evidence links in `docs/BUILD_EVIDENCE_LOG.md`. Never report a test as passed from inspection alone.

### 6. Handoff and acceptance

- Deliver to Ankush the agreed module path, exact callable signature, input/output schema, success/failure behavior, dependency/environment needs, mock fixture and actual component test evidence.
- Do not change another owner’s API or database implementation to make your component fit. Raise a mismatch with concrete producer/consumer examples and request agreement.
- Report completed work, mock/real boundaries, measured results, limitations, missing source/contract artifacts, and next integration owner. Keep all unresolved items OPEN.

## Acceptance for your assignment

- Rules and question bank are traceable to the authoritative PMUY Knowledge Base; no guessed definitions or values.
- Deterministic outcomes respect unknown/contradictory/missing semantics, D13/R03 handling and R07 boundary.
- Official-source evidence retains required provenance; placeholders are not represented as sources.
- Speech wrappers follow the agreed interface, preserve typed/written fallback and do not change frozen API response shape.
- STT comparison is reproducible and only measured outcomes are stated.
- T01–T12 are unchanged and actual outcomes are recorded only after execution.
- Database wiring remains Ankush-owned; your handoffs and file boundaries are explicit.

## Ready-to-paste Antigravity prompt

```text
You are implementing Anamika’s assigned Yojana Mitra Phase 5 work. Follow docs/ANTIGRAVITY_ANAMIKA_BUILD_GUIDE.md and read root AGENTS.md, DECISIONS.md, PHASE_4.2_PERSONAL_BRIEFS.md, YOJANA_MITRA_MASTER_BRIEF.md, ui_userflow.md, docs/PHASE_5_IMPLEMENTATION_PLAN.md, docs/FEATURE_BOARD.md, shared/INTEGRATION_CONTRACTS.md, docs/TEST_ACCEPTANCE_MATRIX.md, and docs/BUILD_EVIDENCE_LOG.md before editing.

Treat sources/ as read-only. Inspect the actual repository and source artifacts first. Report a concise plan with the files you own, dependencies, checks, and missing authoritative inputs before coding. Do not overwrite existing work or edit files outside your ownership without a specific agreed handoff.

Your scope is data, official source inventory/extracted data, deterministic PMUY eligibility/question bank, agreed ingestion/data modules, STT/TTS wrappers, benchmarks and evaluation artifacts. Ankush owns backend routes, schemas, graph/orchestration, retrieval integration and backend database wiring. Do not implement backend/app/database: an older Phase 4.5 prompt assigns it to you, but that conflicts with Phase 4.2 and the explicit Phase 5 ownership decision. Coordinate persistence and module handoffs with Ankush. Aditya owns frontend.

Frozen constraints: PMUY is the only fully assessed scheme; no other scheme eligibility engine. Use the authoritative PMUY Knowledge Base for exact rule values and questions. Preserve R01–R06, D01–D12, D13 once through R03, and keep R07 in readiness/verification outside eligibility. Preserve R05 uncertainty semantics and R06’s pending distributor confirmation. Unknown, unclear, contradictory or missing data must not become No/pass. Keep eligibility, verification and readiness separate. Rules are deterministic; generated text cannot alter outcomes. Use validated official sources with provenance and no fabricated citations. Do not persist raw audio by default or include secrets/Aadhaar/bank data in code, logs or fixtures. Preserve Hindi/English user-selected language behavior and frozen API response including speech.audio_base64.

The PMUY Knowledge Base, T01–T12 definitions and detailed H3/H4/speech schemas may be absent. Do not guess. Mark the dependent item OPEN, report the missing artifact, and proceed only with independent work that does not invent rule or contract behavior. Do not change a frozen decision without an explicit amendment.

Build in this order: (1) verify source/version and owned paths; (2) implement source-traceable PMUY data and deterministic rules from the authoritative KB; (3) agree and implement the exact eligibility handoff with Ankush; (4) prepare validated official-source ingestion/evidence handoffs; (5) agree and implement isolated STT/TTS wrappers and fallback behavior; (6) benchmark Gemini transcription, Whisper Large V3 and Whisper Large V3 Turbo using comparable recorded Hindi samples; (7) run unchanged T01–T12 only after retrieving their definitions; (8) document actual results and handoff details. Adjust for real repository dependencies and explain why.

Before finishing, inspect your own diff and ownership. Run only appropriate available checks; report exact commands and observed outcomes. Update BUILD_EVIDENCE_LOG.md only with actual evidence. Never invent pass results, policy, accuracy, metric values, provider winner or source currency. Finish with files changed, handoff signature and dependencies, checks/results, measured benchmark (if actually run), OPEN items and next owner. Do not commit or push unless separately asked.
```
