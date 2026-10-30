# Antigravity Prompt Sequence — Aditya

**Purpose:** Copy these prompts into one Antigravity conversation in order to build Aditya’s Phase 5 frontend from repository inspection through real API integration and handoff.

**Role guide:** `docs/ANTIGRAVITY_ADITYA_BUILD_GUIDE.md`  
**Ownership:** Aditya owns `frontend/`; shared fixtures are coordinated with Ankush. The client never calls H2–H4 or a database directly. `sources/` is read-only.

## How to use this sequence

1. Paste Prompt A for a read-only repository and UX audit.
2. Confirm Prompt B’s plan and fixture/API agreement with Ankush.
3. Implement with Prompts C–F one stage at a time, reviewing before continuing.
4. Keep live API, microphone, and optional features behind the verified contract and actual acceptance needs.
5. Use Prompt G for final checks, evidence and handoff.

---

## Prompt A — Frontend preflight (read-only)

```text
You are Aditya, responsible for the Yojana Mitra Phase 5 frontend and user experience. Follow docs/ANTIGRAVITY_ADITYA_BUILD_GUIDE.md and root AGENTS.md. This stage is READ ONLY: do not edit/create/delete files, install dependencies, or call live services.

Identify the active repository root. Inspect the current frontend framework, package scripts, source tree, environment examples, UX flow, design assets, frozen H1 API contract, canonical shared fixtures, feature board and acceptance matrix. Treat sources/ as read-only. Confirm that the checkout you inspect is the same repository the backend teammate is using.

Return a map of existing frontend files and working behavior; the exact API/fixture sources found; missing fields/decisions; tasks and Feature Board IDs in your scope; files owned versus shared; and safe work that can start immediately. Explicitly confirm that frontend code will not calculate eligibility, fabricate sources, call internal H2–H4 services, or access Supabase. No edits in this stage.
```

## Prompt B — Frontend plan and shared contract agreement (no code)

```text
Prepare a step-by-step frontend plan from the repository audit. PLAN ONLY; do not edit files.

Sequence the work as: (1) preserve/complete the existing app shell; (2) exact TypeScript H1 models and mock client; (3) language/start/mode flow and scripted offline demo; (4) conversation/session state and text input; (5) voice controls plus typed fallback; (6) result/source/take-away card; (7) real API switch and recoverable errors; (8) responsive/mobile acceptance and handoff.

For each step list exact paths, dependencies, acceptance IDs and what can be checked. Confirm the exact shared fixture names, H1 response/error schema, API base URL/mock switch, local CORS origin, session reload behavior, and audio response content type with Ankush. Do not edit shared contract or fixture files. Verify card copy against Anamika’s authoritative source handoff; do not assume documents or application venues. Mark unresolved details OPEN. End with a short agreement checklist. No code.
```

## Prompt C — App shell, API types and mock client

```text
Implement only the app shell and mock client/types approved in the plan. Inspect existing files first and reuse the current project setup. Do not replace the framework, package manager, or design system without a concrete repo-based reason.

Build the TypeScript models directly from the frozen H1 contract and the mock client from the canonical shared fixtures. Keep fixtures unchanged. Use the existing environment names and approved API/mock configuration. Separate mock mode from real mode in code and visible development behavior; sample assessments and sources must never appear to be live evidence.

Do not guess missing response fields or error variants. If the contract/fixture set does not cover a state, report it OPEN and use a safe UI placeholder that does not invent policy. Do not implement eligibility calculations. Do not edit backend, data, sources or shared contract files.

Run the available frontend checks that are relevant to this slice, if dependencies are already present. Report exact files, commands, outcomes, and which UI paths are still mocked. Wait before building the full journey.
```

## Prompt D — User flow and scripted practice demo

```text
Implement the core navigation and onboarding flow using ui_userflow.md and the approved design assets. Follow the manual Hindi/English selection, welcome/start, mode choice and scripted practice/demo flow present in the project specification.

The scripted demo must use local pre-scripted content and make zero live AI/API calls. Label sample/demo behavior honestly. Do not put policy rules or eligibility calculations in the client. PMUY is the only full eligibility flow; other schemes must be marked “coming soon” or information-only only when approved source content exists.

Preserve existing state and styling conventions. Add empty, loading and recoverable navigation states only where specified. Do not invent content, sources, eligibility results or card details. Report completed screens, supporting checks and remaining dependencies before continuing.
```

