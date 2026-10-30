# Yojana Mitra — Phase 3.3
# API Contract & Project Structure

**Team:** TRIVON  
**Date:** 30 October 2026  
**Phase:** 3.3 — API Contract and Structure  
**Status:** FROZEN  
**Previous phase:** Phase 3.2 — Technology Stack & Architecture (FROZEN)  
**Next step:** Implementation

---

## 1. Purpose

This document defines the agreed API contract, shared data formats, project folder structure, team ownership, environment variable names, run instructions and mock-data policy for Yojana Mitra.

It serves as the common implementation reference for the frontend, backend, AI workflow and data components.

All implementation must follow this contract unless a technical blocker requires an explicitly reviewed change.

## 2. Frozen Technology Baseline

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript + Vite |
| Styling | Tailwind CSS |
| Backend | Python + FastAPI |
| Orchestration | LangGraph |
| LLM | Google Gemini |
| Eligibility engine | Deterministic Python rules |
| Database | Supabase PostgreSQL |
| Retrieval | PostgreSQL full-text search + pgvector |
| Document storage | Supabase Storage |
| Frontend hosting | Vercel |
| Backend hosting | Render |
| Version control | Git + GitHub |

## 3. API Contract

### 3.1 API conventions

- Base path: `/api/v1`
- Request and response formats: JSON unless the endpoint accepts multipart audio.
- Session identifiers connect consecutive conversation turns.
- Text and voice requests enter the same conversation workflow.
- Both input methods return the same standard response structure.
- All timestamps use ISO 8601 format.
- Errors follow one consistent error schema.
- Eligibility results are indicative, not official approvals.

### 3.2 Endpoint summary

| Endpoint | Method | Input | Output | Error cases | Owner |
|---|---|---|---|---|---|
| `/api/v1/sessions` | POST | `language`, `mode` | `session_id`, `status`, session metadata | 422 invalid input, 500 creation failure | Ankush |
| `/api/v1/sessions/{session_id}` | GET | Session ID in path | Session details and conversation turns | 404 session missing, 500 database failure | Ankush |
| `/api/v1/turns` | POST | `session_id`, `text` | Standard turn response | 400 empty input, 404 session missing, 503 AI/retrieval unavailable | Ankush |
| `/api/v1/voice/turns` | POST | Multipart `session_id`, `audio`, optional `language` | Standard turn response plus transcription | 400 invalid audio, 413 payload too large, 503 STT unavailable | Ankush |

### 3.3 Create session

**Endpoint:** `POST /api/v1/sessions`

Request:

```json
{
  "language": "hi",
  "mode": "voice"
}
```

Success — HTTP 201:

```json
{
  "session_id": "sess_demo_001",
  "status": "active",
  "language": "hi",
  "mode": "voice",
  "created_at": "2026-10-30T18:30:00Z"
}
```

Error — HTTP 422:

```json
{
  "error": {
    "code": "INVALID_SESSION_INPUT",
    "message": "The selected language or mode is not supported.",
    "retryable": false,
    "details": {}
  }
}
```

### 3.4 Retrieve session

**Endpoint:** `GET /api/v1/sessions/{session_id}`

Success — HTTP 200:

```json
{
  "session_id": "sess_demo_001",
  "status": "active",
  "language": "hi",
  "mode": "voice",
  "turns": [
    {
      "turn_id": "turn_001",
      "role": "user",
      "text": "क्या मैं उज्ज्वला योजना के लिए पात्र हूं?"
    },
    {
      "turn_id": "turn_002",
      "role": "assistant",
      "text": "क्या आपके घर में पहले से LPG कनेक्शन है?"
    }
  ]
}
```

Error — HTTP 404:

```json
{
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "The requested conversation session was not found.",
    "retryable": false,
    "details": {}
  }
}
```

### 3.5 Submit text turn

**Endpoint:** `POST /api/v1/turns`

Request:

```json
{
  "session_id": "sess_demo_001",
  "text": "क्या मैं प्रधानमंत्री उज्ज्वला योजना के लिए पात्र हूं?"
}
```

