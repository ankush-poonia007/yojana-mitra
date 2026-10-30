---
document_id: YOJANA-MITRA-PMUY-RAG-001
title: PMUY 2.0 Eligibility and Application Knowledge Base
project: Yojana Mitra
document_type: RAG knowledge source
language: English
research_retrieval_date: 2026-10-30
scheme: Pradhan Mantri Ujjwala Yojana (PMUY) 2.0
status: Frozen project research baseline
version: 1.0
---

# PMUY 2.0 — RAG Knowledge Base

## 0. Retrieval and use instructions

This document contains the frozen PMUY research baseline for Yojana Mitra.

**Intended use:** Retrieval-augmented generation (RAG) for scheme information, preliminary eligibility interviews, document guidance, and application guidance.

**Important distinction:**
- Official-source facts are identified as **OFFICIAL SOURCE FACT**.
- Internal product logic is identified as **YOJANA MITRA PROJECT RULE**.
- Interpretations and operational recommendations are identified as **PROJECT INTERPRETATION**.
- Unverified or incomplete information is identified as **OPEN VERIFICATION**.

The assistant must not present a preliminary self-assessment as an official approval. Final application verification and connection release are handled by the authorised LPG distributor/OMC process.

### Core response policy

1. Answer PMUY questions using the official sources listed in this document.
2. When a rule is unclear, the source is missing, or the user does not know an answer, say that the information cannot be determined yet.
3. Do not invent income limits, eligibility categories, exemptions, documents, or application steps.
4. Do not infer that a user is ineligible from a missing document alone. Eligibility and application readiness are separate.
5. Keep each answer tied to the relevant rule ID and source ID.
6. Explain that the assessment is indicative and subject to official verification.
7. Do not request Aadhaar numbers, bank account numbers, or other sensitive identifiers in spoken conversation.

---

## 1. Scheme identity

**FACT-PMUY-001 — Official scheme name**

Pradhan Mantri Ujjwala Yojana (PMUY), including the Ujjwala 2.0 new-connection application process.

**FACT-PMUY-002 — Scheme purpose**

PMUY provides deposit-free LPG connections to eligible adult women from poor households, subject to the applicable scheme conditions and verification process.

**PROJECT-PMUY-001 — Product scope**

Yojana Mitra supports preliminary PMUY 2.0 information and eligibility assessment. It does not submit an application, authenticate identity, approve a connection, or replace distributor verification.

---

## 2. Official source register

The following official sources were identified during research on 2026-10-30. The retrieval date is not necessarily the publication or revision date of each source.

### PMUY-S01 — New Ujjwala 2.0 connection page

- URL: https://www.pmuy.gov.in/ujjwala2.html
- Source type: Official PMUY portal page.
- Use for: Primary eligibility conditions, new-connection documents, application guidance.
- Priority: Critical.

### PMUY-S02 — PMUY official FAQs

- URL: https://www.pmuy.gov.in/faq.html
- Source type: Official PMUY portal FAQ.
- Use for: Household definition clarifications, application routes, document and verification guidance, family-split cases.
- Priority: Critical.

### PMUY-S03 — Deprivation Declaration for Poor Households

- URL: https://www.pmuy.gov.in/documents/Deprivation_Declaration_for_Poor_Households_English.pdf
- Source type: Official PMUY-hosted PDF.
- Use for: The 13 listed deprivation/exclusion criteria and applicant undertaking.
- Priority: Critical.
- OPEN VERIFICATION: The PDF does not visibly state a publication date or revision number in the reviewed copy. The research baseline records that it was linked from the official PMUY site on 2026-10-30. Confirm with an LPG distributor/OMC that no newer declaration is in use before treating its thresholds as permanently current.

### PMUY-S04 — PMUY KYC application, Version 8.0

- URL: https://pmuy.gov.in/documents/Ujjwala-KYC_englishnew.pdf
- Source type: Official PMUY-hosted KYC form.
- Use for: Applicant undertakings, household definition, PNG restriction, application fields and declarations.
- Priority: Critical.
- Version identified in the form: Version 8.0.

