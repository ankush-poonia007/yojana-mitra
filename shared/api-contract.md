# Yojana Mitra — API Contract & Shared Data Formats

**Phase:** 3.3 — API Contract and Structure  
**Status:** FROZEN  
**Base Path:** `/api/v1`

---

## 1. API Conventions

- Base path: `/api/v1`
- Request and response formats: JSON unless the endpoint accepts multipart audio.
- Session identifiers connect consecutive conversation turns.
- Text and voice requests enter the same conversation workflow.
- Both input methods return the same standard response structure.
- All timestamps use ISO 8601 format.
- Errors follow one consistent error schema.
- Eligibility results are indicative, not official approvals.

---

## 2. Endpoint Summary

| Endpoint | Method | Input | Output | Error cases | Owner |
|---|---|---|---|---|---|
| `/api/v1/sessions` | POST | `language`, `mode` | `session_id`, `status`, session metadata | 422 invalid input, 500 creation failure | Ankush |
| `/api/v1/sessions/{session_id}` | GET | Session ID in path | Session details and conversation turns | 404 session missing, 500 database failure | Ankush |
| `/api/v1/turns` | POST | `session_id`, `text` | Standard turn response | 400 empty input, 404 session missing, 503 AI/retrieval unavailable | Ankush |
| `/api/v1/voice/turns` | POST | Multipart `session_id`, `audio`, optional `language` | Standard turn response plus transcription | 400 invalid audio, 413 payload too large, 503 STT unavailable | Ankush |

---

## 3. Endpoints

### 3.1 Create session

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

---

### 3.2 Retrieve session

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

---

### 3.3 Submit text turn

**Endpoint:** `POST /api/v1/turns`

Request:

```json
{
  "session_id": "sess_demo_001",
  "text": "क्या मैं प्रधानमंत्री उज्ज्वला योजना के लिए पात्र हूं?"
}
```

Success (Awaiting Information) — HTTP 200:

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

---

### 3.4 Submit voice turn

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

*Audio transport note: DEMO_AUDIO_DATA is illustrative placeholder data. Implementation must agree on actual Base64 audio delivery or an audio URL before enabling production playback.*

---

### 3.5 Standard final assessment response

This is the agreed response structure for a completed eligibility assessment (HTTP 200).

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

---

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

### 4.6 Standard error envelope

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