Success — HTTP 200:

```json
{
  "session_id": "sess_demo_001",
  "turn_id": "turn_003",
  "status": "awaiting_information",
  "language": "hi",
  "answer": {
    "text": "मैं आपकी पात्रता समझने में मदद करूंगा। क्या आपके घर में पहले से LPG कनेक्शन है?"
  },
  "assessment": null,
  "card": null,
  "sources": [],
  "speech": {
    "status": "generated",
    "content_type": "audio/mpeg",
    "audio_base64": "DEMO_AUDIO_DATA"
  }
}
```

Error — HTTP 503:

```json
{
  "error": {
    "code": "AI_SERVICE_UNAVAILABLE",
    "message": "The assistant is temporarily unavailable. Please try again or use text input later.",
    "retryable": true,
    "details": {}
  }
}
```

### 3.6 Submit voice turn

**Endpoint:** `POST /api/v1/voice/turns`

Request format: `multipart/form-data`

| Field | Type | Required |
|---|---|---|
| `session_id` | String | Yes |
| `audio` | Audio file | Yes |
| `language` | String | No |

Success — HTTP 200:

```json
{
  "session_id": "sess_demo_001",
  "turn_id": "turn_004",
  "status": "awaiting_information",
  "language": "hi",
  "transcription": {
    "text": "मेरे घर में पहले से गैस कनेक्शन नहीं है।",
    "confidence": null
  },
  "answer": {
    "text": "समझ गया। क्या आवेदन करने वाली महिला की उम्र 18 वर्ष या उससे अधिक है?"
  },
  "assessment": null,
  "card": null,
  "sources": [],
  "speech": {
    "status": "generated",
    "content_type": "audio/mpeg",
    "audio_base64": "DEMO_AUDIO_DATA"
  }
}
```

Error — HTTP 503:

```json
{
  "error": {
    "code": "STT_UNAVAILABLE",
    "message": "We could not process the audio. Please try again or type your response.",
    "retryable": true,
    "details": {}
  }
}
```

**Audio transport note:** `DEMO_AUDIO_DATA` is illustrative, not playable audio. The implementation must agree on actual Base64 audio delivery or an audio URL before enabling production playback.

### 3.7 Standard final assessment response

This is the agreed response structure for a completed eligibility assessment.

```json
{
  "session_id": "sess_demo_001",
  "turn_id": "turn_010",
  "status": "completed",
  "language": "hi",
  "answer": {
    "text": "आपके दिए गए उत्तरों के आधार पर आप संभवतः पात्र हैं। अंतिम पुष्टि LPG वितरक द्वारा होगी।"
  },
  "assessment": {
    "scheme_id": "pmuy",
    "result": "likely_eligible",
    "reasons": [
      "आवेदक महिला है और उसकी उम्र 18 वर्ष या अधिक है।",
      "परिवार के पास पहले से LPG कनेक्शन नहीं है।"
    ],
    "missing_information": []
  },
  "card": {
    "scheme_name": "प्रधानमंत्री उज्ज्वला योजना",
    "documents": [
      "आधार कार्ड",
      "राशन कार्ड या परिवार संरचना का प्रमाण",
      "बैंक पासबुक"
    ],
    "where_to_apply": [
      "LPG वितरक",
      "Common Service Centre"
    ],
    "disclaimer": "यह केवल प्रारंभिक पात्रता जानकारी है, आधिकारिक स्वीकृति नहीं।"
  },
  "sources": [
    {
      "document_id": "pmuy_official_001",
      "title": "PMUY Official Guidelines",
      "url": "https://example.gov.in/official-document",
      "page": 4
    }
  ],
  "speech": {
    "status": "generated",
    "content_type": "audio/mpeg",
    "audio_base64": "DEMO_AUDIO_DATA"
  }
}
```

**Important:** This is an illustrative schema example, not a verified eligibility result. The example URL and outcome must not be used as actual official evidence. Real results must come from verified scheme rules and official documents.

## 4. Shared Data Formats

