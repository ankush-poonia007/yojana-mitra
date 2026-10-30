# Phase 4.2 — Personal Briefs

**Status: documented; review pending. Not frozen.** These briefs follow `YOJANA_MITRA_MASTER_BRIEF.md`, `DECISIONS.md` (frozen Phase 4.1), and the read-only roadmap. Checkpoint times below are the requested team gates; the roadmap's original 9:00 PM, midnight, 3:00 AM, 6:00 AM, and 9:00 AM gates remain in force. A brief does not certify that a deliverable has been built.

## Ankush — Team lead, backend orchestration and integration

**Objective:** Deliver the FastAPI-to-workflow path and integrate the grounded PMUY experience without changing frozen Phase 3.2/3.3 contracts.

**Receives:** Master Brief §§4–12; frozen H1–H4 boundary record in `DECISIONS.md`; Phase 3.3 endpoints and response summary in Master Brief §8; Anamika's engine/data/retrieval handoffs; Aditya's frontend and shared mock. Detailed contract artifacts/schemas are not in this project copy.

**Checkpoints (yes/no):** **2:30 AM thin slice** — mock-mode session → turn → standard response traverses the app path and renders in Aditya's client. **5:30 AM first real end-to-end** — one typed PMUY turn traverses real API/workflow, deterministic assessment and official-source retrieval, returning response/card/sources; record pass/fail. **8:00 AM P0 basic** — Hindi typed/voice routes, grounded/refusal behavior, assessment, spoken/on-screen answer and card have a runnable basic path; unimplemented parts are explicitly listed. **9:00 AM freeze** — freeze announcement made; only critical bug fixes thereafter; clean-start handoff, deployment or stable local setup, second-device/network check, reset instructions and known limitations recorded. Roadmap 6:00 AM is the core feature freeze; 9:00 AM is tested/deployed gate.

**Own:** `backend/` routes, schemas, graph, services, retrieval integration, eligibility integration and database wiring; `docs/`; integration/merge coordination; root `.env.example`, `.gitignore`, `README`. **Do not touch:** `sources/`; Aditya's `frontend/`; Anamika's `data/` without a coordinated handoff; frozen decisions/contracts without an explicit amendment.

**Interfaces provided/called — shared H1–H4 contract (same wording in Anamika brief):** **H1 Frontend ↔ API:** provider FastAPI; caller React/TypeScript frontend. Documented endpoints: `POST /api/v1/sessions`, `GET /api/v1/sessions/{session_id}`, `POST /api/v1/turns`, `POST /api/v1/voice/turns`; standard response keys are in Master Brief §8. **H2 API ↔ LangGraph:** provider/caller boundary is API ↔ graph; exact invoke function, graph input/output schema and node names are **OPEN**. **H3 LangGraph ↔ Eligibility Engine:** graph calls deterministic Python PMUY engine; exact function name, arguments and return schema are **OPEN**. **H4 LangGraph ↔ Retrieval:** graph calls official-source retrieval; exact function name, request/response schema and storage tables are **OPEN**. These are boundary facts, not reconstructed detailed contracts. **Mock from 1:00 AM:** coordinate a schema-compatible sample API response and `MOCK_MODE`; exact mock filename is OPEN. Do not score mock assessments as real.

**Acceptance / solo check:** endpoint/error shapes follow §8; deterministic result is not overridden by generated text; sources are official/provenanced or unsupported claims are refused; run API in mock mode then a real typed turn and inspect response/card/source/error paths.

**Out of scope:** private-record lookup, application submission, offline/P1/P2 work, expanding scheme eligibility beyond PMUY, inventing unavailable contract/rule/test details. **Stuck:** after 30 minutes, ask the counterpart owner first (Anamika for data/rules/retrieval, Aditya for client/H1); escalate unresolved cross-team/interface blockers to the team and record them **OPEN**.

## Anamika — Backend data, rules, persistence, ingestion, speech and testing

**Objective:** Supply verifiable PMUY rule/data and speech/testing components that preserve deterministic eligibility and official-source provenance.

**Receives:** Master Brief §§6–11; frozen D1–D14 and H1–H4 boundaries in `DECISIONS.md`; Ankush's documented engine/retrieval handoff when available; PMUY Knowledge Base and T01–T12 are referenced but absent here, so their contents must not be reconstructed.

**Checkpoints (yes/no):** **2:30 AM thin slice** — a labeled mock rule result and evidence record can pass through the agreed backend seam; seam/schema remains OPEN until supplied. **5:30 AM first real end-to-end** — one source-backed PMUY case and one unknown/ambiguous case run against verified rules and persist only the agreed session data; show outputs and provenance. **8:00 AM P0 basic** — PMUY question/rule mapping, official document ingestion, Supabase persistence, STT benchmark/wrapper, TTS wrapper, and baseline test/scorecard path are runnable or individually marked OPEN; no result claimed without evidence. **9:00 AM freeze** — deliver reproducible data/rule/test artifacts and measured benchmark/results; freeze announcement respected, critical fixes only. Roadmap 6:00 AM is core feature freeze; 9:00 AM is tested/deployed gate.

**Own:** `data/` documents, extracted text, scheme metadata/rules and evaluation artifacts; backend eligibility/data-ingestion/speech components only by agreed file handoff. **Do not touch:** `sources/`; frontend; Ankush-owned routes/graph/API schemas/database wiring; frozen rules/contracts. Never fill gaps in absent Knowledge Base/T01–T12 by guess.