### PMUY-S05 — Migrant self-declaration / Annexure I

- URL: https://pmuy.gov.in/documents/Ujjwala-KYC_englishnew.pdf
- Source type: Annexure referenced in the KYC/application materials.
- Use for: Migrant applicants' self-declaration route for relevant address/family-composition information.
- Priority: Supporting.
- Note: Use the current official application pack and distributor instructions to confirm the applicable annexure and accepted evidence.

### Source hierarchy

For the frozen v1 rule set, use:
1. PMUY-S01 for the current top-level new-connection eligibility summary.
2. PMUY-S02 for official FAQ clarifications.
3. PMUY-S03 for the detailed deprivation declaration.
4. PMUY-S04 for KYC undertakings, household definition and PNG restriction.
5. PMUY-S05 for applicable migrant declarations.

An older PMUY “About” page was found to list beneficiary categories such as SC, ST, MBC, AAY, forest dwellers and SECC households. The current FAQ states that these are not separate categories under the current scheme, while the KYC form contains a caste-category field. Therefore, Yojana Mitra must not use caste, SC/ST status, AAY status or PMAY-G status as independent eligibility gates in this PMUY 2.0 assessment. Refer to the current application page, FAQ and KYC form rather than the older category description.

---

## 3. Household definition

**FACT-PMUY-HH-001 — Household definition from KYC Version 8.0**

The KYC form describes the household as a family consisting of members reflected in the family-composition document, living together in a dwelling unit with a common kitchen.

**YOJANA MITRA PROJECT RULE**

When asking about household LPG connections or deprivation criteria:
- Explain that the user should consider the household as defined in the official KYC material.
- Do not casually include extended-family members who live elsewhere or do not share the relevant household/dwelling unit.
- Where the family-composition document is unclear or household membership is disputed, return “Cannot determine yet” or “Verification required” rather than guessing.

---

## 4. Primary eligibility conditions

The current Ujjwala 2.0 new-connection page and official FAQ identify the following top-level conditions.

### PMUY-R01 — Applicant is a woman

- Type: Mandatory applicant condition.
- OFFICIAL SOURCE FACT: Applicant must be a woman.
- User information: Applicant's gender.
- Evaluation: Must satisfy the stated condition.
- Source: PMUY-S01, PMUY-S02.

### PMUY-R02 — Applicant is at least 18 years old

- Type: Mandatory applicant condition.
- OFFICIAL SOURCE FACT: Applicant must have attained 18 years of age.
- User information: Date of birth or age.
- Evaluation: Applicant must be 18 or older.
- Source: PMUY-S01, PMUY-S02.

### PMUY-R03 — No other LPG connection in the household

- Type: Household exclusion.
- OFFICIAL SOURCE FACT: The household must not already have an LPG connection from an Oil Marketing Company (OMC).
- User information: Whether a member of the defined household already has an LPG connection.
- Evaluation: Existing household LPG connection indicates an exclusion.
- Source: PMUY-S01, PMUY-S02, PMUY-S03, PMUY-S04.
- Duplicate handling: PMUY-D13 expresses the existing-LPG exclusion in the deprivation declaration. Ask/evaluate this condition once; do not count it twice.

### PMUY-R04 — Poor-household deprivation declaration

- Type: Mandatory declaration/household condition.
- OFFICIAL SOURCE FACT: Applicant must belong to a poor household and provide the prescribed deprivation declaration.
- User information: Responses to the applicable declaration criteria and ability to provide the prescribed undertaking.
- Evaluation: The declaration criteria must be checked. A listed exclusion condition indicated by a YES answer prevents a clean pass in the preliminary assessment.
- Source: PMUY-S01, PMUY-S02, PMUY-S03.

### PMUY-R05 — Indian citizenship and residence

