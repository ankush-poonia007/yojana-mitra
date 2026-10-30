# Yojana Mitra — Phase 3.2: Technology Stack & Architecture

**Team:** TRIVON  
**Date:** 30 October 2026  
**Phase status:** OPEN  
**Verdict:** Recommendations approved  
**Next phase:** Phase 3.3 — API Contracts & Project Structure

---

## 1. Purpose

This document records the approved technology stack, AI architecture, orchestration strategy, infrastructure decisions, and implementation requirements for Yojana Mitra.

It is the architectural baseline for implementation.

**Important:** Approval of an architectural decision does not mean its performance or deployment has already been validated. Outstanding validation tasks are explicitly listed below.

## 2. Approved Technology Stack

| Layer | Technology | Decision |
|---|---|---|
| Frontend | React | Approved |
| Frontend language | TypeScript | Approved |
| Frontend tooling | Vite | Approved |
| Styling | Tailwind CSS | Approved |
| Backend | Python | Approved |
| Backend framework | FastAPI | Approved |
| Agent orchestration | LangGraph | Approved |
| LLM provider | Google Gemini | Approved |
| Model strategy | High / Mid / Lite | Approved |
| Speech-to-Text | Benchmark candidates | Winner pending |
| Text-to-Speech | Gemini Lite-tier strategy | Exact model pending |
| Eligibility evaluation | Python deterministic rules | Approved |
| Database | Supabase PostgreSQL | Approved |
| Vector search | PostgreSQL + pgvector | Approved design |
| Keyword search | PostgreSQL full-text search | Approved design |
| Document storage | Supabase Storage | Approved design |
| Frontend hosting | Vercel | Approved architecture |
| Backend hosting | Render | Approved architecture |
| Version control | Git + GitHub | Project standard |
| Development environment | Antigravity | Project standard |

## 3. Gemini Model Architecture

### 3.1 Three-tier allocation

| Tier | Model candidate | Responsibilities |
|---|---|---|
| High | Gemini 3.8 Flash | Supervisor and complex verification |
| Mid | Gemini 3.6 Flash | Scheme knowledge and conversational reasoning |
| Lite | Gemini 3.5 Flash-Lite | Intent detection, scheme identification and response formatting |

These are the currently proposed model assignments. Exact API identifiers, availability, quotas and performance must be validated before implementation is finalized.

### 3.2 Seven logical workflow nodes

| # | Node | Responsibility | Processing |
|---|---|---|---|
| 1 | Supervisor | Workflow control and routing | Gemini High |
| 2 | Intent & Language | Detect user intent and language | Gemini Lite |
| 3 | Scheme Identification | Identify the requested scheme | Gemini Lite |
| 4 | Scheme Knowledge | Explain official scheme information | Gemini Mid |
| 5 | Eligibility Engine | Evaluate eligibility conditions | Deterministic Python |
| 6 | Verification | Check claims against official evidence | Gemini High when required |
| 7 | Response Generator | Generate structured user-facing output | Gemini Lite |

**Architecture clarification:**

- Seven logical nodes do not mean seven independent LLM calls.
- Nodes execute conditionally through LangGraph.
- Eligibility evaluation must remain deterministic Python logic.
- The LLM must not independently invent or override eligibility rules.

### 3.3 Dynamic routing

The approved routing strategy is task-complexity-based dynamic routing.

Initial routing policy:

1. Simple classification and formatting use Lite.
2. Normal scheme-related reasoning uses Mid.
3. Complex ambiguity and verification can escalate to High.
4. Eligibility calculations execute through Python.
5. Unnecessary nodes are skipped.
6. Retries and fallback behaviour are bounded.

Exact complexity thresholds and call limits remain subject to testing.

## 4. Speech Architecture

### 4.1 Speech-to-Text

Candidates:

- Gemini transcription.
- Groq Whisper Large V3.
- Groq Whisper Large V3 Turbo.

Selection method: benchmark the same Hindi recordings across candidates.

Evaluation criteria:

- Hindi transcription accuracy.
- Accent and code-switching handling.
- Background noise performance.
- Latency.
- API availability and usage limits.

**Owner:** Anamika.

No provider is declared the winner until benchmark results are available.

### 4.2 Text-to-Speech

Approved strategy: Gemini Lite-tier TTS.

The exact model must be validated for:

- Hindi pronunciation.
- Speech clarity and naturalness.
- Response latency.
- API usage limits.
- Replay and playback behaviour.

If TTS fails, the written answer must remain available.

## 5. Retrieval Architecture

### 5.1 Approved approach

Hybrid retrieval:

- PostgreSQL full-text search.
- PostgreSQL pgvector semantic retrieval.
- Combined candidate retrieval.
- Ranking of relevant passages.
- Grounded answer generation.

### 5.2 Retrieval pipeline

1. Identify the requested scheme.
2. Filter the knowledge base by scheme.
3. Retrieve relevant passages through keyword and vector search.
4. Rank retrieved passages.
5. Pass relevant evidence to Gemini.
6. Generate a source-grounded response.
7. Include source references.
8. Refuse unsupported questions when reliable evidence is unavailable.

### 5.3 Document management

**Supabase Storage:**
- Original official documents.

**Supabase PostgreSQL:**
- Scheme metadata.
- Document metadata.
- Extracted text.
- Document versions.
- Source URLs.
- Publication or revision dates.
- Page and section references.
- Retrieval-related metadata.

Document freshness and source traceability must be preserved.

## 6. Eligibility Engine

The eligibility engine will use deterministic Python rules.

Input:
- Scheme identifier.
- Normalized user answers.
- Required eligibility attributes.

