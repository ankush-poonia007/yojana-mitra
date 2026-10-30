# TRIVON Solution Canvas

## At a glance

**Working name:** Yojana Mitra

**Status:** Problem statement 2.1 chosen and the voice agent approved for building on 30 Oct. The solution below is the agreed starting point; design details are still open (see the last section).

**One-line pitch:** A voice assistant that talks with rural families in their own language, asks the few questions an official scheme needs, and hands over a card with what to carry and where to go, with every answer tied to an official document and a published accuracy score.

**In plain words:** A person speaks a question in Hindi, or types it. The assistant works out which scheme they mean and asks the few questions the official rules need. It replies out loud and on screen with "likely eligible", "likely not eligible" or "cannot tell yet", names what is missing, and gives a card of documents to carry and where to apply. Every answer comes only from the official documents we load, with the source shown; otherwise it says it does not know.

**How it works (proposed; the design phase confirms it)**

&#91;embedded content: voice agent pipeline · 8 steps and a scorecard\]

The speech, retrieval and model providers are still open decisions; the steps stay the same whichever you choose.

## Canvas: Problem

- **Target user:** A farm household member who prefers speaking to reading. Secondary user: an ASHA worker or panchayat helper asking on someone's behalf. (Unvalidated; confirm in the venue conversations.)
- **Task the user is trying to complete:** Find out whether they qualify for a government scheme and what documents and steps they need.
- **Current workflow:** Ask a neighbour, middleman or panchayat staff; visit a Common Service Centre or office; wait; get partial information; return with documents; or phone a helpline within its hours; or try text portals in English or formal Hindi.
- **Main friction:** The information is written, scattered and not personalized. No tool we found combines a spoken, step-by-step eligibility conversation with a list of what to carry.
- **Consequence of the problem:** Trips, waiting, small service fees (Common Service Centre fees are reported at about Rs 10-100; weak sources), mistakes with documents, and possibly missed or delayed benefits (an assumption).
- **Evidence gathered:**
  - 488 million of India's 886 million internet users are rural (IAMAI-Kantar, 2024).
  - Kisan Call Centres registered 17,467,074 calls over about three years to mid-2021 (government statement, 2021): strong demand for spoken help.
  - PM-KISAN's AI chatbot reports very large query volumes (news and developer reports; figures differ).
  - Bharat-VISTAAR (a government voice AI) launched on 17 Feb 2026 with ten central schemes; whether it has expanded is unverified.
  - Awareness-gap surveys exist but are dated (2003 and 2009).
  - Still to collect: competitor test results and two or three venue conversations.
- **Unvalidated assumptions:**
  - Users will speak to a phone or a helper's phone.
  - Speech recognition is accurate enough in Hindi and one more language, in a noisy room.
  - We can get current official documents for the chosen schemes.
  - The tool really saves time compared with the current route.
  - A gap remains after existing government tools (to be tested).

## Canvas: Product

- **Core solution in one sentence:** A voice-first assistant that asks the few questions an official scheme needs, tells the user whether they are likely eligible and what is missing, and hands over a take-away card, with every answer tied to an official document.
- **Main user benefit:** Know in minutes, in their own language, whether to apply and what to carry, so there are fewer trips and fewer mistakes.
- **USP / difference from alternatives:**
  1. *It interviews instead of lecturing.* Chatbots answer a general question and portals use a text form; this asks the few spoken questions the rules need and says what is missing.
  2. *It ends with a take-away card.* The user leaves with the scheme, the documents to carry, where to apply and the source.
  3. *It publishes its own trust scorecard.* About 30 test questions give measured numbers for correct answers, correct sources and correct refusals.
  - Not unique, so do not pitch them as the difference: voice, several languages, and answers with sources. Other tools offer these.