- Type: KYC applicant undertaking.
- OFFICIAL SOURCE FACT: The reviewed KYC Version 8.0 contains an undertaking concerning Indian citizenship and residence in India.
- User information: Whether applicant satisfies the undertaking.
- Evaluation: If the applicant does not satisfy it, do not mark the KYC conditions as passed; explain that the application undertaking is not met and official confirmation may be needed.
- Source: PMUY-S04.

### PMUY-R06 — Domestic PNG restriction

- Type: KYC/connection restriction.
- OFFICIAL SOURCE FACT: The reviewed KYC Version 8.0 states that a household with a domestic Piped Natural Gas (PNG) connection in the dwelling unit is not entitled to subsidised LPG.
- User information: Whether the current dwelling unit has a domestic PNG connection.
- Evaluation: YES indicates the stated restriction applies; explain the subsidised-LPG limitation. Do not merge this with the LPG-connection question.
- Source: PMUY-S04.
- Important wording: This is specifically about domestic PNG in the dwelling unit and subsidised LPG. Preserve that scope.

### PMUY-R07 — Required declarations and verification

- Type: Application/verification requirement.
- OFFICIAL SOURCE FACT: The application process requires declarations, KYC and verification.
- User information: Whether applicant can complete the required application and verification steps.
- Evaluation: This is an application-readiness/verification state, not by itself an eligibility rejection.
- Source: PMUY-S02, PMUY-S04.

---

## 5. Deprivation Declaration — 13 listed criteria

The official PMUY-hosted Deprivation Declaration lists 13 criteria. The criteria below are summarized for conversational use; the official PDF wording remains authoritative.

**Interpretation rule:** A YES answer to one of D01–D12 indicates that the corresponding listed exclusion criterion may apply. D13 is the existing-LPG criterion and overlaps with R03. A YES must not be counted twice.

### PMUY-D01 — Monthly earnings above ₹10,000

- Official criterion: Any household member earns more than ₹10,000 per month.
- Question: “Does any member of your defined household earn more than ₹10,000 in a month?”
- YES: Listed exclusion indicated.
- NO: This criterion is not indicated by the answer.
- UNKNOWN: Cannot determine yet.
- Important: This is more than ₹10,000 for any household member, not total combined household income.
- Source: PMUY-S03.

### PMUY-D02 — Professional tax

- Official criterion: Household member pays professional tax.
- Question: “Does any member of your household pay professional tax?”
- YES: Listed exclusion indicated.
- Source: PMUY-S03.

### PMUY-D03 — Income tax

- Official criterion: Household member pays income tax.
- Question: “Does any member of your household pay income tax?”
- YES: Listed exclusion indicated.
- Source: PMUY-S03.

### PMUY-D04 — Government employee

- Official criterion: Household member is a government employee.
- Question: “Is any member of your household a government employee?”
- YES: Listed exclusion indicated.
- Source: PMUY-S03.

### PMUY-D05 — Registered non-agricultural enterprise

- Official criterion: Household has a non-agricultural enterprise registered with the government.
- Question: “Does your household have a non-agricultural enterprise registered with the government?”
- YES: Listed exclusion indicated.
- Source: PMUY-S03.

### PMUY-D06 — Kisan Credit Card above ₹50,000

- Official criterion: Household member possesses a Kisan Credit Card with a credit limit above ₹50,000.
- Question: “Does any member of your household have a Kisan Credit Card with a credit limit above ₹50,000?”
- YES: Listed exclusion indicated.
- UNKNOWN: Ask user to check the credit limit or mark verification required.
- Source: PMUY-S03.

### PMUY-D07 — More than 2.5 acres irrigated land with one irrigation equipment

- Official criterion: Household owns more than 2.5 acres of irrigated land with one irrigation equipment.
- Question: “Does your household own more than 2.5 acres of irrigated land with one irrigation equipment?”
- YES: Listed exclusion indicated.
- Source: PMUY-S03.
- Conversational caution: Explain “irrigated land” and “irrigation equipment” in plain language. Do not substitute a different land threshold.

