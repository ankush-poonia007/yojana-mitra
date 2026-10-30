# Yojana Mitra — UI, UX and User Flow

**Document purpose:** implementation handoff for the frontend and user experience of the Yojana Mitra hackathon prototype.

**Status:** consolidated from the referenced “Trivon Mentor Setup” conversation and the read-only project references `sources/DECISIONS.md` and `sources/Yojana Mitra Hackathon Roadmap & Checklist.md`. The conversation describes the overall UI direction as finalized, but the available record does not contain final screen designs, component measurements, or a full decision history. This document preserves the decisions that are present and labels the rest as proposals or assumptions.

## 1. Decision status and source of truth

### Frozen direction present in the available record

- Product working name: **Yojana Mitra**. The project decision canvas calls this a working name; final naming is still listed as an open decision.
- The product is a **voice-first, text-supported conversational assistant** for helping people understand government schemes, check indicative eligibility, and learn what documents and steps may be needed.
- A user can speak or type. Assistant answers are available as on-screen text and spoken audio. A user can listen to a response and can move between interaction modes without losing the conversation or restarting an eligibility assessment.
- The experience should support a complete voice-only path for a person who cannot or does not want to read or write.
- An onboarding demo follows language selection. It is a guided, step-by-step interaction exercise, not just a static tutorial. It uses predefined prompts and outputs and **does not call the real AI**.
- After the demo, the user may repeat it, continue to another task, or skip the remaining tutorial; then choose voice or chat mode. The chosen mode is shown before starting the real assistant conversation.
- The assistant asks a small number of short questions (the project canvas suggests 3–5) needed by the selected scheme rules. It reports **likely eligible**, **likely not eligible**, or **cannot tell yet**, explains why or what is missing, and provides a take-away card with documents, where to apply, and the official source.
- Results are indicative, never an official decision. Answers should be grounded in loaded official documents, cite/show the source, and say when the answer is not known from those documents.
- Initial project scope in the decision canvas: 5–8 loaded schemes, 2 languages, and eligibility interviews for 2–3 schemes. These are project targets, not evidence that the implementation already supports them.
- Out-of-scope items before later phases: private-record lookups (including Aadhaar or payment status), application submission, medical/legal/crop advice, 22-language coverage, offline mode, SMS and WhatsApp.

### Open decisions explicitly listed by the project

- Final product name; selected schemes and interview schemes; second language; confirmed primary user; speech provider; language model and fallback; hosting/demo setup.
- Speech, retrieval and model providers are not settled by the reference materials. Do not infer an API, endpoint, payload, vendor, or frontend/backend stack from this document.
- The UI is described as finalized in the conversation request, but exact visual specifications are absent from the available conversation preview and source files. Treat component sizes, colors, typography, iconography, responsive breakpoints, and polished screen layouts as requiring the approved design artifact or team confirmation.

### Labels used below

- **Established:** directly present in the referenced conversation or project decision canvas.
- **Proposal:** a UX recommendation that makes the established flow implementable, but was not explicitly frozen.
- **Assumption:** a detail needed for planning that must be verified before it is treated as a product decision.

## 2. Product and users

### User need

The primary intended user is a farm household member who prefers speaking to reading. A secondary user may be an ASHA worker or panchayat helper asking on someone’s behalf. The project source labels these personas unvalidated; venue conversations are still needed.

The user is trying to learn whether a government scheme may apply to them, what information is missing, what documents to carry, and where/how to apply. The design addresses written, scattered, formal-language information and repeated trips or incomplete guidance.

### Product promise and trust boundary

Help a person understand a scheme in their language through a short spoken or typed conversation, then leave with a source-linked, practical next-step card. The service is an informational aid: it does not determine official eligibility, access personal government records, or file applications.

## 3. Interaction modes

The reference conversation establishes three supported interaction patterns for one assistant experience:

1. **Voice-first / voice-only:** the user speaks, receives a spoken answer, and can complete the flow without reading or typing. Text may still be available when useful, but no required action should depend on reading it.
2. **Chat / text:** the user types and reads responses. Assistant response playback may be available as an audio control.
3. **Combined text and voice:** the assistant response is displayed and can be played aloud; the user may speak or type. The conversation remains one continuous history.

**Established behavior:** changing modes must preserve conversation history and the eligibility assessment. The selected mode is clearly displayed when the real conversation begins.

**Proposal:** offer an always-visible, plainly named mode control, plus a microphone and a text-entry fallback where screen space permits. Do not hide the ability to switch behind a settings screen. Mode names, control placement, and whether combined mode is a separate named selection remain design details to confirm.

## 4. End-to-end user flows

### First-time user and guided demo

1. **Choose language.** User selects a supported language (Hindi and English are explicitly used in the conversation example; the project source says Hindi plus one additional language, not yet chosen). The selection applies to onboarding and subsequent assistant interaction.
2. **Welcome.** Assistant introduces the service and explains that the user can speak or type. The conversation recommends showing and speaking the welcome. Spoken welcome is an established recommendation, but whether it is mandatory is not recorded as a final decision.
3. **Explain the demo.** Make clear this is a practice experience and uses prepared answers rather than the live AI. This follows the user's explicit dummy-demo requirement; the exact disclosure wording is open.
4. **Guide navigation.** Highlight the next control and give one short instruction at a time, for example asking the user to tap the microphone.
5. **Prompt a practice utterance.** Display and, where available, read a sample phrase such as asking about Ujjwala Yojana. The example phrase is illustrative, not a selected live scheme.
6. **Simulate interaction.** User speaks (or follows the visible demo instruction); the experience maps the practice step to a predefined response. No real AI request is made during the demo. The demo may display a simulated transcript/response and play prepared audio if assets exist; exact implementation is open.
7. **Explore response controls.** Let the user practice hearing a response, replaying it, viewing its text, and answering a follow-up. These interactions are present in the referenced proposal; detailed steps and assets are not specified.
8. **Offer choice.** User can repeat the exercise, continue to another task, or skip remaining demo steps if comfortable.
9. **Choose mode.** User selects voice or chat; selected mode is shown.
10. **Enter live assistant.** Demo state ends and the real assistant begins. Keep the demo/live boundary clear.

**Demo states (proposal):** language selection → welcome → step instruction → awaiting practice → simulated response → response exploration/follow-up → demo completion → repeat/continue/skip decision → mode choice → live conversation. Each step needs a visible and/or spoken way to continue, go back where safe, or skip.

### Returning user

**Assumption:** returning users can bypass the guided demo and go directly to their last or default interaction mode. The available record does not specify persistence, user accounts, or how the system identifies a returning user. Do not require an account solely to implement this assumption.

### Live scheme conversation

1. User asks a question by voice or text, for example “Am I eligible for …?”
2. System identifies a supported scheme from loaded material, or asks a simple clarifying question if the scheme is unclear. Exact selection behavior is not specified.
3. Assistant asks the minimum relevant eligibility questions, one at a time, using short everyday language. The project canvas suggests 3–5 questions, with interview logic for 2–3 schemes in the initial build.
4. User can answer by speaking or typing, switch modes, replay or hear the question, and correct an answer. Confirm important answers before using them where misunderstanding could change the outcome.
5. Assistant summarizes relevant answers and reports likely eligible, likely not eligible, or cannot tell yet. It names the reason and missing information, and shows the official source.
6. Assistant shows and reads the take-away card: scheme, required documents, where to apply, source, and a clear indicative-status caveat.
7. User can ask a follow-up, hear the response, or start another scheme inquiry. The exact controls and whether a card can be saved are phase-dependent.

### Unclear, missing, or unsupported request