**Interfaces provided/called — shared H1–H4 contract (same wording in Ankush brief):** **H1 Frontend ↔ API:** provider FastAPI; caller React/TypeScript frontend. Documented endpoints: `POST /api/v1/sessions`, `GET /api/v1/sessions/{session_id}`, `POST /api/v1/turns`, `POST /api/v1/voice/turns`; standard response keys are in Master Brief §8. **H2 API ↔ LangGraph:** provider/caller boundary is API ↔ graph; exact invoke function, graph input/output schema and node names are **OPEN**. **H3 LangGraph ↔ Eligibility Engine:** graph calls deterministic Python PMUY engine; exact function name, arguments and return schema are **OPEN**. **H4 LangGraph ↔ Retrieval:** graph calls official-source retrieval; exact function name, request/response schema and storage tables are **OPEN**. These are boundary facts, not reconstructed detailed contracts. **Mock from 1:00 AM:** coordinate a schema-compatible sample API response and `MOCK_MODE`; exact mock filename is OPEN. Do not score mock assessments as real.

**Acceptance / solo check:** rule result stays deterministic; unknown is not coerced to “No”; evidence records official source ID/page or section/version/retrieval date; run rule examples only from authoritative artifacts, ingestion/provenance checks, STT comparison (Gemini transcription, Whisper Large V3, Whisper Large V3 Turbo), TTS wrapper check and available PMUY-T01–T12 unchanged. If source/tests unavailable, report OPEN rather than pass.

**Out of scope:** choosing an unmeasured STT winner, inventing policy, private-record checks, expanding eligibility to other schemes, changing API/graph contracts unilaterally. **Stuck:** after 30 minutes, ask Ankush first for backend seam/persistence/retrieval; ask the team for missing authoritative rule/source material; log unresolved issues OPEN.

## Aditya — Frontend, voice/text interface, result card and deck

**Objective:** Deliver an accessible voice/text client that guides a user from input to an understandable, sourced PMUY result and take-away card.

**Receives:** Master Brief §§4, 8–10 and `ui_userflow.md`; H1 boundary and Phase 3.3 paths/response summary; Ankush's API/mock; Anamika's result/source/card examples when available. Exact visual design and full H1 schema are not present in this project copy.

**Checkpoints (yes/no):** **2:30 AM thin slice** — mock-backed typed turn renders user/assistant exchange and a result/card state. **5:30 AM first real end-to-end** — live API typed turn displays response, assessment, source and card; errors remain recoverable. **8:00 AM P0 basic** — Hindi voice/text path, transcript/typed fallback, spoken/on-screen answer, likely eligible/not eligible/cannot tell yet, indicative caveat and source-linked card work at basic level; missing capabilities listed. **9:00 AM freeze** — feature freeze observed; clean-start walkthrough works on small screen, known limitations and deck draft are ready; only critical fixes thereafter. Roadmap 6:00 AM core freeze and 9:00 AM tested/deployed gate remain.

**Own:** `frontend/`; shared client examples/mock fixtures only by agreement; deck/presentation files (exact path OPEN). **Do not touch:** `sources/`; backend routes/graph/data/rules or frozen H1 schema; do not send live AI requests from scripted onboarding demo.

**Provides/calls:** calls H1 endpoints `POST /api/v1/sessions`, `GET /api/v1/sessions/{session_id}`, `POST /api/v1/turns`, `POST /api/v1/voice/turns`; response fields per Master Brief §8. Provides UI behavior and mock rendering for those documented shapes. Exact component/function names and mock fixture path are **OPEN**. H2–H4 are backend-to-backend, not called directly by frontend. **Mock from 1:00 AM:** use a clearly labeled schema-compatible sample response coordinated with Ankush; file/name OPEN.

**Acceptance / solo check:** voice and typed fallback, preserved conversation across mode switch, visible source/date when available, indicative caveat, understandable missing information and safe error/loading states; run the client against mock response then API success/failure examples. **Out of scope:** eligibility decisions, fabricated citations, P1 card export/helper mode, P2 offline/SMS, live backend internals. **Stuck:** after 30 minutes, ask Ankush first for H1/API/mock issues, Anamika for verified rule/card content; escalate unresolved blockers to team and mark OPEN.

## Caller / callee matrix

| Interface | Caller | Callee / provider | Defined here | OPEN |
|---|---|---|---|---|
| H1 Frontend ↔ API | Aditya's React/TypeScript frontend | Ankush's FastAPI app | Four endpoint paths and response summary (§8) | Detailed schemas/examples, client function names, mock file path |
| H2 API ↔ LangGraph | FastAPI route/orchestration | LangGraph workflow | Boundary only | Invoke function, graph state/input/output, node names |
| H3 LangGraph ↔ Eligibility Engine | LangGraph workflow | Deterministic Python PMUY engine (Anamika rule/data contribution; integration owner Ankush) | Boundary and deterministic role | Function, args, return schema |
| H4 LangGraph ↔ Retrieval | LangGraph workflow | Official-source retrieval service (Anamika source/data contribution; integration owner Ankush) | Boundary and provenance requirement | Function, request/response schema, tables |
| Mock API response | Frontend and API integration | Coordinated sample fixture | Mock/real schemas must match; `MOCK_MODE` exists | Exact artifact path/name and payload contract |

## OPEN — unowned or unresolved work

- Detailed H1–H4 artifacts are reported reviewed in the conversation but are not present in this project copy; attach/link them before relying on details beyond the Master Brief summary.
- Exact internal function names, detailed schemas, node names/order, mock file path, deck path, and shared fixture owner are not specified. Do not silently assign or invent them.
- PMUY Knowledge Base, PMUY-T01–T12, exact question bank/rule values, Supabase DDL, document freshness procedure, speech provider selection, privacy/retention policy, and reset procedure remain unresolved or unavailable as recorded in the Master Brief/decision record.
- Phase 4 roadmap setup items (branches, Antigravity instructions, base-project setup) have no owner established in available documentation: OPEN.