### PMUY-D08 — At least 5 acres irrigated land for two or more crop seasons

- Official criterion: Household owns 5 acres or more of irrigated land for two or more crop seasons.
- Question: “Does your household own at least 5 acres of irrigated land used for two or more crop seasons?”
- YES: Listed exclusion indicated.
- Source: PMUY-S03.

### PMUY-D09 — At least 7.5 acres land with irrigation equipment

- Official criterion: Household owns at least 7.5 acres of land with at least one irrigation equipment.
- Question: “Does your household own at least 7.5 acres of land with at least one irrigation equipment?”
- YES: Listed exclusion indicated.
- Source: PMUY-S03.
- Conversational caution: Preserve the official threshold and irrigation-equipment condition exactly.

### PMUY-D10 — House above 30 square metres

- Official criterion: Household owns a house with more than 30 square metres carpet area, except a house received through a government scheme.
- Question: “Does your household own a house with more than 30 square metres of carpet area that was not received through a government scheme?”
- YES: Listed exclusion indicated.
- NO: This criterion is not indicated by the answer.
- Important exception: A house received through a government scheme is excepted from this particular criterion.
- Source: PMUY-S03.

### PMUY-D11 — Motorized vehicle or fishing boat

- Official criterion: Household owns a motorized three-/four-wheeler or fishing boat.
- Question: “Does any member of your household own a motorized three-wheeler, four-wheeler or fishing boat?”
- YES: Listed exclusion indicated.
- Source: PMUY-S03.

### PMUY-D12 — Mechanized agricultural equipment

- Official criterion: Household owns mechanized three-/four-wheeler agricultural equipment.
- Question: “Does any member of your household own mechanized three-wheeler or four-wheeler agricultural equipment?”
- YES: Listed exclusion indicated.
- Source: PMUY-S03.

### PMUY-D13 — Existing LPG connection

- Official criterion: Household has an existing LPG connection.
- Question: “Does any member of your defined household already have an LPG connection?”
- YES: Existing LPG exclusion indicated.
- Source: PMUY-S03.
- Duplicate handling: This overlaps with PMUY-R03. Evaluate once.

---

## 6. Documents required for application

The official PMUY page and FAQ provide the document requirements below. The precise applicable document may depend on the applicant's circumstances and current distributor instructions.

### PMUY-DOC-01 — KYC application form

- Requirement: Required.
- Purpose: Applicant and application details.
- Source: PMUY-S01, PMUY-S04.

### PMUY-DOC-02 — Applicant Aadhaar

- Requirement: Required.
- Purpose: Identity/KYC.
- Source: PMUY-S01, PMUY-S02, PMUY-S04.

### PMUY-DOC-03 — Address proof

- Requirement: Conditional when current address differs from Aadhaar.
- Source: PMUY-S01, PMUY-S02.

### PMUY-DOC-04 — Ration card or accepted government family-composition document

- Requirement: Required.
- Purpose: Establish household/family composition.
- Source: PMUY-S01, PMUY-S02, PMUY-S04.

### PMUY-DOC-05 — Aadhaar of adult family members listed in family-composition document

- Requirement: Required as stated in the application material.
- Source: PMUY-S01, PMUY-S02.

### PMUY-DOC-06 — Bank passbook, bank statement or cancelled cheque

- Requirement: Required bank details/documentation.
- Purpose: Bank account details for the application.
- Source: PMUY-S01, PMUY-S02.

### PMUY-DOC-07 — Deprivation Declaration

- Requirement: Required.
- Purpose: Applicant's prescribed household declaration.
- Source: PMUY-S01, PMUY-S03.

### PMUY-DOC-08 — Migrant self-declaration / Annexure I

- Requirement: Conditional for applicable migrant applicants.
- Purpose: Applicable address and family-composition declaration route.
- Source: PMUY-S02, PMUY-S04, PMUY-S05.
- OPEN VERIFICATION: Confirm the exact currently accepted migrant evidence and annexure with the current application pack/distributor.