## Prompt E — Conversation, session and voice/text experience

```text
Implement the approved conversation experience against the exact H1 contract. Confirm endpoints, payloads, voice transport and session semantics with Ankush before making API calls. The frontend uses only public H1 endpoints; it must not call internal graph, eligibility, retrieval, speech-provider or database services.

Build text sending, message rendering, session continuity, loading/error/retry behavior and voice controls from the approved contract. Keep user input when a recoverable request fails. If microphone permission or STT fails, make typed input available. If TTS/audio playback fails or the fixture audio is a placeholder, keep the written answer visible and show a usable non-audio state. Never persist audio to browser storage or log private transcripts.

Preserve `speech.audio_base64`; do not ask for or implement an external audio URL contract. Use content type only if the frozen response provides it; otherwise confirm with Ankush. Do not alter API schemas. Verify success and error fixtures locally, report exact results, and wait before final card integration.
```

## Prompt F — Results, sources, disclaimer and take-away card

```text
Implement the result and take-away card by rendering fields from the approved API response and verified content handoff. Do not derive eligibility or “fix” assessment results in the frontend.

Clearly render the frozen outcomes: likely eligible, likely not eligible, and cannot determine, using approved Hindi/English text. Display reasons, missing information, official source information and the indicative-not-official disclaimer as supplied by verified contract/content. Keep eligibility separate from document readiness or official verification. Never invent source links, source dates, documents required or application destinations. If a required field is absent, show an honest unavailable state and report the producer/contract mismatch.

Check readable layout, mobile behavior, keyboard interaction and visible error/empty states without claiming formal accessibility compliance unless a defined check was run. Report actual checks, screenshots/evidence path if permitted, and remaining contract issues.
```

## Prompt G — Real API integration and client acceptance

```text
Connect the frontend to Ankush’s backend using the frozen H1 contract and approved local configuration. First verify the server URL, CORS origin, mock switch and the backend’s actual status. Do not disable validation or silently change request/response fields to make a mismatch disappear.

Exercise the acceptance matrix items relevant to the frontend: Hindi and English clean starts, mock-vs-real labeling, result/card/source/disclaimer, voice-to-text continuity where supported, STT/TTS fallback, errors/retry, mobile layout and clean reset. Separate checks that use mock fixtures from real API runs. Use only test data approved for the demo.

Record actual outcomes in docs/BUILD_EVIDENCE_LOG.md with environment, browser/device, revision, steps, expected/observed result and evidence. Do not claim all acceptance is passed from a mock run. Report every API mismatch to Ankush with the observed request/response and expected frozen schema; do not modify shared contract yourself.
```

## Prompt H — Frontend final review and handoff

```text
Review the frontend changes and prepare Aditya’s handoff. Do not add optional features during this pass.

Check that only owned paths changed; server secrets are absent; mock fixtures are unchanged; no client-side eligibility logic or fabricated citation exists; scripted demo makes no live requests; audio is not persisted; Hindi/English and disclaimer behavior match the frozen spec; typed/written fallback works; and all API requests match H1.

Run available relevant checks and report exact commands and observed outcomes. Update BUILD_EVIDENCE_LOG.md only with evidence actually captured; label each path MOCKED, REAL, PARTIAL or NOT RUN. Return changed files, run steps, environment setup, supported browsers/devices actually checked, known limitations, OPEN fields, and backend handoff needs. Do not commit or push unless separately authorized.
```

## Aditya team gates

- **Before C:** canonical repository, H1 contract and fixtures verified.
- **Before D:** existing UX flow and scripted demo behavior confirmed.
- **Before E:** endpoint, session and audio semantics agreed with Ankush.
- **Before F:** response fields and card copy verified against contract and Anamika’s evidence.
- **Before G:** Ankush’s backend status and local CORS origin confirmed.
- **Before completion:** mock and real runs clearly separated and evidence recorded.