### 4.1 Language and interaction mode

```json
{
  "language": "hi",
  "mode": "voice"
}
```

Allowed values:

- Language: `hi`, `en`
- Mode: `voice`, `text`, `combined`

### 4.2 Session

```json
{
  "session_id": "sess_demo_001",
  "language": "hi",
  "mode": "voice",
  "status": "active"
}
```

### 4.3 Conversation turn

```json
{
  "turn_id": "turn_001",
  "role": "user",
  "text": "User message",
  "created_at": "2026-10-30T18:30:00Z"
}
```

Roles: `user`, `assistant`.

### 4.4 Assessment

```json
{
  "scheme_id": "pmuy",
  "result": "cannot_determine",
  "reasons": [],
  "missing_information": [
    "household_lpg_connection"
  ]
}
```

Allowed results:

- `likely_eligible`
- `likely_not_eligible`
- `cannot_determine`

### 4.5 Evidence reference

```json
{
  "document_id": "pmuy_official_001",
  "title": "Official scheme document",
  "url": "https://example.gov.in/document",
  "page": 4,
  "section": "Eligibility"
}
```

### 4.6 Standard error

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "retryable": false,
    "details": {}
  }
}
```

### 4.7 LangGraph shared state

The internal workflow state must support:

- `session_id`
- `language`
- `input_type`
- `user_text`
- `intent`
- `scheme_id`
- `eligibility_answers`
- `retrieved_evidence`
- `assessment`
- `response`
- `error`

Internal state is not the public API response. Prompts, private reasoning and internal workflow details must not be exposed to the frontend.

### 4.8 Eligibility engine interface

Input:

```json
{
  "scheme_id": "pmuy",
  "answers": {
    "applicant_is_woman": true,
    "age_18_or_above": true,
    "household_has_lpg": false
  }
}
```

Output:

```json
{
  "result": "cannot_determine",
  "reasons": [],
  "missing_information": [
    "poor_household_declaration"
  ]
}
```

Python owns the final eligibility evaluation. Gemini may explain the result but cannot override the rule engine.

### 4.9 Retrieval result

```json
{
  "scheme_id": "pmuy",
  "document_id": "pmuy_official_001",
  "chunk_id": "chunk_004",
  "text": "Retrieved official document passage.",
  "source_url": "https://example.gov.in/document",
  "page": 4,
  "document_version": "current_verified_version"
}
```

## 5. Frozen Folder Structure and Ownership

```text
yojana-mitra/
│
├── frontend/                         # Aditya
│   ├── src/
│   │   ├── components/               # Reusable UI components
│   │   ├── pages/                    # Home, conversation, result
│   │   ├── services/                 # Backend API client
│   │   ├── hooks/                    # Voice and session hooks
│   │   ├── types/                    # Frontend TypeScript types
│   │   ├── mocks/                    # Mock API responses
│   │   └── App.tsx                   # Application entry component
│   ├── public/                       # Static assets
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                          # Ankush
│   ├── app/
│   │   ├── main.py                   # FastAPI application entry
│   │   ├── api/
│   │   │   └── routes/               # Session, turn and voice endpoints
│   │   ├── schemas/                  # Pydantic request/response models
│   │   ├── graph/                    # LangGraph workflow and state
│   │   ├── agents/                   # Logical workflow node implementations
│   │   ├── services/                 # Gemini, STT and TTS integrations
│   │   ├── retrieval/                # Search, ranking and evidence retrieval
│   │   ├── eligibility/              # Deterministic Python rules
│   │   ├── database/                 # Supabase connection and persistence
│   │   └── core/                     # Settings, configuration and errors
│   ├── tests/                        # Backend and integration tests
│   └── requirements.txt
│
├── data/                             # Anamika
│   ├── documents/                    # Official source documents
│   ├── extracted/                    # Extracted document text
│   ├── schemes/                      # Scheme metadata and rules
│   └── evaluation/                   # Test questions and expected results
│
├── shared/                           # Ankush + Aditya
│   ├── api-contract.md               # API contract
│   └── examples/                     # Canonical JSON examples
│
├── docs/                             # Ankush
│   ├── architecture.md               # Frozen architecture reference
│   └── decisions.md                  # Decision register
│
├── .env.example                      # Variable names, no real secrets
├── .gitignore                        # Secrets and generated files
└── README.md                         # Setup and run instructions
```

### Ownership rules

- Aditya owns `frontend/`.
- Ankush owns `backend/`, `shared/` and integration.
- Anamika owns scheme research, extraction and evaluation data in `data/`.
- Shared API contract changes require agreement between frontend and backend owners.
- Every person must work within their assigned folder unless ownership is agreed.
- The `agents/` folder contains logical workflow nodes, not necessarily independent autonomous agents.

## 6. Environment Variables

### Backend

| Variable | Purpose |
|---|---|
| `APP_ENV` | Application environment |
| `APP_PORT` | Backend port |
| `CORS_ORIGINS` | Allowed frontend origins |
| `GEMINI_API_KEY` | Gemini authentication |
| `GEMINI_MODEL_HIGH` | High-tier model ID |
| `GEMINI_MODEL_MID` | Mid-tier model ID |
| `GEMINI_MODEL_LITE` | Lite-tier model ID |
| `STT_PROVIDER` | Selected STT provider |
| `STT_API_KEY` | STT authentication |
| `STT_MODEL` | STT model identifier |
| `TTS_PROVIDER` | TTS provider |
| `TTS_API_KEY` | TTS authentication |
| `TTS_MODEL` | TTS model identifier |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_ANON_KEY` | Public/anonymous Supabase key |
| `SUPABASE_SERVICE_ROLE_KEY` | Backend-only privileged key |
| `DATABASE_URL` | PostgreSQL connection |
| `MOCK_MODE` | Backend mock processing switch |
| `LOG_LEVEL` | Logging verbosity |