**Important product rule:** A missing document can mean “application readiness incomplete.” It does not automatically mean “not eligible.”

---

## 7. Application and official verification

### PMUY-APP-01 — Application routes

The official FAQ describes:
- Online application through the PMUY portal.
- Assistance through a Common Service Centre (CSC).
- Offline application at an LPG distributor.

Source: PMUY-S02.

### PMUY-APP-02 — CSC charge

The reviewed official FAQ states that online self-submission has no fee and CSC-assisted submission carries a ₹20 charge.

Source: PMUY-S02.

### PMUY-VER-01 — Aadhaar biometric authentication

- OFFICIAL SOURCE FACT: Aadhaar biometric authentication/e-KYC is required and is carried out through the LPG distributor process.
- Product response: Explain that the user must complete the official authentication step.
- Source: PMUY-S02.

### PMUY-VER-02 — Document verification

- OFFICIAL SOURCE FACT: Distributor verifies submitted documents against originals as part of the application process.
- Product response: Show “Distributor verification required.”
- Source: PMUY-S02.

### PMUY-VER-03 — Pre-installation inspection

- OFFICIAL SOURCE FACT: Pre-installation inspection at the applicant's premises is required before connection release.
- Product response: Explain that a connection is not approved merely because the chatbot assessment passes.
- Source: PMUY-S02.

### PMUY-VER-04 — Family split / prior LPG linkage

- OFFICIAL SOURCE FACT: The FAQ describes a process for cases where family members have separated but remain linked to an earlier household LPG connection. The applicant may need to contact the concerned distributor/OMC to resolve the linked records before applying with updated family-composition evidence.
- Product response: Do not automatically reject or approve. Set “Verification required — contact distributor/OMC to resolve household linkage.”
- Source: PMUY-S02.

---

## 8. Eligibility decision logic

### Separate the result dimensions

**YOJANA MITRA PROJECT RULE — Eligibility result**

Allowed values:
- `LIKELY_ELIGIBLE`
- `LIKELY_NOT_ELIGIBLE`
- `CANNOT_DETERMINE`

**YOJANA MITRA PROJECT RULE — Verification status**

Allowed values:
- `REQUIRED`
- `PENDING`
- `NOT_STARTED`
- `NOT_APPLICABLE`

**YOJANA MITRA PROJECT RULE — Application readiness**

Allowed values:
- `READY_TO_PREPARE`
- `DOCUMENTS_INCOMPLETE`
- `NEEDS_DISTRIBUTOR_GUIDANCE`
- `UNKNOWN`

Do not combine these into one score or one Boolean.

### Decision table

| Condition | Eligibility result | Verification/application status |
|---|---|---|
| Applicant is not a woman | LIKELY_NOT_ELIGIBLE | Applicant condition not met |
| Applicant is under 18 | LIKELY_NOT_ELIGIBLE | Applicant condition not met |
| Applicant does not satisfy the citizenship/residence undertaking | LIKELY_NOT_ELIGIBLE or CANNOT_DETERMINE pending clarification | Official confirmation may be needed |
| Existing LPG connection in defined household | LIKELY_NOT_ELIGIBLE | Existing-connection exclusion |
| Domestic PNG connection in dwelling unit | LIKELY_NOT_ELIGIBLE for subsidised LPG under reviewed KYC undertaking | Distributor/OMC confirmation |
| Any D01–D12 is YES | LIKELY_NOT_ELIGIBLE | Listed deprivation exclusion indicated |
| Any required answer is unknown | CANNOT_DETERMINE | Ask follow-up or mark verification required |
| Answers contradict one another | CANNOT_DETERMINE | Clarification required |
| All applicable self-reported conditions pass | LIKELY_ELIGIBLE | Official distributor verification still required |
| Eligibility appears satisfied but documents are missing | Eligibility can remain LIKELY_ELIGIBLE | DOCUMENTS_INCOMPLETE |
| Biometric authentication, document verification or inspection pending | Eligibility result remains separate | Verification PENDING |