When a rule-critical answer is missing or unclear, ask one simple follow-up or report “cannot tell yet” and say what information is missing. For a scheme/topic outside the loaded material, say the assistant does not know from its sources and direct the user to an appropriate human/official channel (the project example says to ask the panchayat). Do not fabricate an answer or imply a negative eligibility result merely because the system lacks information.

## 5. Screen and component specifications

The following describes functional responsibilities. It does not claim exact visual styling where the record contains no final design file.

### Language and welcome screen

- Language choices for supported languages; initial examples are Hindi and English, while final second language remains open.
- Clear primary action to continue and a spoken/readable welcome if implemented.
- Preserve the selected language into the demo and assistant.

### Guided demo overlay and practice area

- One focused instruction at a time, tied to the control the user should activate.
- Highlight the target UI element; avoid blocking the target or essential context.
- Practice prompt in selected language; microphone practice affordance; simulated response area; replay/listen control if audio is provided.
- Progress cue and controls for repeat, next/continue, and skip. Provide a way to recover from accidental taps.
- Persistent indication that responses are scripted/demo content, not live AI output.

### Conversation workspace

- Conversation history with distinct user and assistant turns.
- Assistant text response with source attribution and a listen/play control.
- Voice input control with clear listening/processing/ready states; stop/cancel affordance while recording or processing.
- Typed input and send action as a fallback and as the primary chat-mode path.
- Mode indicator/switch that preserves the current conversation.
- Simple suggested questions to help users begin; the referenced friction analysis recommends making these playable as audio.
- Progress or question count for an eligibility interview is a proposal; avoid a long intimidating form.

### Eligibility result and take-away card

- Result label: likely eligible / likely not eligible / cannot tell yet.
- Short explanation grounded in the relevant rule; show missing details where applicable.
- Documents to carry, where to apply, and official source/document date when available.
- Indicative-only notice close to the result and card.
- Save/share as image or PDF is P1 in the project plan, not a guaranteed P0 capability.

### Helper context

Helper mode (asking on someone else’s behalf) is P1. If implemented, make it clear whose answers are being entered and avoid implying that the helper’s own details determine the outcome. Exact consent and data handling are unresolved.

## 6. Frontend-to-backend data flow

This section defines a logical data flow, not an API contract. No endpoint, schema, service, vendor, or stack is established in the available materials.

### Demo path

1. Frontend tracks the current demo step and selected language.
2. User input/action is interpreted by the demo controller, which maps the action or recognized sample utterance to a predefined demo state and response.
3. Frontend displays the scripted output and any prepared audio. The demo must not send a real question to the live AI backend.
4. On demo completion, frontend transitions to the selected live mode.

**Implementation choice open:** whether scripted demo content is bundled in the frontend or served as static content. Either way, it must be deterministic and available without relying on the live AI service.

### Live path

1. Frontend captures a typed message or records speech after the user activates the microphone and grants browser/device permission.
2. Speech handling converts spoken audio to text (speech-to-text). Whether transcription is performed on-device or by a service is undecided.
3. Frontend presents the recognized text for correction when feasible, especially before consequential eligibility answers. The project identifies speech errors and accents/noise as risks; transcript confirmation UI is a proposal.
4. Frontend sends the user message and the minimum conversation context needed to continue the interaction to the backend through an implementation-defined interface. The UI must preserve turn ordering and associate the response with the correct conversation. Exact fields and transport are not specified here.
5. Backend is expected by the project plan to retrieve from loaded official documents, handle eligibility question logic for selected schemes, generate a grounded response or refusal, and return source information. These are logical responsibilities only; actual service boundaries are open.
6. Frontend renders the text, source, eligibility state/card when returned, and speaks the answer when audio is available/requested.
7. User’s next voice or text turn follows the same conversation and assessment state. Mode switching must not reset it.

### Logical information categories

Potential information exchanged, subject to backend contract and data minimization:

- User message as typed text or a speech transcript; raw audio only if the chosen speech service requires it.
- Selected language and interaction mode.
- Minimal conversation/session reference and prior turns needed for context.
- Eligibility answers intentionally provided by the user and the selected scheme.
- Assistant response text, spoken-audio data/reference if applicable, result category, reasons/missing information, citations/source metadata, and take-away-card content.
- Processing status or recoverable error category.

These are not finalized field names or commitments to persist data. Do not collect identity numbers, payment status, or unrelated personal details. The project explicitly excludes private-record lookups.

## 7. Voice and text processing behavior

- Accept natural conversational Hindi; the project also plans a second language, not yet selected. Dialect/accent performance is an acknowledged limitation.
- Keep prompts and answers short, everyday, and free of unexplained government terminology.
- Speak complete assistant responses in voice-only flow, including eligibility criteria and next steps; do not make the user read a card to finish.
- Provide text alongside audio in combined mode; provide replay/listen controls for assistant output.
- Support correction, repeat, or rephrasing after speech recognition mistakes. Typed input is the fallback when voice fails.
- Ask one question at a time for eligibility; allow “I don’t know” or an equivalent response when appropriate, then explain if the result cannot yet be determined.
- Show the recognized input where possible and let the user confirm/correct consequential details. This is a proposal grounded in the source’s recommendation to confirm important answers.
- Speech accuracy may drop with noise and accents. Do not present a transcript as certain when confidence is low; exact confidence thresholds and speech provider are open.

## 8. User friction and mitigations

| Friction | User impact | Established mitigation / recommendation | Status |
| --- | --- | --- | --- |
| Not knowing how to start | User opens the app but cannot decide what to tap or ask | Prominent microphone, spoken welcome, simple suggested questions, interactive onboarding demo | Prominent mic and demo are in the direction; exact layout open |
| Difficulty reading or writing | Text chatbot blocks the intended audience | Complete voice-only path; speak prompts and full answers; allow switch to text | Established direction |
| Fear of speaking to a device / unfamiliar controls | User may abandon before first useful answer | Practice with highlighted navigation and a scripted response before live AI | Established demo concept |
| Speech recognition errors, accents, noise | Wrong scheme or eligibility answer | Natural language, short prompts, repeat/rephrase, typed fallback, confirm key answers | Recommendations in referenced UX discussion; provider/performance open |
| Formal government language | User misunderstands requirements | Everyday language, concise explanations, source shown, explain terms | Established product goal/recommendation |
| Eligibility interview feels long | Fatigue, incomplete answers | Ask only required questions, one at a time; aim for 3–5 relevant questions | Project canvas target; actual scheme rules determine count |
| User does not know an answer | False outcome or stalled flow | Allow unknown; state “cannot tell yet” and identify missing information | Established result category |
| Trust / privacy concern | User withholds information or fears misuse | Explain purpose, ask only necessary details, no private-record lookup, show source and indicative caveat | Privacy controls are recommendations; policy/retention details open |
| Mode change loses work | Repetition and frustration | Preserve history and eligibility state across voice/text changes | Explicitly established |
| Answer has no actionable next step | User still must search or make repeat trips | Take-away card with documents, where to apply, and source; read it aloud | Established product direction |
| Unsupported question gets a confident guess | User may act on false information | Refuse beyond loaded documents and direct to an official/help channel | Established grounding/refusal requirement |
| Permission, network, or service failure | Voice-first path cannot continue | Explain the issue simply; offer retry and typing where possible; keep the user’s entered text | Failure fallback is in project plan; exact recovery UI is proposal |

## 9. Error, loading, and recovery states

These are required UX cases from the project roadmap’s test checklist plus the voice design. Exact copy should be localized and user-tested.