Output:
- Indicative eligibility status.
- Reasons.
- Missing information.
- Relevant rule references.
- Verification requirements.

Possible statuses:

- Likely eligible.
- Likely not eligible.
- Cannot determine yet.

Important safeguards:

- Unknown answers must not be treated as negative answers.
- Missing required information must produce an incomplete result.
- Contradictory answers must be flagged.
- Eligibility is indicative, not official approval.
- Required rules must be evaluated before presenting a final result.

## 7. Database and Persistence

Approved database: Supabase PostgreSQL.

The application may persist:

- Session identifiers.
- Selected language and interaction mode.
- Necessary conversation history.
- Eligibility interview answers.
- Assessment results.
- Generated card data.
- Official source references.

### Privacy requirements

- Do not collect Aadhaar numbers or bank details.
- Avoid unnecessary sensitive personal data.
- Keep privileged database operations on the backend.
- Configure Supabase Row Level Security.
- Keep service-role keys and provider API keys out of frontend code.
- Define appropriate retention and deletion behaviour.

## 8. Hosting Architecture

Approved deployment architecture:

- Frontend: Vercel.
- Backend: Render.
- Database and document storage: Supabase.

Before deployment is considered validated, test:

- Frontend-to-backend communication.
- CORS configuration.
- Environment variables.
- API connectivity.
- Cold starts and service availability.
- Microphone permissions.
- Audio playback.
- Mobile browser behaviour.
- Recovery from backend or provider failures.

## 9. Application Behaviour and Fallbacks

### Shared conversation state

Voice and text must use the same conversation state.

Users must be able to switch between interaction modes without losing the current session.

### Failure handling

| Failure | Expected behaviour |
|---|---|
| STT unavailable | Allow typed input |
| TTS unavailable | Display written response |
| Gemini unavailable | Controlled error or approved fallback |
| Retrieval unavailable | Do not invent an answer |
| No reliable evidence | Refuse or request clarification |
| Database unavailable | Controlled failure; do not claim persistence |
| Network interruption | Preserve available session state and provide retry |

Use limited retries and prevent uncontrolled model-to-model calls.

## 10. Standard Architecture Contracts

The following interfaces must be defined consistently before implementation.

### LangGraph state

Shared state should represent:

- Session information.
- User input.
- Language.
- Intent.
- Selected scheme.
- Eligibility answers.
- Retrieved evidence.
- Assessment status.
- Final response.
- Error and processing status.

### Eligibility interface

The LangGraph workflow must pass normalized answers to the Python eligibility engine and receive a structured assessment result.

### Retrieval interface

Each retrieved passage should carry:

- Scheme ID.
- Document ID.
- Source URL.
- Page or section.
- Relevant text.
- Document version or date.

### Response schema

A common structured response must support:

- Text display.
- Spoken output.
- Eligibility result.
- Reasons.
- Missing information.
- Document checklist.
- Application instructions.
- Source references.
- Disclaimer.

### Configuration

Model IDs, provider credentials, routing configuration and service settings must be configurable through backend environment variables.

### Observability

Capture:

- Model calls.
- Latency.
- Errors.
- Retrieval outcomes.
- Routing decisions.
- Workflow execution paths.

Do not log unnecessary sensitive user information.

## 11. Team Ownership

| Member | Primary responsibilities |
|---|---|
| Ankush | LangGraph, Gemini integration, retrieval, eligibility integration, backend architecture |
| Anamika | Official scheme documents, eligibility rule verification, STT benchmarking, evaluation |
| Aditya | Frontend, voice/text interface, audio playback, results and take-away card UI |

## 12. Outstanding Validation Checklist

These items remain open:

- [ ] Complete STT benchmark and select the provider.
- [ ] Validate exact Gemini model IDs and API availability.
- [ ] Verify current model quotas and usage restrictions.
- [ ] Validate Hindi TTS quality and latency.
- [ ] Evaluate hybrid retrieval against the official-document test set.
- [ ] Define and test routing thresholds.
- [ ] Define maximum model calls and retry limits.
- [ ] Validate LangGraph conditional execution.
- [ ] Validate Supabase RLS and access policies.
- [ ] Test Vercel, Render and Supabase integration.
- [ ] Complete end-to-end voice, text, eligibility and card testing.

## 13. Decision Record

### Confirmed decisions

1. React + TypeScript + Vite + Tailwind CSS.
2. Python + FastAPI.
3. LangGraph orchestration.
4. Google Gemini LLM strategy.
5. Three-tier High / Mid / Lite model allocation.
6. Seven logical workflow nodes.
7. Deterministic Python eligibility engine.
8. Dynamic task-complexity-based routing.
9. Supabase PostgreSQL.
10. Gemini Lite-tier TTS strategy.
11. Hybrid keyword + vector retrieval architecture.
12. PostgreSQL full-text search and pgvector.
13. Supabase Storage for original documents.
14. Vercel + Render + Supabase deployment architecture.
15. Shared voice/text conversation state.
16. Privacy-conscious persistence and backend-mediated privileged access.

### Pending validation

- STT provider winner.
- Exact TTS model.
- Exact Gemini API model IDs.
- Provider quotas and availability.
- Retrieval performance.
- Routing thresholds and call limits.
- Database security validation.
- Deployment and integration testing.

### Phase status

**PHASE 3.2: OPEN**

The architectural recommendations have been approved, but validation work remains.

**Do not begin Phase 3.3 until the user explicitly declares Phase 3.2 frozen.**

### Next action

Complete the remaining validation checks, review the resulting architecture and obtain explicit approval to freeze Phase 3.2.

Only then proceed to:

**Phase 3.3 — API Contracts, Folder Structure and Integration Ownership.**