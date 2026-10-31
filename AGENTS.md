# AGENTS.md — Repository Governance & Development Rules
# Yojana Mitra (TRIVON)

**Working Name:** Yojana Mitra  
**Product Concept:** AI-powered, voice- and text-enabled rural government scheme navigation assistant (Hindi and English).  
**Status:** Architectural and implementation governance for all Antigravity and automated agents.

---

## 1. Documentation Authority Hierarchy

All agent actions, implementations, and planning must strictly respect this four-level authority order. Do not silently resolve conflicts; report any discrepancies.

1. **Level 1 — Project Rules, Decisions, and Ownership:**
   - `AGENTS.md` (this governance file)
   - `docs/DECISIONS.md` (frozen Phase 4.1 decisions D1–D14; authoritative and frozen)
   - `docs/PHASE_4.2_PERSONAL_BRIEFS.md` (team ownership and boundaries; status: **DOCUMENTED — REVIEW PENDING; NOT FROZEN**. Provides useful operational guidance on team working boundaries, but does not independently override frozen Level 1 decisions).

2. **Level 2 — Product, UX, and Architecture Baseline:**
   - `docs/YOJANA_MITRA_MASTER_BRIEF.md`
   - `docs/ui_userflow.md`
   - `docs/YOJANA_MITRA_PHASE_3_2_TECH_STACK.md`
   - `docs/YOJANA_MITRA_PHASE_3_3_API_CONTRACT_AND_STRUCTURE.md`

3. **Level 3 — Phase 5 Planning and Integration:**
   - `docs/PHASE_5_IMPLEMENTATION_PLAN.md`
   - `docs/FEATURE_BOARD.md`
   - `docs/INTEGRATION_CONTRACTS.md`
   - `docs/TEST_ACCEPTANCE_MATRIX.md`
   - `docs/BUILD_EVIDENCE_LOG.md`
   - `docs/ANKUSH_PHASE_5_DETAILED_ROADMAP.md`

4. **Level 4 — Role-Specific Instructions:**
   - `docs/ANTIGRAVITY_ANKUSH_BUILD_GUIDE.md` & `docs/ANTIGRAVITY_ANKUSH_PROMPT_SEQUENCE.md`
   - `docs/ANTIGRAVITY_ANAMIKA_BUILD_GUIDE.md` & `docs/ANTIGRAVITY_ANAMIKA_PROMPT_SEQUENCE.md`
   - `docs/ANTIGRAVITY_ADITYA_BUILD_GUIDE.md` & `docs/ANTIGRAVITY_ADITYA_PROMPT_SEQUENCE.md`

---

## 2. Team Ownership & Working Boundaries

Respect assigned boundaries. Never edit, overwrite, rename, or discard another teammate's owned files without an explicit, documented handoff.

- **Ankush (Backend Developer & Integration Lead):**
  - Owns: `backend/` (routes, schemas, core, services, graph orchestration, adapters, backend database wiring), `shared/` (API contract and mock fixtures with Aditya), root configuration (`.env.example`, `env.example`, `requirements.txt`, `AGENTS.md`), and integration documentation in `docs/`.
  - Explicit assignment: Ankush owns backend database wiring and migrations following the Phase 5 implementation plan resolution of the Phase 4.5 prompt fragment conflict. Unresolved technical persistence decisions (database schema/DDL, column types, retention/deletion policy) remain **OPEN** pending formal team agreement.

- **Anamika (Data, Research, Rules & Speech):**
  - Owns: `data/` (documents, extractions, scheme data, evaluation sets), `docs/research/PMUY/` (authoritative research, Knowledge Base, and test definitions), deterministic PMUY eligibility rule engine implementation, STT/TTS benchmark artifacts and wrappers, and agreed integration handoff modules.
  - Research files under `docs/research/PMUY/` are strictly read-only for other agents.