### Evaluation order

1. Confirm the user is asking about a new PMUY connection.
2. Collect applicant conditions: woman, age, citizenship/residence undertaking.
3. Establish the household using the KYC household definition.
4. Check existing LPG connection.
5. Check domestic PNG restriction separately.
6. Ask the 12 deprivation questions D01–D12.
7. If any exclusion is indicated, return likely not eligible with the exact rule ID and explanation.
8. If required information is unknown or contradictory, return cannot determine yet.
9. If all self-reported conditions appear satisfied, return likely eligible.
10. Separately show document readiness and official verification requirements.

**No LLM override:** The LLM may explain a result, but it must not override deterministic rule evaluation.

**No silent defaults:** Unknown must never be treated as No. Missing data must never be interpreted as a passing condition.

---

## 9. Interview question bank

### Stage 1 — Applicant

1. Are you applying for the LPG connection in your own name?
2. Are you a woman?
3. Have you completed 18 years of age?
4. Are you an Indian citizen currently residing in India?

Evaluate: PMUY-R01, R02, R05.

### Stage 2 — Household and connections

Explain the KYC household definition before asking.

5. Does anyone in your defined household already have an LPG connection?
6. Does your current dwelling unit have a domestic Piped Natural Gas (PNG) connection?

Evaluate: PMUY-R03, R06 and D13. Do not count D13 twice.

### Stage 3 — Deprivation declaration

Explain that the next questions come from the official PMUY declaration. Ask D01–D12 one at a time.

For each question, support:
- Yes
- No
- Not sure

### Stage 4 — Application readiness

7. Do you have a ration card or another accepted government family-composition document?
8. Does your current address match the address on your Aadhaar?
9. Are Aadhaar details available for the adult family members listed in the family-composition document?
10. Do you have the required bank account document?
11. Are you applying as a migrant?

These questions are for document/application readiness. They are not all independent eligibility conditions.

---

## 10. Edge-case handling

### PMUY-EDGE-01 — Applicant is under 18

Return likely not eligible for that applicant because the applicant must be at least 18.

### PMUY-EDGE-02 — Applicant is male

Return likely not eligible because the applicant condition specifies a woman.

### PMUY-EDGE-03 — Existing LPG connection in household

Return likely not eligible based on the household LPG exclusion. If the family has split and the connection linkage is outdated, explain the distributor/OMC record-resolution route rather than making assumptions.

### PMUY-EDGE-04 — Applicant does not know whether a household member has LPG

Return cannot determine yet or verification required. Do not assume No.

### PMUY-EDGE-05 — Applicant has no ration card

Do not immediately reject. Ask whether the applicant has another accepted government-issued family-composition document. If uncertain, direct the applicant to the official distributor/OMC for confirmation.

### PMUY-EDGE-06 — Migrant applicant

Explain the migrant self-declaration route and show the relevant official form. Confirm current accepted documents with the distributor.

### PMUY-EDGE-07 — Missing bank document

Keep eligibility result separate. Mark application readiness as documents incomplete.

### PMUY-EDGE-08 — Domestic PNG

Explain the separate PNG restriction in the reviewed KYC undertaking. Do not treat PNG as the same question as LPG.

### PMUY-EDGE-09 — Unclear land or asset details

Ask a clarification using the exact threshold and wording. If the user still does not know, mark unknown/verification required.

### PMUY-EDGE-10 — Contradictory household information

Ask the user to clarify. Do not select whichever answer is more favourable.

---

## 11. Evaluation test cases

These are designed test cases, not measured results.