- **Microphone permission denied/unavailable:** explain that voice input is unavailable and offer typed input; if possible give a clear way to retry permission.
- **Recording cancelled or empty:** return to ready state without submitting an empty turn; let the user try again or type.
- **Speech not understood / noisy audio:** say the system did not catch it, offer replay/rephrase, and provide text entry. Do not silently substitute an uncertain transcript.
- **Slow response:** show a calm in-progress state and allow cancellation/retry without duplicating a turn.
- **Network/backend failure:** state that the response could not be loaded, retain the unsent user message where safe, and offer retry or typed/demo fallback as applicable.
- **Unexpected or malformed response:** show a plain-language failure and safe recovery; never render raw technical errors or infer an eligibility result.
- **Empty or invalid input:** explain what can be entered; do not advance an eligibility assessment on an empty answer.
- **Audio playback unavailable:** keep text available and provide a retry/listen control if supported; in voice-only mode explain the limitation and offer a repeat or alternate channel.
- **Refresh/re-entry:** recovery of conversation state is not specified. Decide whether the hackathon demo is session-only or persistent; do not promise recovery until implemented.
- **Demo/live confusion:** visibly label scripted practice, and clearly signal when the real assistant starts.

## 10. Accessibility, privacy, and trust

### Accessibility requirements

- A user must be able to complete the main task without reading or typing.
- Pair important visual prompts with spoken guidance in voice mode; never rely only on color, animation, or a small icon to explain the next step.
- Use large, well-spaced touch targets and plain-language labels (exact dimensions are an implementation/design decision).
- Keep speech and text synchronized by turn; ensure audio can be replayed and stopped.
- Keep one primary action clear at each demo step; support keyboard and assistive technology semantics in web contexts.
- Provide visible focus, adequate contrast, scalable text, and accessible names for controls; verify across web and small-screen layouts.
- Avoid time-limited steps in onboarding. Make replay and skip available.

### Privacy and trust requirements

- Request microphone access only when the user chooses voice input and explain its purpose in plain language.
- Collect the minimum information needed to answer the scheme questions. Never ask for Aadhaar/payment status or claim to retrieve private government records in this scope.
- Explain that eligibility results are indicative and must be confirmed with the relevant office/portal.
- Show the official source supporting answers, including its date when available; refuse beyond loaded sources.
- Demo answers are synthetic/predetermined and must be disclosed as practice content.
- Data retention, raw-audio handling, consent wording, logging, encryption, and account requirements are unresolved implementation/policy assumptions. Decide them before handling real personal data; this document does not assert that any particular protection is already implemented.

## 11. Web and mobile behavior

The referenced request asks for web and mobile considerations, but the available project files do not specify final visual mockups. Treat the following as responsive behavior requirements, not approved pixel designs.

- **Small screens:** prioritize the current prompt/response and one clear next action; keep microphone and text fallback reachable; prevent the keyboard from covering the active question or send action; keep the result card readable and speakable.
- **Wider screens:** retain a clear conversation hierarchy with the answer and source visible; a separate source/card area may be used if approved by design. Avoid splitting attention in voice-only use.
- **Both:** the same selected language, mode, demo progress, conversation, and assessment semantics should apply. Touch, keyboard, and screen-reader operation should be possible as relevant to the platform.
- Breakpoints, navigation shell, portrait/landscape behavior, and offline behavior are unconfirmed. Offline mode is explicitly out of scope before P2.

## 12. Priorities and delivery scope

Project priority labels are preserved from `sources/DECISIONS.md`:

- **P0:** Hindi spoken or typed input with speech-to-text; collect/clean official documents for 5–8 schemes and record dates; grounded retrieval with sources and refusal outside coverage; eligibility flow for 2–3 schemes; spoken and on-screen answer; take-away card; ~30-question test set and scorecard script.
- **P1:** second language; save card as image/PDF; helper mode; scorecard page in app.
- **P2:** cached offline answers; WhatsApp/SMS; more schemes.

The interactive onboarding demo is explicitly part of the user’s requested finalized experience, but it is not separately assigned a P0/P1 priority in the project decision canvas. Confirm how it fits the event build scope. Do not misrepresent a scripted demo as the live AI pipeline.

