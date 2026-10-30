# Yojana Mitra — Build and Evidence Log

**Purpose:** Record observed build state and evidence. This is a blank log initialized before implementation; it contains no claimed test results, measurements, deployments, or performance metrics.

## Current record

| Item | Status | Evidence / notes |
| --- | --- | --- |
| Phase 5 application implementation | NOT VERIFIED | No application code was changed as part of this documentation task. |
| Tests / acceptance runs | NOT RUN HERE | See `TEST_ACCEPTANCE_MATRIX.md`; actual results must be entered after execution. |
| Performance / speech measurements | NOT MEASURED HERE | No latency, accuracy, payload size, scorecard or baseline number is asserted. |
| Deployment / clean-start demo | NOT VERIFIED | Record actual environment and steps when run. |
| Frozen contracts and rule source artifacts | PARTIALLY AVAILABLE | See `DECISIONS.md`; linked reviewed H1–H4 artifacts, Phase 3.2/3.3 full records, PMUY KB and T01–T12 details were not available in the inspected editable copy. |
| Schedule/checkpoints | OPEN | Confirm actual event times. Historical times are templates only. |

## Evidence entry template

Copy one entry per build, test, measurement, deployment or demo run.

```text
Entry ID:
Date/time and timezone:
Owner / independent runner:
Repository revision or artifact version:
Feature / acceptance IDs:
Environment and device/network:
Mode: MOCKED / REAL / PARTIAL (describe):
Steps and inputs (exclude secrets and personal data):
Expected result and authoritative source:
Observed result:
Outcome: PASS / FAIL / BLOCKED / NOT RUN
Evidence link or repository path:
Limitations / follow-up:
```

## Measurement record template

Record the method, conditions and sample size. Keep measured, estimated and target values distinct; omit unsupported values.

| Measure | Label (MEASURED / ESTIMATED / TARGET) | Method and conditions | Sample size | Value/result | Evidence | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| End-to-end response time | OPEN | OPEN | OPEN | Not measured | — | — |
| Audio payload size | OPEN | OPEN | OPEN | Not measured | — | — |
| STT comparison (Gemini / Whisper Large V3 / Whisper Large V3 Turbo) | OPEN | Benchmark plan frozen; provider not selected | OPEN | Not measured | — | Hindi sample and noise/accent conditions to specify |
| PMUY rule tests T01–T12 | OPEN | Run authoritative cases through agreed path | 12 cases once definitions available | Not run | — | Case definitions unavailable here |
| Retrieval/source scorecard | OPEN | Define against approved test/evidence set | OPEN | Not measured | — | Metric definition and corpus OPEN |
| Baseline task timing | OPEN | Same task and conditions for baseline and prototype | OPEN | Not measured | — | Baseline procedure OPEN |

## Feature state and claims register

Use only `BUILT`, `PARTIAL`, `MOCKED`, `PLANNED`, or `OPEN`, with a linked evidence entry. No product feature is marked BUILT by this initial record.

| Feature | State | Evidence entry | Claim allowed now |
| --- | --- | --- | --- |
| PMUY deterministic eligibility | OPEN | — | Planned scope only; no build/test claim |
| Official-source retrieval and refusal | OPEN | — | Frozen requirement only; no runtime claim |
| Hindi/English text and voice path | OPEN | — | Frozen language scope only; no runtime claim |
| Result and take-away card | OPEN | — | Planned acceptance only |
| Database persistence | OPEN | — | Ankush ownership confirmed; implementation not verified |
| Speech wrappers/benchmark | OPEN | — | Benchmark required; provider/result not selected |
| Deployment / demo path | OPEN | — | No deployment claim |

## Known limitations and open evidence

- The declaration revision currency and domestic PNG interpretation require the confirmations recorded in frozen `DECISIONS.md`.
- PMUY Knowledge Base, PMUY Research Analysis, Phase 3.2/3.3 detailed records, reviewed H1–H4 schemas, and PMUY-T01–T12 exact cases were not inspectable in this repository copy; retrieve them before exact implementation/verification.
- No test result, score, latency, STT accuracy, impact, or deployment status is asserted until an evidence entry supports it.
- Eligibility outputs remain indicative; only official authorities decide eligibility and application acceptance.
- Raw audio must not be persisted by default. Retention/deletion policy must be defined before deployment.