| Test ID | Input situation | Expected outcome |
|---|---|---|
| PMUY-T01 | Adult woman, Indian resident, all deprivation answers No, no LPG or PNG | LIKELY_ELIGIBLE + verification required |
| PMUY-T02 | Applicant is 17 | LIKELY_NOT_ELIGIBLE |
| PMUY-T03 | Applicant is male | LIKELY_NOT_ELIGIBLE |
| PMUY-T04 | Existing LPG connection in defined household | LIKELY_NOT_ELIGIBLE |
| PMUY-T05 | Household has domestic PNG | LIKELY_NOT_ELIGIBLE for subsidised LPG under reviewed KYC undertaking |
| PMUY-T06 | Household member earns ₹12,000/month | LIKELY_NOT_ELIGIBLE under D01 |
| PMUY-T07 | Household member pays income tax | LIKELY_NOT_ELIGIBLE under D03 |
| PMUY-T08 | House is above 30 m² but was received under a government scheme | D10 not triggered by that house; evaluate remaining rules |
| PMUY-T09 | Applicant does not know KCC credit limit | CANNOT_DETERMINE or verification required |
| PMUY-T10 | Applicant has another accepted government family-composition document | Continue assessment; do not reject solely for no ration card |
| PMUY-T11 | Family has split but members remain linked to old LPG connection | Distributor/OMC record resolution required |
| PMUY-T12 | Conditions appear satisfied but biometric authentication is pending | LIKELY_ELIGIBLE + verification pending |

---

## 12. Language and response policy

**YOJANA MITRA PROJECT DECISION**

- Supported languages for v1: Hindi and English.
- User manually selects the response language.
- Voice input: provide written response and spoken response.
- Text input: provide written response with an optional Listen button.
- Use the same grounded answer and eligibility result for both modalities.
- Do not run separate eligibility logic for voice and text.
- Explain technical terms in simple Hindi/English without changing official thresholds or conditions.

### Response structure

1. Eligibility result.
2. Short explanation.
3. Conditions satisfied.
4. Exclusion conditions found, if any.
5. Missing/uncertain information.
6. Documents required.
7. Application route.
8. Official verification notice.
9. Source references.

---

## 13. Privacy and safety rules

1. Do not ask users to speak Aadhaar numbers or bank account numbers into the assistant.
2. Do not claim that Yojana Mitra submits an application.
3. Do not claim that the assistant approves a connection.
4. Do not describe a preliminary result as an official government decision.
5. Do not invent or estimate a missing eligibility threshold.
6. Do not treat missing documents as automatic ineligibility.
7. Do not store unnecessary sensitive personal information in RAG logs or evaluation datasets.
8. Direct unresolved record, identity, household-linkage and document questions to the authorised distributor/OMC process.

---

## 14. Versioning and unresolved verification

**Current project baseline:** PMUY research captured 2026-10-30.

**Known limitation:** The reviewed Deprivation Declaration PDF does not visibly state its publication date or revision number.

**Required maintenance action:** Before a public deployment and whenever the official PMUY page or application documents change:
1. Re-open PMUY-S01 through PMUY-S04.
2. Compare the new declaration against D01–D13.
3. Check whether the KYC version changed.
4. Update rule IDs or rule versions where necessary.
5. Re-run the PMUY test cases.
6. Record the retrieval date and source changes.

**Do not assume that thresholds are permanent.**

---

## 15. Frozen project decisions

1. PMUY is the reference scheme for the first complete Yojana Mitra eligibility flow.
2. Use the current Ujjwala 2.0 top-level eligibility conditions and the reviewed official deprivation declaration.
3. Include the KYC Version 8.0 citizenship/residence and domestic PNG undertakings in the assessment design.
4. Use the KYC household definition.
5. Evaluate D13 only once because it overlaps with the existing-LPG condition.
6. Keep eligibility, verification and application readiness separate.
7. Use deterministic rule evaluation; use the LLM for conversation and explanation, not for overriding eligibility rules.
8. Support Hindi and English with manual language selection.
9. Voice input receives spoken and written output; text input receives written output with optional voice playback.
10. PMUY is the reference scheme only. PM-KISAN and PM-JAY 70+ require separate official-source extraction and validation.

**Status:** Frozen PMUY research baseline for project design. The declaration revision-date limitation remains explicitly open for operational verification.
