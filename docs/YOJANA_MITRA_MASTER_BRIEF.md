# Yojana Mitra — Master Brief
**Phase 4.1 · 30 October 2026 · Source-constrained consolidation**

**Authority:** Phase 3.3 governs interfaces; the PMUY knowledge base governs eligibility rules. That knowledge base is unavailable. Local references: `sources/DECISIONS.md`, `sources/Yojana Mitra Hackathon Roadmap & Checklist.md`, `ui_userflow.md`. Project files under `sources/` are read-only.

## 1. Problem, user and evidence
- **FACT:** Intended primary user is a farm household member who prefers speaking to reading; task is understanding likely eligibility, missing details, documents and application destination. Persona is unvalidated.
- **FACT:** Canvas records 488 million of 886 million Indian internet users as rural (IAMAI-Kantar, 2024) and 17,467,074 Kisan Call Centre calls over about three years to mid-2021 (government statement, 2021).
- **ASSUMPTION:** Scattered written information contributes to repeat trips, waiting, fees, document mistakes or delayed benefits; a gap after existing tools remains.
- **NEEDS VERIFICATION:** Venue interviews, competitor comparison, Bharat-VISTAAR expansion, current sources, user demand and speech performance in noise/accent conditions.

## 2. Solution, USP and what we will not build
Voice-first, text-supported assistant asks rule-relevant questions, reports “likely eligible”, “likely not eligible” or “cannot tell yet”, explains missing information and provides a source-linked take-away card. Indicative only; not an official decision.
**USP:** interviews rather than only lecturing; actionable documents/where-to-apply/source card; measured trust scorecard. Voice and citations alone are not claimed unique.
**Out of scope:** private-record lookups (Aadhaar/payment status), application submission, medical/legal/crop advice, 22 languages, offline, SMS/WhatsApp before P2. Exact source example: “I don't know; ask your panchayat”.

## 3. Scope
| Priority | Recorded scope |
|---|---|
| P0 | Hindi spoken/typed input + STT; dated official documents for 5–8 schemes; grounded sourced retrieval/refusal; eligibility interviews for 2–3 schemes; spoken/on-screen answer; take-away card; ~30-question scorecard. |
| P1 | Second language; save card image/PDF; helper mode; in-app scorecard. |
| P2 | Cached offline answers; WhatsApp/SMS; more schemes. |
PMUY as the only fully built scheme is requested, but not confirmed by available evidence. PM-KISAN and PM-JAY 70+ status is not stated. The canvas target (5–8 schemes, 2–3 interviewed) must be reconciled with PMUY-only build in OPEN.

## 4. User journey and screens mapped to API
| UX step/screen | API |
|---|---|
| Language/mode and start | POST /api/v1/sessions |
| Welcome and guided scripted practice | No API call; demo must not call live AI |
| Typed conversation | POST /api/v1/turns |
| Voice conversation | POST /api/v1/voice/turns (multipart); transcription enters shared workflow |
| Reopen session/history | GET /api/v1/sessions/{session_id} |
| Follow-up questions | Repeated text/voice turns in same session |
| Result/card/source | Standard turn response |
UX screens: language/welcome, guided demo, conversation (history, mode, mic, text fallback, source/audio controls), result/card, optional helper (P1). Exact visuals and demo screen-to-call mapping are absent.

## 5. Workflow and shared state
Contract stack names LangGraph, Gemini and deterministic Python eligibility. Shared state: session_id, language, input_type, user_text, intent, scheme_id, eligibility_answers, retrieved_evidence, assessment, response, error. Internal prompts/reasoning are not public.
**OPEN:** seven node names/order and Gemini-tier versus Python assignment are missing; do not infer them.

## 6. Eligibility engine
PMUY knowledge base is the eligibility authority but unavailable. Contract results: likely_eligible, likely_not_eligible, cannot_determine (UX wording “cannot tell yet”). Eligibility, verification and application readiness are three distinct dimensions; only eligibility result values are defined.
R01–R06, D01–D13, question sequence, rule mapping, stop conditions and verification/readiness definitions: **OPEN**. Contract examples are illustrative, not verified scheme rules.

## 7. Retrieval and knowledge
Stack: Supabase PostgreSQL, full-text search + pgvector, Supabase Storage. Retrieval fields: scheme_id, document_id, chunk_id, text, source_url, page, document_version; evidence references also title and section. Use official loaded documents, show source/date, ground claims and refuse beyond coverage; never fabricate a source. Exact tables/DDL and freshness process are OPEN.

## 8. API contract and examples
Base /api/v1; JSON except multipart audio; ISO 8601 timestamps; text/voice share workflow and response.
| Method/path | Input → output | Errors |
|---|---|---|
| POST /sessions | language, mode → session_id/status | 422, 500 |
| GET /sessions/{session_id} | id → session/turns | 404, 500 |
| POST /turns | session_id, text → standard turn | 400, 404, 503 |
| POST /voice/turns | multipart session_id, audio, optional language → standard turn + transcript | 400, 413, 503 |
Response keys: session_id, turn_id, status, language, answer.text, assessment, card, sources, speech; voice adds transcription.text/confidence. Assessment: scheme_id, result, reasons, missing_information. Example statuses: awaiting_information/completed.
Error envelope: `{"error":{"code":"ERROR_CODE","message":"Human-readable message","retryable":false,"details":{}}}`. Examples: INVALID_SESSION_INPUT (422), SESSION_NOT_FOUND (404), AI_SERVICE_UNAVAILABLE/STT_UNAVAILABLE (503). DEMO_AUDIO_DATA and sample outcome/documents/example.gov.in URL are placeholders, not playable audio or evidence.