## 13. Acceptance criteria

The following combine explicit project checks with UX criteria needed for a reviewable implementation. They are acceptance targets, not evidence of current completion.

### Onboarding demo

- A new user can select a language and follow sequential instructions to practice the microphone/navigation.
- Demo uses predetermined responses and makes no real-AI request.
- User can repeat, continue, or skip remaining demo steps.
- User can select voice or chat after practice; selected mode is visible on entering the live assistant.
- Demo and live conversation are clearly distinguishable; each step has understandable recovery.

### Conversation and eligibility

- User can begin by voice or typing; typed input works when speech fails.
- Assistant response is available on screen and can be heard; voice-only path provides the full useful answer without requiring reading.
- User can switch modes without losing conversation history or restarting the eligibility assessment.
- Eligibility questions are grounded in official scheme rules, asked one at a time, and limited to relevant information.
- Outputs distinguish likely eligible, likely not eligible, and cannot tell yet; missing information and reasoning are clear.
- Source is shown; unsupported requests are refused rather than guessed.
- Take-away card contains all required documents for each demo scheme, where to apply, source, and indicative-only caveat.

### Failure and quality

- Exercise empty/invalid input, slow response, failed request, unexpected output, page refresh, and small-screen layout per roadmap checklist.
- Test typical, edge, ambiguous, out-of-scope, and service-failure cases; record actual results rather than assumed success.
- For the planned test set (~30), measure correct answers with correct official source, correct out-of-scope refusals, card completeness, speech transcription on recorded sentences, and time to card. No score target is set yet.
- A teammate who did not build the feature can run the main workflow from a clean start and explain what happened.

## 14. Implementation assumptions to resolve

1. What approved UI designs or screenshots define the “finalized” visual interface, including web and mobile variants?
2. Is the first language pair Hindi + English, or Hindi + another team-validated language? The conversation uses Hindi/English examples; the project canvas leaves the second language open.
3. Which schemes are selected, which have ask-back eligibility interviews, and which official documents/versions are authoritative?
4. Which speech-to-text/text-to-speech/model/retrieval providers and hosting arrangement will be used? Do not encode vendor-specific UI assumptions before this is decided.
5. What is the frontend/backend interface and response contract? Define with the backend team; this document intentionally gives no endpoint or field schema.
6. Does speech audio leave the device? Is raw audio stored? What data is retained and for how long? What consent and deletion behavior apply?
7. Does the demo ship with scripted content and audio locally, and what exact prepared utterances/responses/languages are needed?
8. Is combined mode a named third choice, or a voice/chat preference with optional text/audio controls? The conversation supports voice-only, text, and both, but final control semantics are not recorded.
9. Is conversation state session-only or persistent across reloads/devices? Are accounts intentionally excluded from the demo?
10. Is card export included in the event build or deferred to P1? Is helper mode included or deferred to P1?
11. What localization, audio assets, pronunciation review, and human validation are available for the second language and scheme terminology?
12. What official destination can be recommended for each scheme, and what wording is approved for the indicative result and escalation/refusal?

## 15. Reference record and limitations

This document draws on:

- Referenced ChatGPT conversation **“Trivon Mentor Setup”** (conversation ID `6ae47b45-a3c4-83ec-8f1d-712f6c8c97d6`), including the request for an interactive dummy onboarding exercise and the voice-first/text-supported chatbot direction.
- `sources/DECISIONS.md` — TRIVON Solution Canvas, delivery priorities, product scope, metrics, and open decision register.
- `sources/Yojana Mitra Hackathon Roadmap & Checklist.md` — build, testing, freeze, and delivery checklist.

The available conversation record is a bounded preview and omits portions of earlier UX discussion. The source canvas also states that design details remain open. Therefore this file records all visible decisions and requirements, but should not be treated as proof of missing visual decisions or as a backend/API specification. Update the open assumptions when the team confirms them.