- **Aditya (Frontend & Client Experience):**
  - Owns: `frontend/` (React application, TypeScript types, Vite tooling, Tailwind styling, UI/UX components, client-side API integration, audio playback, client demo materials).

---

## 3. Frozen Architectural & Product Invariants

These decisions are frozen. Agents must not alter or bypass them:

1. **The Four Frozen API Routes:**
   - `POST /api/v1/sessions` (session initialization)
   - `GET /api/v1/sessions/{session_id}` (session retrieval)
   - `POST /api/v1/turns` (text turn interaction)
   - `POST /api/v1/voice/turns` (multipart audio turn interaction)
   - Plus utility health check `GET /health`.

2. **Unified Turn Workflow:** Text and voice turns enter the identical conversation workflow and share session state.
3. **Audio Response Contract:** Preserve `speech.audio_base64` in the agreed response shape.
4. **Shared Error Envelope:** All error responses must adhere strictly to:
   ```json
   {
     "error": {
       "code": "ERROR_CODE",
       "message": "Human-readable description",
       "retryable": false,
       "details": {}
     }
   }
   ```
5. **Deterministic Eligibility Authority:**
   - Pradhan Mantri Ujjwala Yojana (PMUY 2.0) is the ONLY scheme with full eligibility assessment in Phase 5. PM-KISAN and PM-JAY 70+ remain information-only pending validated official sources.
   - Deterministic Python rules (R01–R07, D01–D12, D13 evaluated once via R03) exclusively own eligibility results.
   - Gemini models conduct conversation, phrasing, and explanation; Gemini must NEVER independently decide or override eligibility rules.
   - Eligibility is indicative, not an official government determination.
   - Unknown, unclear, contradictory, or missing inputs must NEVER default to "No" or a passing condition.
   - Application readiness (documents) and official verification remain distinct from eligibility.

6. **Official-Source Retrieval:**
   - Factual answers must be grounded in loaded official source documents with full provenance (source ID, page/section, document version, retrieval date).
   - If evidence is absent or unsupported, the system must return an explicit refusal or request clarification. Never fabricate citations.

7. **Languages:** Hindi and English are v1 languages. User manually selects the response language.

---

## 4. Privacy, Security, and Data Guardrails

1. **Audio Persistence:** Uploaded raw audio must NEVER be persisted to disk, storage buckets, or database tables. Audio bytes are processed in-memory only.
2. **Personal Identifiable Information (PII):** Do not ask for, accept, collect, log, or persist Aadhaar numbers, bank account numbers, or biometric credentials.
3. **Credential Management:** Secrets and API keys must remain strictly server-side. Never commit `.env` or secrets to git. Never expose backend privileged keys (`SUPABASE_SERVICE_ROLE_KEY`, `GEMINI_API_KEY`) to frontend bundles or client-facing responses.

---

## 5. Testing, Verification, and Evidence Rules

1. **Honest Status Reporting:** Use strict status vocabulary: `REAL`, `PARTIAL`, `MOCKED`, `NOT STARTED`, `OPEN`, `BLOCKED`.
2. **Never Claim Without Proof:** Do not mark a feature or test as passed or complete unless actual command execution has been observed and verified in the current environment.
3. **No Invented Interfaces:** If an internal interface, schema, table DDL, or rule is missing, label it `OPEN` and identify the responsible owner. Do not guess or invent placeholder interfaces.
4. **Build Evidence Logging:** All verification runs must be recorded in `docs/BUILD_EVIDENCE_LOG.md` with timestamp, revision, exact command, input, observed result, and outcome.

---

## 6. Git & Environment Safety Rules

1. **Preserve Working Trees:** Never run `git reset --hard`, `git clean -fd`, or discard uncommitted teammate or working files.
2. **Authorized Actions Only:** Do not commit, push, switch branches, or deploy unless explicitly directed by the repository lead (Ankush).
3. **Safe Dependency Management:** Do not install packages, update requirements, or run database migrations without explicit review and approval.