- **Core user journey (3-6 steps):**
  1. The user speaks (or types) a question in Hindi, for example whether they qualify for a scheme.
  2. The assistant finds the scheme and asks 3-5 short questions the official rules need.
  3. It answers "likely eligible", "likely not eligible" or "cannot tell yet", with the reasons and what is missing.
  4. It shows and reads out a card: documents to carry, where to apply, and the source document.
  5. For anything outside the loaded documents it says "I don't know; ask your panchayat".
- **What we will not build:**
  - Lookups of private records (Aadhaar or payment status)
  - Submitting applications for the user
  - Medical or legal advice, or crop advice
  - 22 languages, SMS or WhatsApp (before P2)
  - An offline mode (before P2)
  - Any claim that results are official decisions; every result is labeled "indicative; confirm at the office or portal"

## Canvas: Evaluation

- **Primary metric:** The share of about 30 test questions answered correctly with the correct official source shown.
- **Secondary metrics:**
  - Correct refusals: the share of questions outside the loaded documents where it says "I don't know"
  - Card completeness: the share of required documents the card lists, against the official document list
  - Speech accuracy: how many of our own recorded test sentences are transcribed correctly
  - Time from question to card
- **Baseline and how it will be measured:** Run the same 5 realistic situations through the existing tools (Bharat-VISTAAR, Kisan e-Mitra, myScheme's eligibility check and a general AI assistant). For each, record whether it understood the Hindi, asked a follow-up, named a source, listed documents, admitted when it did not know, and how long it took. Also time your own team finding the same answers on official portals.
- **Target (not yet a result):** Set after the first full run; do not put a number on a slide in advance. Write it here once chosen: \_\_\_\_\_\_
- **Test cases (five types, at least 5 of each in the 30):**
  - Typical: a clearly eligible or clearly ineligible person
  - Edge: a borderline case at a rule's limit
  - Ambiguous: key information missing, so the correct answer is "cannot tell yet"
  - Out of scope: a scheme or topic that is not loaded, so the correct answer is a refusal
  - Failure: speech recognition fails or a service is down, so the typed fallback works
- **Known limitations:**
  - Results are indicative, not official decisions
  - Only 5-8 schemes and two languages are covered
  - Speech accuracy drops in noise and with accents
  - The documents may become outdated; record each document's date
  - The test set is built by our team, not by independent experts

## Canvas: Delivery

**Priorities and owners**

| Priority | Task | Owner | How we know it works |
| --- | --- | --- | --- |
| P0 | Spoken or typed input with speech to text in Hindi | Anamika (speech), Aditya (microphone and typed interface) | 5 recorded Hindi sentences come back correct, and typed input works when speech fails |
| P0 | Collect and clean official documents for 5-8 schemes, with each document's date | Anamika | A list of documents with source links and dates |
| P0 | Retrieval and grounded answers with the source shown, and refusal outside the documents | Ankush | Test questions return the right source; out-of-scope questions are refused |
| P0 | Ask-back eligibility flow for 2-3 schemes | Ankush (logic), Anamika (checks the rules against the official text) | The flow reaches the right result on the typical, edge and ambiguous test cases |
| P0 | Spoken reply and on-screen answer | Aditya (interface), Ankush (service) | The answer is audible and readable with its source |
| P0 | Take-away card | Aditya (design), Ankush (content) | The card lists every required document for each demo scheme |
| P0 | Test set of about 30 questions and the scorecard script | Anamika | One command prints the scorecard |
| P1 | A second language | Anamika, Aditya | A person who speaks it checks 10 answers |
| P1 | Card saved as an image or PDF | Aditya | The file opens on a phone |
| P1 | Helper mode (asking on someone's behalf) | Ankush, Aditya | The demo works for "my neighbour" questions |
| P1 | Scorecard page inside the app | Aditya, Anamika | Numbers shown match the script |
| P2 | Cached offline answers; WhatsApp or SMS; more schemes | Whoever has time | Only after P0 and P1 are tested |

**Integration checkpoints** (move them later only if the build start slips; never move the freeze)

- [ ] 9:00 PM: a thin slice runs end to end, with mock data where needed
- [ ] Midnight: the first real end-to-end run with real speech, documents and model
- [ ] 3:00 AM: every P0 works in at least a basic form
- [ ] 6:00 AM: core complete; feature freeze
- [ ] 9:00 AM: tested and deployed; the demo is rehearsed after this
- [ ] 1:00 PM at the latest: submitted

**Feature freeze:** 6:00 AM on 31 Oct. After that, only bug fixes.

**Demo fallback:**

- Typed input instead of speech
- A pre-recorded Hindi question played into the microphone, which still runs the real pipeline
- A screen recording only if the event rules allow it, and only if you say it is a recording

## Canvas: Pitch

This is the draft story; replace each blank with a measured result or a real story before presenting.

- **Opening problem statement:** A farmer wants to know one thing: do I qualify, and what do I carry? Today the answer is written in English or formal Hindi, spread across portals, and finding it means trips, waiting and a fee. (Swap in a real story from a venue conversation.)
- **Best evidence:** 488 million of India's internet users are rural; Kisan Call Centres registered 17.5 million calls in about three years; in our competitor test, \_\_\_ of 5 situations got a follow-up question from the existing tools.
- **Cost or consequence:** Use the measured time and visits from your venue conversations or your own timing: \_\_\_ hours and \_\_\_ visits. (Until measured, label the illustrative calculation as an illustration.)
- **Solution and differentiator:** Awaaz Saathi (rename) interviews the user in their own language, hands over a card of what to carry and where to go, and publishes its own accuracy scorecard. Voice and sources are table stakes; the interview, the card and the scorecard are the difference.
- **Demo scenario (under 3 minutes):**
  1. A family member asks in Hindi whether they qualify for a scheme.
  2. The assistant asks three questions, and a judge answers them.
  3. It gives the result and reasons, names what is missing, and shows and reads out the card.
  4. A question outside the loaded documents gets "I don't know; ask your panchayat".
  5. A slide shows the scorecard and the competitor test.
- **Measured impact (if available):** Scorecard \_\_\_ of 30 correct with the right source; \_\_\_ of \_\_\_ out-of-scope questions refused correctly; the card lists \_\_\_% of the required documents; time to answer \_\_\_ compared with \_\_\_ for the current route.
- **Known limitation:** Results are indicative, not official; only 5-8 schemes and two languages; speech accuracy depends on noise and accent; the test set was built by our team.
- **Next step:** Ask a panchayat office or a Common Service Centre to try it with real users, add schemes and languages, and keep the documents current with an update date on every source.

## The process from now

Use this doc as the one place that holds the solution: after every decision, update the canvas above and add a line to the decision log below. These steps follow your TRIVON Roadmap and Prompt Pack.

- [ ] **Now to 4:45 PM, freeze the open decisions** in the last section: the new name, the 5-8 schemes, the second language and the speech provider
- [ ] **At the same time, run the two tests:** the 30-minute speech smoke test and the 15-minute competitor test (record results in the table below); if either fails, switch to the support triage agent
- [ ] **4:45 PM, challenge it:** paste this canvas into the other AI with the Challenge Prompt (Prompt Pack 2.3) and bring back what you accept or reject
- [ ] **4:45 to 5:30 PM, Phase 3:** run Prompt Pack 3.1 (flow and logic), 3.2 (stack and architecture) and 3.3 (API contract and folders); save each Decision Record to decisions.md
- [ ] **5:30 to 6:15 PM, Phase 4:** run 4.1 (master brief), 4.2 (personal briefs), then set up Antigravity with 4.3, 4.4 and 4.5
- [ ] **From 6:15 PM, build:** work to the checkpoints in the Delivery section, with a five-minute check-in every two hours and the sleep rota from midnight
- [ ] **6:00 AM, freeze;** then testing, deployment and the scorecard run
- [ ] **9:00 AM onward:** fill the results table below, replace the blanks in the Pitch section, then run the Chat 4 prompts (evidence, deck, demo script, judge questions, submission check)

## Open decisions, decision log and results

**Open decisions**

| Decision | What to settle | Owner | By |
| --- | --- | --- | --- |
| Event rules | Are outside APIs, AI coding tools and starter code allowed? | Ankush | Now |
| New name | The final product name; replace the working name everywhere | Ankush | 4:45 PM |
| Schemes | Which 5-8 schemes to load and which 2-3 get the ask-back interview; each needs a current official document you can get today | Ankush, Anamika | 4:45 PM |
| Second language | Hindi plus one that someone on the team can check | Team | 4:45 PM |
| Primary user | Farm household member or a helper, after the venue conversations | Team | 5:00 PM |
| Speech provider | Bhashini or Sarvam, with a local model as backup; confirm free credits and prices at signup because sources conflict | Anamika | 5:00 PM |
| Language model | Which model, its quota and a fallback | Ankush | 5:15 PM |
| Hosting and demo setup | Local or deployed; test from another device and network | Ankush, Aditya | 5:30 PM |

**Decision log** (add a line after every decision)

| Time | Decision | Decided by | Notes |
| --- | --- | --- | --- |
| 30 Oct, afternoon | Problem statement 2.1 chosen; voice agent approved for building | Team | Support triage agent is the fallback |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

**Results to fill at the end** (copy these into the Pitch section and the deck)

| Measure | Baseline | Our result | Label |
| --- | --- | --- | --- |
| Test answers correct with the right source (of about 30) |  |  | Measured |
| Out-of-scope questions refused correctly |  |  | Measured |
| Card lists the required documents (%) |  |  | Measured |
| Speech transcribed correctly on our recorded sentences |  |  | Measured |
| Time from question to card |  |  | Measured |
| Existing tools that asked a follow-up question (of 5 situations) |  |  | Measured |

## Phase 3.2 — Stack and architecture decisions (30 Oct 2026)

**Status: IN PROGRESS — NOT FROZEN.** These decisions were explicitly confirmed by Ankush. They supersede earlier proposals where they conflict. Do not begin Phase 3.3 until Ankush explicitly says **"frozen"**.

### Confirmed decisions

1. **Orchestration:** LangGraph.
2. **LLM strategy:** Gemini as the selected model-provider strategy. Exact model IDs, task-to-model assignments and fallback behavior remain open.
3. **Speech-to-text (STT):** Benchmark candidate providers/models before selecting the production choice.
4. **Text-to-speech (TTS):** Use a Lite-tier model as the primary direction. Exact provider/model and fallback remain open.
5. **Database:** Supabase PostgreSQL.

### Remaining unresolved items

| Area | Open item | Suggested owner |
| --- | --- | --- |
| LLM model selection | Confirm exact Gemini model IDs for high-, mid- and lite-complexity tasks; verify current API availability and free-tier quotas in the team's accounts. | Ankush |
| LLM routing | Map each LangGraph node/agent to a model and define when a task is escalated to a stronger model. | Ankush |
| LLM resilience | Decide whether to configure a secondary provider, and define retry, quota-exhaustion and provider-outage behavior. | Ankush |
| Agent design | Confirm the final agent/node responsibilities, conditional routes and which steps must use deterministic code rather than an LLM. | Ankush |
| STT benchmark | Select the candidate models/providers, prepare a representative Hindi audio test set, define evaluation measures (transcription correctness, critical-field accuracy, latency and failure rate), run the benchmark and choose the winner. | Anamika (test set and evaluation), Ankush (integration) |
| TTS implementation | Select the exact Lite-tier model/provider; verify Hindi voice quality, latency, quota and browser/device compatibility. Decide the fallback if synthesis fails. | Ankush (provider), Aditya (UX playback validation) |
| Supabase design | Finalize tables, relationships, migrations, session/message persistence and which assessment data is retained. | Ankush |
| Supabase security | Define RLS policies, backend-only service-role access, secrets handling, data minimization and retention/deletion behavior. Avoid storing raw audio or sensitive identity/bank details by default. | Ankush |
| API and deployment details | Confirm frontend/backend hosting, environment configuration, CORS, health checks and deployment fallback. | Ankush (backend/deployment), Aditya (frontend) |
| Free-tier validation | Check actual project/account quotas, rate limits, billing requirements and inactivity/sleep behavior for selected services; treat free availability as subject to change. | Ankush, with each integration owner |

### Phase gate

- [ ] Exact Gemini model IDs and task routing agreed.
- [ ] LangGraph nodes/agents and deterministic boundaries agreed.
- [ ] STT benchmark candidates, test set and selection criteria agreed; benchmark result recorded (or an explicit event-time decision to defer is documented).
- [ ] Lite-tier TTS model and fallback agreed and Hindi playback tested.
- [ ] Supabase schema, access controls and data-retention approach agreed.
- [ ] Hosting, quotas, secrets and failure fallbacks checked.
- [ ] Ankush explicitly says **"frozen"**.

**Next:** Continue resolving Phase 3.2 only. Phase 3.3 (API contract and folder structure) is blocked until explicit freeze approval.
## Status reconciliation

The Phase 3.2 section earlier in this file is a historical snapshot and says “IN PROGRESS — NOT FROZEN.” The later reviewed decision context confirms Phase 3.2 was frozen and Phase 3.3 was also the frozen API contract authority before Phase 4.1 approval. Preserve the Phase 3.2 decisions themselves; use the confirmed frozen status and authority hierarchy in the Phase 4.1 record below. This note corrects status interpretation without rewriting the prior decision content.
## Record status

| Field | Value |
| --- | --- |
| Record | Phase 4.1 — Scheme Knowledge, Eligibility Rules & Integration Contracts |
| Decision date | 30 October 2026 (Asia/Kolkata), based on the referenced conversation |
| Status | **FROZEN — explicitly approved by the user** |
| Product | Yojana Mitra |
| Decision authority | User's submitted D1–D14 decisions and explicit final approval |

> **Freeze authorization.** The user explicitly confirmed: “All four detailed contracts and examples are documented and reviewed. I explicitly approve freezing Phase 4.1.” The phase is frozen on that authorization. The user also confirmed the H1–H4 contracts and success/failure examples were documented and reviewed. This record did not independently inspect those detailed artifacts, and therefore does not reproduce or certify their schemas or examples.

## 1. Decision scope and hierarchy

Phase 4.1 freezes the scheme scope, PMUY eligibility and interview policy, evaluation baseline, integration boundaries, audio/STT/privacy/retrieval policy, source caveat, and v1 language behavior recorded below.

Authority order for implementation:

1. This record contains the user's frozen Phase 4.1 choices D1–D14.
2. The PMUY Knowledge Base is the intended authority for PMUY rules and test content. Its full text was not available among the editable project files inspected for this record; consult the designated source artifact before implementing rule-level details.
3. Frozen Phase 3.2 remains authoritative for architecture and technology choices.
4. Frozen Phase 3.3 remains authoritative for endpoint and response contracts, including the preserved `speech.audio_base64` response field.
5. Phase 4.1 does not silently amend Phase 3.2 or 3.3. Resolve any implementation conflict through a separately recorded change.

Earlier frozen phases remain intact. Older multi-scheme proposals are superseded where they conflict with D1.

## 2. PMUY scope reset

- **PMUY:** the only scheme with full eligibility assessment in this scope.
- **PM-KISAN and PM-JAY 70+:** information-only, and only after their source material is validated. No eligibility engine for either is authorized by this decision.
- This resets the older roadmap/canvas proposal for 5–8 schemes and eligibility interviews for 2–3 schemes. Those broader targets are not Phase 4.1 implementation scope.
- Eligibility outputs are indicative, not official determinations. Unsupported claims must be refused or returned as unknown.

## 3. Frozen decisions D1–D14

### D1 — Scheme scope

**Decision:** Implement full eligibility for PMUY. PM-KISAN and PM-JAY 70+ may be information-only after source validation.

**Rationale / effect:** Focuses the eligibility engine on one reviewed scheme. It supersedes earlier multi-scheme eligibility targets.

### D2 — PMUY rules and declarations

**Decision:** Adopt rules R01–R06 and declarations D01–D12. Evaluate D13 only once through R03. Keep R07 in application readiness/verification, outside the eligibility determination.

**Rationale / effect:** Keeps application verification separate from eligibility and avoids double-counting D13. Use the PMUY Knowledge Base for the definitions and values; do not recreate absent rule text from this summary.

### D3 — R05 outcomes

**Decision:** A clear R05 failure maps to “likely not eligible”; an unclear or uncertain answer maps to “cannot determine.”

**Effect:** Missing or ambiguous input must not be silently treated as a negative answer.

### D4 — R06 and domestic PNG

**Decision:** Keep R06 separate. Domestic PNG means likely not eligible for subsidised LPG under the reviewed KYC interpretation, subject to distributor confirmation.

**Caveat:** This operational interpretation remains subject to the open confirmation listed below.

### D5 — Assessment dimensions

**Decision:** Adopt all three sets of assessment values exactly as documented in the PMUY Knowledge Base.

**Boundary:** The value sets are not reproduced here because the referenced Knowledge Base was not independently available for inspection in this documentation pass. Implementers must use that source verbatim and keep the dimensions distinct.

### D6 — Interview

**Decision:** Adopt the four-stage interview. Ask D01–D12 one at a time. Keep readiness questions separate from eligibility questions.

**Boundary:** The detailed stage definitions and question wording remain in the reviewed source artifacts; they are not reconstructed here.

### D7 — Tests

**Decision:** Adopt existing PMUY-T01 through PMUY-T12 as the baseline test suite.

**Boundary:** Preserve the existing test cases; do not invent replacements or claim this record contains their case data.

### D8 — Integration handshakes

**Decision:** Approve the H1–H4 boundaries and the detailed contracts as user-confirmed documented and reviewed.

| Handshake | Boundary | Status |
| --- | --- | --- |
| H1 | Frontend ↔ API | User confirmed detailed contract and success/failure examples documented and reviewed; not independently inspected here |
| H2 | API ↔ LangGraph | User confirmed detailed contract and success/failure examples documented and reviewed; not independently inspected here |
| H3 | LangGraph ↔ Eligibility Engine | User confirmed detailed contract and success/failure examples documented and reviewed; not independently inspected here |
| H4 | LangGraph ↔ Retrieval | User confirmed detailed contract and success/failure examples documented and reviewed; not independently inspected here |

The user's review checklist also confirmed endpoint requests/responses/errors (H1), graph input/shared state/output (H2), answer representation/engine output (H3), retrieval requests/evidence metadata (H4), one success and failure example per handshake, and validation against PMUY-T01–T12 and Phase 3.3 examples. **No payload schemas, field lists, or examples are asserted in this record.** Use the reviewed contract artifacts as the implementation source of truth.

### D9 — Audio response contract

**Decision:** Preserve the Phase 3.3 `speech.audio_base64` response contract. Benchmark payload size and latency before considering any amendment.

**Effect:** Do not change the frozen response shape as part of routine Phase 4.1 implementation.

### D10 — Speech-to-text benchmark

**Decision:** Benchmark Gemini transcription, Whisper Large V3, and Whisper Large V3 Turbo. Select based on measured results.

**Effect:** No provider is selected by this decision; record the benchmark results and selection separately.

### D11 — Privacy

**Decision:** Do not persist raw audio by default. Minimize session data and define retention and deletion before deployment.

**Effect:** A concrete retention/deletion policy and its implementation remain open work, not assumed complete.

### D12 — Retrieval

**Decision:** Use official-source-only retrieval. Preserve source IDs, page/section, version, and retrieval date. Refuse unsupported claims.

**Effect:** Source provenance and refusal behavior are requirements. Exact storage schema and retrieval DDL are implementation work.

### D13 — Declaration revision currency

**Decision:** Use the captured declaration as a design baseline, but leave its revision currency open until confirmed with a distributor/OMC.

**Caveat:** Do not describe the captured declaration as independently verified current policy.

### D14 — Languages

**Decision:** Hindi and English in v1. The user manually selects the response language. Voice and text use shared logic.

**Effect:** Do not infer automatic language switching as a frozen requirement.

## 4. H1–H4 freeze gate and evidence limits

The linked conversation records the user's completion of all six H1–H4 review checklist items and explicit confirmation that detailed contracts and examples exist and were reviewed. This is sufficient to record the user's approval and freeze authorization. The detailed contract artifacts were not independently inspected in this conversation, and the available local project files do not supply their schemas or examples. Accordingly:

- This record captures handshake names, boundaries, review status, and the user's confirmation only.
- It intentionally does not invent endpoint fields, state keys, engine result schemas, retrieval tables, or example payloads.
- Implementation should link or attach the reviewed H1–H4 contract artifacts to the project record when available, without reopening the approved decision unless a real contract conflict is found.

## 5. Source and research caveats

- The Deprivation Declaration PDF's revision/publication currency was not established in the reviewed material. D13 leaves confirmation open with a distributor/OMC.
- PMUY R06's domestic PNG interpretation requires distributor confirmation.
- The PMUY Knowledge Base, PMUY Research Analysis, Phase 3.2 record, Phase 3.3 full record, and PMUY-T01–T12 were referenced in the conversation, but were not present as inspectable local project files in this pass. The record reports the decisions supplied in the conversation and does not claim independent source verification.
- Any PM-KISAN or PM-JAY 70+ content must be checked against current official sources before being presented, even as information-only.
- The broader solution canvas labels user demand, venue interviews, competitor results, provider performance, and some impact claims as unvalidated or needing measurement. Do not present them as demonstrated results.
- All eligibility outputs remain indicative; only official authorities determine eligibility and application acceptance.

## 6. Open implementation and verification work

These items do not revoke the freeze. Owners below follow the project roadmap's role assignments; where an assignment is inferred for coordination, it is labeled **proposed** and is not a new frozen decision.

| Item | Owner | Status / completion evidence |
| --- | --- | --- |
| Confirm captured Deprivation Declaration revision/current acceptance with LPG distributor or OMC | Anamika (roadmap research/data owner) | Open; record confirming source and date |
| Benchmark Gemini transcription, Whisper Large V3, and Whisper Large V3 Turbo | Anamika | Open; compare measured transcription quality and latency and record selection |
| Measure audio payload size and end-to-end latency while preserving Phase 3.3 response contract | Ankush (proposed; integration owner) with Aditya for client behavior | Open; measurements and any contract-change proposal if needed |
| Define and implement session retention/deletion; verify raw audio is not persisted by default | Ankush (proposed; architecture/integration owner) | Open; documented policy and implementation evidence before deployment |
| Finalize retrieval database DDL and provenance fields | Ankush (proposed; integration owner) | Open; schema supports source ID, page/section, version, retrieval date |
| Validate PM-KISAN and PM-JAY 70+ official sources before any information-only content is enabled | Ankush and Anamika (proposed) | Open; dated official-source register and reviewed content |
| Carry out the frozen H1–H4 contracts in integration and link the reviewed artifacts in the project | Ankush (integration), Aditya (frontend/H1), Anamika (rule/source checks) | User reports contracts/examples reviewed; implementation and artifact linkage evidence not inspected here |

## 7. Assumptions and implementation guardrails

- R01–R06, D01–D12, assessment values, four interview stages, and PMUY-T01–T12 are defined by the referenced PMUY artifacts; fetch those artifacts before implementing exact rules or tests.
- Unknown, unclear, or missing answers must remain unknown; do not coerce them to “No.”
- The deterministic eligibility engine owns the eligibility result; generated language may explain but must not override that result.
- Keep eligibility, official verification, and application readiness distinct.
- Retrieval is constrained to validated official sources, with the provenance metadata in D12.
- Do not persist raw audio by default. Minimize collected session data and complete retention/deletion decisions before deployment.
- Existing Phase 3.2/3.3 decisions remain authoritative in their domains; a necessary amendment must be explicit and recorded.

## 8. Next phase

**Next: Phase 4.2 — personal briefs**, then the remaining Phase 4 setup and implementation handoff described in the roadmap. Phase 4.1 is complete and frozen. Phase 4.2 and later work must implement these decisions without expanding the approved scope by implication.

## 9. Change control

Treat D1–D14 as frozen. A correction to source facts, a contract conflict, or a required change to a prior frozen phase must be raised as a proposed amendment with its evidence, affected decision, owner, and implementation impact. Do not silently rewrite this record or the Phase 3.2/3.3 authority.



## Phase 4.2 — Personal Briefs (31 Oct 2026)

### Record status

| Field | Value |
| --- | --- |
| Record | Phase 4.2 — Personal Briefs |
| Decision date | 31 October 2026 (Asia/Kolkata) |
| Status | **DOCUMENTED — REVIEW PENDING; NOT FROZEN** |
| Product | Yojana Mitra |
| Authority | Existing frozen Phase 4.1 decisions, Master Brief, and the roadmap; this entry records documentation progress only |

### Decision

Prepare exactly three personal briefs for Ankush, Anamika, and Aditya, followed by a caller/callee matrix. Preserve the existing contents and prior decisions in this file. Phase 4.1 remains frozen as previously authorized. Phase 4.2 is not declared complete or frozen by this entry; a separate explicit approval is required to freeze it.

### Brief requirements and checkpoint gates

Each brief records its objective, inputs, yes/no deliverables at 2:30 AM (thin slice), 5:30 AM (first real end-to-end), 8:00 AM (P0 basic), and 9:00 AM (freeze gate), owned and forbidden files, interfaces provided/called, mock availability from 1:00 AM, acceptance criteria, solo test, out-of-scope work, and the 30-minute escalation rule.

The roadmap's original gates remain in force: 9:00 PM mock thin slice, midnight first real end-to-end, 3:00 AM P0 basic, 6:00 AM core feature freeze, 9:00 AM tested/deployed and rehearsal, and submission by 1:00 PM. The requested 2:30/5:30/8:00/9:00 AM gates are documented as additional team checkpoints and do not move the roadmap freeze.

### H1–H4 interface documentation boundary

The two backend briefs use matching H1–H4 boundary wording. The available project record names these boundaries as H1 Frontend ↔ API, H2 API ↔ LangGraph, H3 LangGraph ↔ Eligibility Engine, and H4 LangGraph ↔ Retrieval. The documented API paths are `POST /api/v1/sessions`, `GET /api/v1/sessions/{session_id}`, `POST /api/v1/turns`, and `POST /api/v1/voice/turns`.

Exact internal function names and detailed H2–H4 schemas are not present in the available Master Brief/decision record and are marked **OPEN** in the briefs. No names, payload fields, or mock file paths are inferred. The briefs note that the detailed H1–H4 artifacts were reported reviewed, but are not attached to the project copy inspected for this record.

### Deliverable and review status

The three briefs and caller/callee matrix are documented in `PHASE_4.2_PERSONAL_BRIEFS.md`. This is evidence that the documents were prepared; it is not evidence that implementation checkpoints have passed. The two backend H1–H4 blocks were checked for matching wording. Review of the briefs remains pending.

### OPEN items

- Review and accept the three briefs; obtain explicit approval before marking Phase 4.2 frozen.
- Link or attach detailed H1–H4 contract artifacts if exact schemas/function names are needed.
- Exact internal function names, detailed graph/engine/retrieval schemas, mock fixture path, deck path, and ownership for shared mock setup remain OPEN where not documented.
- PMUY knowledge/test materials, rule details, Supabase DDL, provider selection, retention policy, and reset procedure remain governed by the existing open-item records; this Phase 4.2 entry does not resolve them.
