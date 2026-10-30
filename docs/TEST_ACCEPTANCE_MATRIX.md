# Yojana Mitra — Test and Acceptance Matrix

**Status:** Planned acceptance register; no test has been run or passed by this document.  
**Rule:** Record actual environment, build/revision, inputs, expected result from authoritative sources, observed result, pass/fail, evidence link and runner in `BUILD_EVIDENCE_LOG.md`. Missing source case details remain **OPEN**.

## Frozen PMUY baseline

The frozen decision record adopts PMUY-T01 through PMUY-T12 as the baseline. The exact case inputs and expected outcomes are absent from the inspected project copy. Do not invent or rename test cases; retrieve the authoritative PMUY test artifact before execution. Enter each case separately below once available.

| Case | Source input / expected outcome | Execution | Acceptance | Status |
| --- | --- | --- | --- | --- |
| PMUY-T01 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T02 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T03 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T04 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T05 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T06 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T07 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T08 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T09 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T10 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T11 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |
| PMUY-T12 | **OPEN — authoritative case definition required** | Real API per approved baseline | Match source expected result; record evidence | OPEN |

## Acceptance coverage

| ID | Area and check | Acceptance condition | Required evidence | Owner(s) | Status |
| --- | --- | --- | --- | --- | --- |
| AT-01 | Clean-start primary journey, Hindi | Start at clean state; complete PMUY text interview and result | Run notes/screenshot or recording allowed by event rules; build and time | Aditya + Ankush | OPEN |
| AT-02 | Clean-start primary journey, English | Same core path in English | Run notes and observed output | Aditya + Ankush | OPEN |
| AT-03 | Deterministic rules and uncertainty | Unknown/missing/unclear/contradictory inputs are not silently No/pass; D13 once via R03; R07 kept outside eligibility | Rule-to-KB review and T01–T12 results | Anamika + Ankush | OPEN |
| AT-04 | Eligibility vs readiness/verification | Separate outputs/claims; missing documents affect readiness, not eligibility | Contract/code behavior review against authoritative artifacts | Anamika + Ankush | OPEN |
| AT-05 | Grounding and refusal | Official-source provenance is present; unsupported/out-of-source question is refused or unknown | Evidence links and observed response | Ankush + Anamika | OPEN |
| AT-06 | Result/card | Reasons, source and “indicative, not official” disclaimer shown; field mapping matches frozen API | Client/API evidence | Aditya + Ankush | OPEN |
| AT-07 | Voice and text in one session | Switch voice→text→voice without losing agreed session state | Actual device run; exact API behavior per H1 | Aditya + Ankush + Anamika | OPEN |
| AT-08 | STT unavailable | Typed input continues to work | Controlled failure run and observation | Anamika + Aditya | OPEN |
| AT-09 | TTS unavailable | Written answer remains visible | Controlled failure run and observation | Anamika + Aditya | OPEN |
| AT-10 | LLM/Gemini unavailable | Controlled behavior follows approved error/fallback contract; no unsupported answer | Failure run and contract comparison | Ankush | OPEN |
| AT-11 | Retrieval unavailable | No invented factual answer; safe refusal/unknown behavior | Failure run and evidence | Ankush | OPEN |
| AT-12 | Persistence unavailable | Controlled failure; no false success or data loss claim | Failure run and observed state | Ankush | OPEN |
| AT-13 | Input validation | Empty, invalid, unknown and contradictory inputs follow frozen error/rule behavior | Request/response evidence | Ankush + Anamika | OPEN |
| AT-14 | Deployment and client | Frontend reaches backend; CORS/env values, cold start, microphone permission, playback and phone browser checked | Dated device/network checklist; measurements only if recorded | Ankush + Aditya | OPEN |
| AT-15 | Privacy and demo safety | No raw audio persisted by default; no secrets, Aadhaar/bank data, or sensitive real personal data in repo/logs/demo | Review checklist and configuration evidence | All | OPEN |
| AT-16 | Clean reset and independent run | A teammate who did not build it can reset and complete main flow | Runner, steps, outcome and evidence | All | OPEN |

## Unresolved acceptance details

- Exact T01–T12 case data and expected results: **OPEN** pending PMUY test artifact.
- Exact endpoint/error, voice formats, response fields and persistence behavior: **OPEN** pending frozen Phase 3.3/H1–H4 artifacts.
- Event permission for recordings/screenshots, target devices, demo slot, thresholds for latency/audio size, and definition of “correct with source/refusal”: **OPEN — event/team confirmation**.
- No numeric performance or accuracy threshold is inferred. Record measurements with method and sample size before making a claim.
