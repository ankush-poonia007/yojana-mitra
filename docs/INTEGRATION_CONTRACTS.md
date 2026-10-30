# Yojana Mitra — Integration Contracts (Phase 5 working register)

**Contract status:** Boundary register only. Frozen contracts remain authoritative; this file does not amend or reproduce missing schemas. **OPEN** means the exact contract detail must be retrieved from the reviewed artifact or agreed by owners before implementation.

## Authority

Use frozen Phase 3.3 for external API endpoints, payloads, response/error shapes and `speech.audio_base64`; use the reviewed H1–H4 artifacts for internal handshakes. `DECISIONS.md` records that H1–H4 were user-confirmed as reviewed but that detailed artifacts and schemas were not independently available in this project copy. Do not infer field names from this register. Any proposed change requires explicit amendment approval.

## H1 — Frontend ↔ API

- **Provider / caller:** FastAPI backend / React + TypeScript frontend.
- **Known endpoints from Phase 4.2 brief:** `POST /api/v1/sessions`, `GET /api/v1/sessions/{session_id}`, `POST /api/v1/turns`, `POST /api/v1/voice/turns`.
- **Exact request/response/error schemas and examples:** **OPEN — retrieve frozen Phase 3.3/API contract and reviewed H1 artifact.** Do not recreate them from endpoint names or Master Brief summary.
- **Ownership:** Ankush backend; Aditya client; coordinate shared mock and changes.
- **Mock/real:** Mock may unblock client development, but must be labeled sample and must not be represented as a real eligibility result. Exact mock mode and fixture path **OPEN**.
- **Acceptance:** Endpoint, standard response and error shapes match the frozen API artifact; client displays source and indicative disclaimer; voice failure leaves typed input available. Actual tests pending.

## H2 — API ↔ LangGraph

- **Provider / caller:** workflow graph / API layer invokes graph (direction details to verify against H2 artifact).
- **Boundary:** API-to-workflow orchestration.
- **Exact invoke function, graph input/output/shared state, node names, routing, exceptions and examples:** **OPEN — retrieve reviewed H2 contract.**
- **Ownership:** Ankush.
- **Mock/real behavior:** **OPEN**; mark each integration run MOCKED or REAL in evidence log.
- **Acceptance:** Actual API-to-graph exchange matches reviewed H2 contract and frozen external API; no schema inferred here.

## H3 — LangGraph ↔ Eligibility Engine

- **Provider / caller:** deterministic PMUY eligibility module / graph workflow (call direction to confirm against reviewed H3 artifact).
- **Boundary:** PMUY interview answers to deterministic assessment.
- **Exact function names, argument representation, return schema, error/unknown semantics and examples:** **OPEN — retrieve reviewed H3 contract.**
- **Ownership:** Anamika owns eligibility implementation/handoff; Ankush owns graph integration.
- **Frozen behavior:** PMUY only for full eligibility; R01–R06, D01–D12; evaluate D13 once via R03; R07 remains readiness/verification; unknown, unclear, contradictory or missing input must not be treated as “No” or pass; apply D3 R05 outcomes. The PMUY Knowledge Base is the source for exact rule values and wording.
- **Mock/real behavior:** Mock outputs must be visibly labeled and not scored as real. Exact fixture/signature **OPEN**.
- **Acceptance:** Run the frozen T01–T12 cases after obtaining their exact definitions; record each actual result. No result asserted here.

## H4 — LangGraph ↔ Retrieval

- **Provider / caller:** official-source retrieval module / graph workflow (call direction to confirm against reviewed H4 artifact).
- **Boundary:** Retrieval request and source evidence metadata.
- **Exact function name, request/response schema, tables/DDL, ranking behavior, empty/error behavior and examples:** **OPEN — retrieve reviewed H4 contract and approved schema artifact.**
- **Ownership:** Anamika owns data and agreed ingestion/data handoffs; Ankush owns retrieval integration and backend database wiring.
- **Frozen behavior:** official sources only; preserve source ID, page/section, version and retrieval date; refuse unsupported claims. Do not invent source content or metadata.
- **Mock/real behavior:** Separate sample/mock evidence from real validated retrieval. Exact switch and fixture **OPEN**.
- **Acceptance:** Source provenance appears in the user-facing result according to frozen API contract; unavailable evidence does not produce an invented factual answer. Actual checks pending.

## Additional handoffs and OPEN items

| Handoff | Owner boundary | Exact contract status |
| --- | --- | --- |
| Persistence operations (create/get session, add turn, save assessment) | Ankush: database wiring; Anamika: agreed data/eligibility handoff | Function names, fields, transaction/error semantics, schema and retention behavior **OPEN** |
| Speech transcription and synthesis | Anamika: wrappers/benchmark; Ankush: workflow wiring; Aditya: client use | Function names, provider, audio formats, timeouts, retry and response schemas **OPEN**; preserve frozen API response |
| Official-source ingestion | Anamika: source/data artifacts; Ankush: database wiring/retrieval integration | Input document format, chunk schema, embedding fields and repeatability/error behavior **OPEN** |

## Contract sign-off checklist

For each OPEN item, attach/link the authoritative artifact; record exact caller/callee, function/endpoint, schemas, success/failure examples, mock/real behavior, owner and version; verify against Phase 3.3 and frozen decisions; obtain the responsible owners' agreement. A clarification may fill an OPEN implementation detail only when it does not change a frozen boundary. A boundary change requires an explicit amendment.