## 9. Folders, owners and handshakes
Contract layout: frontend/ (Aditya); backend/ (Ankush: routes, schemas, graph, services, retrieval, eligibility, database); data/ (Anamika: documents, extracted text, scheme metadata/rules, evaluation); shared/ (Ankush + Aditya); docs/ (Ankush); root .env.example, .gitignore, README. Backend split: Ankush routes/orchestration/contracts and eligibility logic; Anamika scheme data, rule verification, STT evaluation. Four handshake interfaces are not named in available material: OPEN.

## 10. Environment and mock/real switches
Backend names: APP_ENV, APP_PORT, CORS_ORIGINS, GEMINI_API_KEY, GEMINI_MODEL_HIGH, GEMINI_MODEL_MID, GEMINI_MODEL_LITE, STT_PROVIDER, STT_API_KEY, STT_MODEL, TTS_PROVIDER, TTS_API_KEY, TTS_MODEL, SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, DATABASE_URL, MOCK_MODE, LOG_LEVEL. Frontend: VITE_API_BASE_URL, VITE_MOCK_MODE. Keep secrets off frontend.
Mock/real schemas must match; label sample data, never fabricate sources, don’t mix mock assessments into real evaluation; mock mode must not replace rule evaluation during scoring. Provider choices remain open.

## 11. Tests, metrics and scorecard
PMUY T01–T12 definitions: **OPEN / unavailable**. Canvas categories for ~30 cases, at least five each: typical, edge, ambiguous, out-of-scope, failure. Metrics: correct response with correct source, correct refusal, card completeness, speech transcription accuracy, time to card. Compare five situations against Bharat-VISTAAR, Kisan e-Mitra, myScheme eligibility and general AI; also time the team on official portals. Target set after first full run; no result supplied.

## 12. Reset schedule, checkpoints, freeze, sleep
Roadmap schedule: 9 PM mock thin slice; midnight first real end-to-end; 3 AM all P0 basic; 6 AM core complete/freeze; 9 AM tested/deployed/rehearsal; submission by 1 PM, 31 Oct. Freeze at 6 AM; then bug fixes only. Gate checks: 9 PM, midnight, 3/6/9/11 AM. Reset procedure itself unavailable.
Suggested rota: 12–2 AM Aditya sleeps; 2–4 AM Ankush; 4–6 AM Anamika; two awake. Five-minute check-in every two hours; 30 minutes stuck → ask for help; 60 minutes → change approach/cut. Timings are plan, not proof completion.

## 13. Risks and fallbacks
Speech/noise/accent/STT failure: repeat/rephrase, typed fallback; prerecorded Hindi question may exercise real pipeline. Quota: check limits; mock for UI/rehearsal; provider fallback OPEN. Cold start/network: wake service before demo, measure, retry or text/demo path. Privacy: collect minimum; no private-record lookup; consent, raw audio, retention/logging OPEN. Source freshness: official documents/date/source visible; refresh process OPEN. Outcomes indicative; unsupported topics refused; offline only P2.

## 14. Glossary
| Term | Meaning |
|---|---|
| Session / turn | Conversation id / one exchange; session_id / turn_id |
| Assessment | Deterministic outcome, reasons, missing information |
| Result | likely_eligible / likely_not_eligible / cannot_determine |
| Evidence | Official source document/chunk |
| Take-away card | Scheme, documents, destination, source, caveat |
| Mock mode | Predictable schema-compatible sample path |
| P0/P1/P2 | Must / should / nice-to-have |
| PMUY | Pradhan Mantri Ujjwala Yojana; rule source unavailable |

## OPEN
1. Missing named attachments: separate solution canvas, Phase 3.2 stack record, PMUY knowledge base/research analysis, Read First reset/scope/backend split, PMUY T01–T12. Available: local canvas/roadmap/UX and Phase 3.3 excerpt in referenced chat.
2. Scope conflict: PMUY-only fully built request vs 5–8 loaded schemes and 2–3 interviews. Documents: Phase 4.1 Master Brief request; TRIVON Solution Canvas (sources/DECISIONS.md). PMUY authority file absent.
3. PM-KISAN/PM-JAY 70+ status not specified: Phase 4.1 request vs TRIVON Solution Canvas / UI, UX and User Flow.
4. Seven node definitions/model tiers, four handshake interfaces, exact retrieval tables/source metadata, rules R01–R06/D01–D13, question order, other two dimensions and T01–T12 are undefined in available sources.
5. Reset procedure; actual provider/model IDs, quotas/fallbacks/audio transport, consent/retention and visual design details remain unspecified.
