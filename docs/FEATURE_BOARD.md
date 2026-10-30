# Yojana Mitra — Phase 5 Feature Board

**Status:** Planning baseline; no implementation status or test result is implied.  
**Schedule:** Actual dates/times and checkpoint mapping **OPEN — team confirmation**. Historical checkpoints are templates only.

Statuses: `NOT STARTED` / `IN PROGRESS` / `BLOCKED` / `DONE`; evidence maturity may additionally be `MOCKED`, `PARTIAL`, or `OPEN`. A task is DONE only with evidence recorded in `docs/BUILD_EVIDENCE_LOG.md`.

| ID | Feature / task | Owner | Priority | Dependencies | Expected output | Acceptance criteria | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P5-01 | Confirm authoritative source artifacts and repository baseline | Ankush; team for source owners | P0 | Phase 4.1/4.2 records | Linked/available frozen architecture, API, H1–H4, PMUY KB, T01–T12 | Exact sources verified; missing artifacts listed and not reconstructed | OPEN |
| P5-02 | Confirm actual schedule and gates | Ankush; team | P0 | Event rules/team availability | Dated checkpoint/freeze/demo/submission plan | Actual local times confirmed; adequate test/rehearsal buffer | OPEN |
| P5-03 | Shared API mock and frontend contract check | Ankush (API/mock); Aditya (client) | P0 | Phase 3.3 API and mock fixture | Contract-compatible mock path | Endpoints and response/error shapes match frozen API artifact; actual check logged | OPEN |
| P5-04 | H1 API session and turn path | Ankush; Aditya | P0 | P5-01, P5-03 | Session and text/voice API integration | Exact Phase 3.3 behavior; errors follow frozen envelope; test evidence recorded | OPEN |
| P5-05 | LangGraph orchestration / H2 | Ankush | P0 | H2 contract artifact | API-to-workflow path | Input/state/output and failure behavior match reviewed H2 contract; exact details OPEN until source available | OPEN |
| P5-06 | PMUY question bank and deterministic rules / H3 | Anamika (eligibility handoff); Ankush (integration) | P0 | PMUY Knowledge Base, H3, T01–T12 | Rule-based interview/evaluation module | R01–R06 and D01–D12 only; D13 once via R03; unknown/missing/contradictory handling per freeze; test outcomes logged | OPEN |
| P5-07 | Backend database wiring and persistence | Ankush | P0 | Approved persistence boundary; agreed data handoff | Backend database connection and workflow wiring | Uses agreed schema/fields; no raw audio by default; retention/deletion requirements addressed; exact schema OPEN | OPEN |
| P5-08 | Data, official-source ingestion and provenance | Anamika (data/ingestion); Ankush (retrieval integration) | P0 | Validated official documents; H4 | Source data and retrieval handoff | Official sources only; source ID, page/section, version, retrieval date retained; unsupported claims refused | OPEN |
| P5-09 | H4 retrieval seam and grounded response | Ankush (integration); Anamika (data handoff) | P0 | P5-08, H4 artifact | Workflow retrieval and provenance response | Exact request/response/storage fields follow H4 artifact; no invented claims; schema remains OPEN until inspected | OPEN |
| P5-10 | STT/TTS wrappers and fallback | Anamika (wrappers/benchmark); Ankush (workflow wiring); Aditya (client behavior) | P0/P1 **OPEN** | H1 and speech contract | Voice path with written fallback | Hindi/English behavior follows frozen language choice; speech failure preserves typed/written answer; provider and exact wrapper signatures OPEN | OPEN |
| P5-11 | Result and take-away card | Ankush (response integration); Aditya (UI) | P0 | Frozen API response; verified sources | User-facing result/card | Reasons, source references and indicative-not-official disclaimer shown; exact field mapping verified against Phase 3.3 | OPEN |
| P5-12 | Frontend core journey | Aditya | P0 | P5-03, P5-04 | Language, welcome, mode, conversation, result/card and error states | Hindi/English; shared voice/text session; text remains usable when speech fails; tested client evidence | OPEN |
| P5-13 | PMUY baseline tests T01–T12 | Anamika (rule test artifacts); Ankush (real API run) | P0 | PMUY KB and test definitions | Frozen baseline cases run and recorded | Preserve source cases and expected outcomes; do not invent cases; actual pass/fail by case recorded | OPEN |
| P5-14 | Integration, clean-start and deployment checks | Ankush (backend); Aditya (frontend); Anamika (rule/data verification) | P0 | P5-04–P5-13 | Reproducible demo path and reset instructions | Independent clean-start run, network/client check and actual deployment status recorded | OPEN |
| P5-15 | Evidence, limitations and claims audit | Anamika (evaluation); Ankush (log); Aditya (demo evidence) | P0 | Actual runs and measurements | Evidence log, measured claims and limitations | Every claim backed by linked evidence and labeled measured/estimated/target; no invented metrics | OPEN |
| P5-16 | Secondary scheme chips / info-only material | Ankush + Anamika | P1 **OPEN** | Current official-source validation | Validated info-only content or “coming soon” UI | No eligibility assessment; only enabled after source validation | NOT STARTED |
| P5-17 | My Conversations, Settings, Guest User, interactive demo screens | Aditya | P1/P2 **OPEN** | P0 path | Optional UI features | Only pursued after P0 and schedule review; each has separate acceptance detail OPEN | NOT STARTED |
| P5-18 | Image/PDF card export and visual polish | Aditya; Ankush for response support if needed | P2 **OPEN** | P0 result/card | Optional export/polish | Only after protected P0 and evidence; acceptance detail OPEN | NOT STARTED |

## Ownership note

Ankush owns backend database wiring under the Phase 4.2 briefs and the explicit Phase 5 instruction. A conflicting Phase 4.5 prompt block assigning `backend/app/database` to Anamika is not adopted. Anamika owns data, eligibility, speech wrappers, evaluation artifacts, and agreed handoff modules. Shared folder edits and exact module boundaries require coordination; do not infer ownership from a broad path label.