### Frontend

| Variable | Purpose |
|---|---|
| `VITE_API_BASE_URL` | Backend API base URL |
| `VITE_MOCK_MODE` | Frontend mock-data switch |

**Security rules:**

- Never expose `SUPABASE_SERVICE_ROLE_KEY` in frontend code.
- Never expose provider API keys in frontend code.
- Keep actual secrets in local environment files and deployment secrets.
- Commit only variable names in `.env.example`.

## 7. Run Instructions

### Frontend

1. Open the `frontend/` directory.
2. Install dependencies using the package manager.
3. Configure the frontend environment variables.
4. Start the Vite development server.

### Backend

1. Open the `backend/` directory.
2. Create and activate a Python virtual environment.
3. Install dependencies from `requirements.txt`.
4. Configure backend environment variables.
5. Start the FastAPI application using an ASGI server with development reload enabled.

### API documentation

After the backend starts, use FastAPI's generated Swagger documentation at `/docs`.

### Testing

- Run backend tests using pytest.
- Run frontend tests using the configured JavaScript test runner.
- Test the frontend with mock data before integrating real backend services.
- Run end-to-end tests against real processing before the final demo.

### Production

- Build the frontend for deployment.
- Deploy the frontend through Vercel.
- Deploy the backend through Render.
- Configure Supabase connectivity and secrets.
- Run the application without development reload.

## 8. Mock Data vs Real Data Policy

### Mock mode

Use mock data when:

- Frontend screens are being developed.
- Backend endpoints are not ready.
- UI interactions need predictable responses.
- Loading, error and empty states are being tested.
- Rehearsing without consuming provider API quotas.

Mock responses must follow the exact same schema as real API responses.

### Real mode

Use real services when:

- Testing Gemini integration.
- Testing STT and TTS.
- Retrieving official scheme information.
- Running actual eligibility rules.
- Testing database persistence.
- Performing end-to-end evaluation.

### Switching

Use the following configuration switches:

- Frontend: `VITE_MOCK_MODE`
- Backend: `MOCK_MODE`

The frontend mock service must return the same structures as the real API client.

Backend mock mode may replace external provider responses with predictable data, but it must not silently replace actual eligibility rules during evaluation.

### Mandatory safeguards

1. Never mix mock assessment results with real assessment results in the same evaluation.
2. Clearly label sample and demo data.
3. Never display fabricated official sources.
4. Mock audio must not be presented as actual STT or TTS performance.
5. Before the final demo, identify every feature as built, partial, mocked, planned or measured.
6. Run the final scorecard against real processing wherever functionality is claimed.

## 9. Implementation Notes

The following are agreed contract details that must be handled carefully during implementation:

1. The sample audio Base64 value is a placeholder. Actual audio delivery must be implemented and tested.
2. Session persistence is part of the contract. Retention and deletion behaviour must be defined consistently with the privacy requirements.
3. The PMUY final assessment example is illustrative and must not be used as a verified eligibility result.
4. Placeholder source URLs must be replaced with actual official documents.
5. The eligibility engine must return `cannot_determine` when required information is missing.
6. The API must preserve conversation state when switching between voice and text.
7. Errors must use the standard error envelope.
8. The frontend must not depend on internal LangGraph state.

## 10. Implementation Handoff Checklist

### Ankush — Backend and AI

- [ ] Implement FastAPI application entry.
- [ ] Implement session endpoints.
- [ ] Implement text and voice turn endpoints.
- [ ] Define Pydantic schemas matching this contract.
- [ ] Implement LangGraph shared state.
- [ ] Integrate Gemini model routing.
- [ ] Integrate retrieval and evidence references.
- [ ] Integrate deterministic eligibility engine.
- [ ] Integrate Supabase persistence.
- [ ] Implement error handling and safe fallbacks.
- [ ] Add backend tests.

### Anamika — Data and Evaluation

- [ ] Collect official scheme documents.
- [ ] Maintain source metadata and document versions.
- [ ] Extract and organize document text.
- [ ] Verify eligibility rules against official documents.
- [ ] Complete STT benchmark.
- [ ] Prepare evaluation questions and expected answers.
- [ ] Validate retrieval and assessment results.

### Aditya — Frontend

- [ ] Implement application shell and navigation.
- [ ] Implement session creation.
- [ ] Implement shared conversation interface.
- [ ] Integrate text input.
- [ ] Integrate microphone and audio playback.
- [ ] Implement loading, error and retry states.
- [ ] Implement assessment result UI.
- [ ] Implement take-away card.
- [ ] Integrate mock API responses first.
- [ ] Switch to real API responses after backend integration.

### Integration gate

Before considering the implementation integrated:

- [ ] Frontend and backend use the same contract.
- [ ] Session state persists across turns.
- [ ] Text and voice use the same workflow.
- [ ] Eligibility results come from deterministic Python rules.
- [ ] Official evidence is attached to factual responses.
- [ ] Error handling works.
- [ ] Mock and real modes are distinguishable.
- [ ] A teammate who did not build the feature can run the full workflow.

## 11. Decision Record

**DECISION RECORD — Phase 3.3 — 30 October 2026**

### FROZEN DECISIONS

1. Four API endpoints: session creation, session retrieval, text turn and voice turn.
2. Standard JSON response and error formats.
3. Shared conversation state for voice and text.
4. Standard assessment, evidence and retrieval formats.
5. Seven logical LangGraph nodes remain the architecture baseline.
6. Python deterministic eligibility interface.
7. Agreed folder structure and team ownership.
8. Agreed environment variable names.
9. Vercel, Render and Supabase deployment architecture.
10. Frontend and backend mock-mode switches.
11. Mock and real-data separation rules.
12. Implementation responsibilities assigned to Ankush, Anamika and Aditya.

### PHASE STATUS

**PHASE 3.3: FROZEN**

The API contract and project structure decisions are approved.

Freezing this phase means the design and interfaces are agreed. It does not claim that implementation, testing or deployment has already been completed.

### NEXT

Proceed to implementation using this document as the shared reference.

**No unapproved API redesign, folder restructuring or technology substitution should be introduced during implementation.** Any necessary deviation must be raised, explained and agreed by the team.
