# Yojana Mitra — PMUY Research and Eligibility Analysis

**Project:** Yojana Mitra — AI-powered government scheme assistance  
**Scheme:** Pradhan Mantri Ujjwala Yojana (PMUY) 2.0  
**Document:** PMUY Research & Analysis Report  
**Research retrieval date:** 30 October 2026  
**Document version:** 1.0  
**Status:** Frozen project research baseline; source-version caveat remains open

---

## 1. Executive summary

This report records the frozen PMUY research pack for Yojana Mitra. PMUY is the reference scheme for designing the platform's first complete eligibility interview and assessment flow.

The research reviewed the official PMUY Ujjwala 2.0 new-connection page, official FAQs, the official Deprivation Declaration PDF, and the PMUY KYC application identified as Version 8.0.

The key findings are:

1. The current Ujjwala 2.0 application flow has three primary eligibility conditions: applicant must be a woman, must be at least 18 years old, and the household must not already have an LPG connection. The applicant must also belong to a poor household under the prescribed deprivation declaration.
2. The official Deprivation Declaration lists 13 criteria. D13 (existing LPG connection) overlaps with the primary household LPG condition and should not be evaluated twice.
3. The reviewed KYC Version 8.0 contains additional undertakings concerning Indian citizenship/residence and domestic PNG connection in the dwelling unit for subsidised LPG.
4. The KYC household definition is important: members reflected in the family-composition document who live together in a dwelling unit with a common kitchen.
5. Eligibility, official verification and document readiness must be represented separately.
6. Yojana Mitra should use deterministic rule evaluation for eligibility. The LLM should conduct the interview and explain the outcome, not independently decide or override the rules.
7. The reviewed Deprivation Declaration PDF does not visibly show a publication date or revision number. Its current applicability should be reconfirmed with a distributor/OMC before operational deployment.

This document records the team's research baseline. It does not constitute legal advice or an official government eligibility determination.

---

## 2. Product context and frozen scope

### 2.1 Product concept

Yojana Mitra is a voice- and text-enabled assistant that helps users understand government schemes, answer scheme-specific questions, receive an indicative eligibility assessment, and prepare the documents and application steps.

### 2.2 Frozen product decisions

| Area | Frozen decision |
|---|---|
| Full eligibility implementation | PM-KISAN, PMUY and PM-JAY 70+ pathway |
| PMUY role | Reference scheme for first complete eligibility flow |
| Official-record dependency | Show “Verification required” when self-reported information cannot establish the answer |
| Languages | Hindi and English |
| Language selection | User manually selects response language |
| Voice input | Written and spoken response |
| Text input | Written response with optional Listen button |
| Eligibility evaluation | Deterministic rule-based assessment |
| LLM role | Scheme identification, conversational question phrasing, answer explanation and grounded guidance; no rule override |

PM-KISAN and PM-JAY 70+ must have separate official-source extraction and rule validation. PMUY criteria must not be copied into those schemes.

---

## 3. Research scope and method

### 3.1 Sources reviewed

| Source ID | Official source | Research use |
|---|---|---|
| PMUY-S01 | https://www.pmuy.gov.in/ujjwala2.html | Current Ujjwala 2.0 eligibility and documents |
| PMUY-S02 | https://www.pmuy.gov.in/faq.html | Household definition, application and verification clarifications |
| PMUY-S03 | https://www.pmuy.gov.in/documents/Deprivation_Declaration_for_Poor_Households_English.pdf | Thirteen deprivation/exclusion criteria |
| PMUY-S04 | https://pmuy.gov.in/documents/Ujjwala-KYC_englishnew.pdf | KYC Version 8.0, household definition, PNG and applicant undertakings |
| PMUY-S05 | https://pmuy.gov.in/documents/Ujjwala-KYC_englishnew.pdf | Migrant self-declaration / Annexure I in application materials |

**Retrieval date:** 30 October 2026. This is the date the research captured the sources, not necessarily the publication date of the documents.

### 3.2 Source hierarchy

The research uses the current Ujjwala 2.0 new-connection page for primary eligibility, the official FAQ for clarifications, the official declaration for the detailed exclusion criteria, and KYC Version 8.0 for the application undertakings.

An older PMUY “About” page was found to list categories such as SC, ST, MBC, AAY, forest dwellers and SECC households. The current FAQ states that there are no such separate categories under the current scheme, while the KYC form contains a caste-category field.

**Research resolution:** Do not use caste, SC/ST status, AAY status or PMAY-G status as independent eligibility gates in the current PMUY 2.0 assessment. Follow the current new-connection page, FAQ, declaration and KYC material.

---

## 4. Findings: primary eligibility conditions

The current Ujjwala 2.0 new-connection page and FAQ identify the primary conditions below.

| Rule ID | Condition | Type | Evidence needed in interview |
|---|---|---|---|
| PMUY-R01 | Applicant must be a woman | Mandatory applicant condition | Applicant's gender |
| PMUY-R02 | Applicant must have attained 18 years | Mandatory applicant condition | Age/date of birth |
| PMUY-R03 | No other LPG connection from any OMC in the same household | Household exclusion | Existing household LPG status |
| PMUY-R04 | Applicant must belong to a poor household and provide the prescribed deprivation declaration | Mandatory household/declaration condition | Answers to declaration criteria and undertaking |

The assessment must preserve the official conditions and must not replace them with a generic “Are you poor?” question.

---

## 5. Findings: KYC Version 8.0 undertakings

The reviewed KYC form contains additional applicant undertakings.

### 5.1 Indian citizenship and residence

The form contains an undertaking concerning Indian citizenship and residence in India. This must be included in the assessment design and clearly identified as a KYC undertaking.

### 5.2 Domestic PNG connection

The form states that a household with a domestic Piped Natural Gas (PNG) connection in the dwelling unit is not entitled to subsidised LPG.

This is separate from the existing LPG connection condition. Yojana Mitra must ask about PNG separately and preserve the wording about the dwelling unit and subsidised LPG.

### 5.3 Household definition

The KYC form describes the household as a family consisting of all members reflected in the family-composition document, living together in a dwelling unit with a common kitchen.

This definition should be explained before asking the user about:
- Existing LPG connections.
- Household members covered by the deprivation declaration.
- Household assets and other listed exclusion conditions.

Do not casually include extended-family members who live elsewhere or do not share the relevant household/dwelling unit. Where the household record is unclear, request clarification or mark verification required.

---

## 6. Findings: all 13 deprivation criteria

The official Deprivation Declaration lists the following criteria. The summaries below are for analysis and conversational design; the PDF wording remains authoritative.

| Rule ID | Official criterion, summarized | User information |
|---|---|---|
| PMUY-D01 | Any household member earns more than ₹10,000 per month | Whether any member earns above the threshold |
| PMUY-D02 | Household member pays professional tax | Professional-tax status |
| PMUY-D03 | Household member pays income tax | Income-tax status |
| PMUY-D04 | Household member is a government employee | Government employment status |
| PMUY-D05 | Household has a government-registered non-agricultural enterprise | Enterprise registration status |
| PMUY-D06 | Household member possesses a Kisan Credit Card with credit limit above ₹50,000 | KCC ownership and limit |
| PMUY-D07 | Household owns more than 2.5 acres of irrigated land with one irrigation equipment | Irrigated land area and equipment |
| PMUY-D08 | Household owns 5 acres or more of irrigated land for two or more crop seasons | Land area and crop seasons |
| PMUY-D09 | Household owns at least 7.5 acres of land with at least one irrigation equipment | Land area and equipment |
| PMUY-D10 | Household owns a house above 30 square metres carpet area, except one received through a government scheme | House area and acquisition route |
| PMUY-D11 | Household owns a motorized three-/four-wheeler or fishing boat | Vehicle/boat ownership |
| PMUY-D12 | Household owns mechanized three-/four-wheeler agricultural equipment | Agricultural equipment ownership |
| PMUY-D13 | Household has an existing LPG connection | Existing LPG connection |

### 6.1 Interpretation

- YES to D01–D12 indicates that a listed exclusion criterion may apply.
- D13 overlaps with the primary existing-LPG rule PMUY-R03. Evaluate once, not twice.
- D01 refers to any household member earning more than ₹10,000 per month, not combined household income.
- D10 has an exception for a house received through a government scheme.
- The declaration is an applicant undertaking. The assistant must not represent its self-reported evaluation as official verification.

### 6.2 Language and comprehension risk

Some criteria contain technical terms:
- Professional tax.
- Kisan Credit Card credit limit.
- Irrigated land.
- Irrigation equipment.
- Carpet area.
- Mechanized agricultural equipment.
- Non-agricultural registered enterprise.

The Hindi and English question wording should explain these terms simply without changing the thresholds or conditions. If a user cannot answer confidently, the system must support “Not sure.”

---

## 7. Application documents

The current PMUY page and FAQ list the following documents.

| Document | Requirement | Product explanation |
|---|---|---|
| KYC application form | Required | Complete the official application |
| Applicant Aadhaar | Required | Identity/KYC |
| Address proof | Conditional when address differs from Aadhaar | Explain when additional proof is needed |
| Ration card or accepted government family-composition document | Required | Establish household composition |
| Aadhaar of adult family members listed in family-composition document | Required | Identity details for listed adults |
| Bank passbook / bank statement / cancelled cheque | Required | Bank account details |
| Deprivation Declaration | Required | Prescribed household undertaking |
| Migrant self-declaration / Annexure I | Conditional for applicable migrants | Use current official application/distributor guidance |

### 7.1 Important distinction

Document readiness is not eligibility.

For example, a user may appear to satisfy the eligibility rules but may not have a bank document ready. The system should show:
- Eligibility: likely eligible, subject to verification.
- Application readiness: documents incomplete.

It must not convert a missing bank document into an automatic eligibility rejection.

---

## 8. Application and verification process

The official FAQ describes online application through the PMUY portal, CSC assistance and offline application at an LPG distributor.

The reviewed FAQ states:
- Online self-submission has no fee.
- CSC-assisted submission carries a ₹20 charge.

The FAQ also describes:
- Aadhaar biometric authentication/e-KYC through the distributor.
- Verification of submitted documents against originals.
- Pre-installation inspection at the applicant's premises before connection release.

### 8.1 Family-split cases

The FAQ describes cases where family members have separated but remain linked to an earlier household LPG connection. The applicant may need to contact the concerned distributor/OMC to resolve the linked records before applying with updated family-composition evidence.

**Product handling:** Show “Verification required — contact distributor/OMC to resolve household linkage.” Do not automatically reject or approve based on an unclear record.

---

## 9. Eligibility assessment design

### 9.1 Three separate dimensions

The system must not collapse eligibility, verification and document readiness into one Boolean or score.

**Eligibility result**
- Likely eligible.
- Likely not eligible.
- Cannot determine yet.

**Verification status**
- Required.
- Pending.
- Not started.
- Not applicable.

**Application readiness**
- Ready to prepare.
- Documents incomplete.
- Needs distributor guidance.
- Unknown.

### 9.2 Decision table

| Situation | Eligibility result | Status / explanation |
|---|---|---|
| Applicant is not a woman | Likely not eligible | Applicant condition not met |
| Applicant is under 18 | Likely not eligible | Age condition not met |
| Applicant does not satisfy citizenship/residence undertaking | Likely not eligible or cannot determine pending clarification | KYC undertaking not satisfied; official confirmation may be needed |
| Existing LPG connection in defined household | Likely not eligible | Household LPG exclusion |
| Domestic PNG connection in dwelling unit | Likely not eligible for subsidised LPG under reviewed KYC undertaking | Distributor/OMC confirmation |
| Any D01–D12 answer is Yes | Likely not eligible | Listed deprivation exclusion indicated |
| One or more required answers are unknown | Cannot determine yet | Follow-up or verification required |
| Answers contradict one another | Cannot determine yet | Clarification required |
| All self-reported conditions appear satisfied | Likely eligible | Official distributor verification remains required |
| Documents missing | Eligibility remains separate | Application readiness incomplete |
| Biometric authentication/document verification/inspection pending | Eligibility remains separate | Verification pending |

### 9.3 Evaluation order

1. Confirm the user is asking about a new PMUY connection.
2. Collect applicant conditions: woman, age, citizenship/residence undertaking.
3. Establish the household using the KYC definition.
4. Check existing LPG connection.
5. Check domestic PNG restriction separately.
6. Ask D01–D12.
7. If an exclusion is indicated, return likely not eligible and cite the rule.
8. If information is unknown or contradictory, return cannot determine yet.
9. If all self-reported conditions pass, return likely eligible.
10. Separately show documents, application readiness and official verification requirements.

### 9.4 Non-negotiable engine rules

- The LLM may explain a result but must not override deterministic rule evaluation.
- Unknown must never be treated as No.
- Missing data must never be treated as a passing condition.
- An exclusion must be linked to its rule ID and source.
- A result must be labelled indicative, not official approval.

---

## 10. Proposed PMUY interview flow

### Stage 1 — Applicant

1. Are you applying for the connection in your own name?
2. Are you a woman?
3. Have you completed 18 years of age?
4. Are you an Indian citizen currently residing in India?

Evaluate R01, R02 and R05.

### Stage 2 — Household

Explain the KYC household definition.

5. Does anyone in your defined household already have an LPG connection?
6. Does your current dwelling unit have a domestic Piped Natural Gas (PNG) connection?

Evaluate R03, R06 and D13. Do not count D13 twice.

### Stage 3 — Deprivation declaration

Explain why the questions are being asked. Ask D01–D12 one at a time.

Each question must accept:
- Yes.
- No.
- Not sure.

### Stage 4 — Application readiness

1. Do you have a ration card or another accepted government family-composition document?
2. Does your current address match your Aadhaar?
3. Are Aadhaar details available for adult family members listed in the family-composition document?
4. Do you have your bank account document?
5. Are you applying as a migrant?

These are document/readiness questions, not all independent eligibility gates.

### Stage 5 — Assessment

Display:
- Eligibility result.
- Conditions satisfied.
- Exclusions identified.
- Unknown or contradictory information.
- Documents required.
- Application route.
- Verification steps.
- Official sources.

---

## 11. Edge cases

| Case | Expected handling |
|---|---|
| Applicant is under 18 | Likely not eligible for that applicant |
| Applicant is male | Likely not eligible |
| Household has existing LPG connection | Likely not eligible; if household split/record linkage is disputed, refer to distributor/OMC |
| User does not know whether household has LPG | Cannot determine; do not assume No |
| No ration card but another accepted government family-composition document exists | Continue assessment; do not reject solely for no ration card |
| Migrant applicant | Explain applicable self-declaration route; confirm accepted evidence with distributor |
| Missing bank document | Eligibility separate; application readiness incomplete |
| Domestic PNG connection | Explain separate restriction in reviewed KYC undertaking |
| Unclear land/asset details | Clarify exact official threshold; otherwise mark unknown |
| Contradictory household answers | Ask for clarification; do not select the favourable answer |

---

## 12. Evaluation test cases

These are designed test cases, not measured model results.

| ID | Scenario | Expected outcome |
|---|---|---|
| TC01 | Adult woman, Indian resident, all declaration answers No, no LPG/PNG | Likely eligible + verification required |
| TC02 | Applicant is 17 | Likely not eligible |
| TC03 | Applicant is male | Likely not eligible |
| TC04 | Existing household LPG connection | Likely not eligible |
| TC05 | Domestic PNG connection | Likely not eligible for subsidised LPG under reviewed KYC undertaking |
| TC06 | Household member earns ₹12,000/month | Likely not eligible under D01 |
| TC07 | Household member pays income tax | Likely not eligible under D03 |
| TC08 | House above 30 m² received through a government scheme | D10 not triggered by that house; evaluate remaining rules |
| TC09 | Applicant does not know KCC credit limit | Cannot determine / verification required |
| TC10 | Applicant has another accepted government family-composition document | Continue assessment |
| TC11 | Family has split but members remain linked to old LPG connection | Distributor/OMC record resolution required |
| TC12 | All self-reported conditions pass but biometric authentication is pending | Likely eligible + verification pending |

---

## 13. Voice, text and language behaviour

### Frozen product decision

- Languages: Hindi and English.
- User manually selects response language.
- Voice input: written and spoken response.
- Text input: written response with optional Listen button.
- One grounded answer and one eligibility evaluation pipeline serve both modalities.
- Do not run separate eligibility logic for voice and text.

### Recommended answer-card structure

1. Eligibility result.
2. Short reason.
3. Conditions satisfied.
4. Exclusions identified.
5. Missing/uncertain information.
6. Documents required.
7. Application location/process.
8. Verification notice.
9. Official source references.
10. Listen button for text responses.

---

## 14. Privacy and safety requirements

- Do not ask users to speak Aadhaar numbers or bank account numbers into the assistant.
- Do not claim to submit an application.
- Do not claim to approve a connection.
- Do not represent a preliminary result as an official government decision.
- Do not invent missing thresholds or exceptions.
- Do not treat missing documents as automatic ineligibility.
- Avoid storing unnecessary sensitive personal information in logs or test data.
- Refer unresolved identity, record-linkage and document issues to the authorised distributor/OMC process.

---

## 15. Limitations and open verification

### 15.1 Deprivation Declaration revision date

The reviewed official Deprivation Declaration PDF does not visibly state a publication date or revision number. The research can confirm that the PDF was linked from the official PMUY site as captured on 2026-10-30, but cannot independently certify when the PDF itself was last revised.

**Action:** Confirm with an LPG distributor/OMC that this is the currently accepted declaration before operational deployment. Record any replacement document and revalidate all thresholds.

### 15.2 Other limitations

- Self-reported answers cannot establish official records.
- Distributor/OMC verification remains necessary.
- Household composition can be complicated by migration, separation or outdated LPG records.
- Users may not understand technical asset/land terminology without explanation.
- PMUY rules and forms can change; source freshness must be monitored.
- This report does not establish PM-KISAN or PM-JAY eligibility rules.

---

## 16. Team work allocation

| Owner | Responsibility |
|---|---|
| Ankush | Review rule logic, define eligibility-engine contract and integrate scheme reasoning |
| Anamika | Verify the declaration version with distributor/OMC; validate each criterion against official sources |
| Aditya | Design interview UI, progress indicator, language selection, answer card and Listen interaction |

### Immediate follow-up

1. Confirm the latest accepted Deprivation Declaration with an LPG distributor/OMC.
2. Validate Hindi and English wording for all 12 distinct deprivation questions.
3. Review PMUY edge cases with the team.
4. Use this PMUY pack as the reference for Phase 3 system design.
5. Research PM-KISAN and PM-JAY 70+ separately before implementing those rule sets.

---

## 17. Frozen decision record

**Status:** PMUY research pack approved/frozen by the team for project design.

### Frozen

1. PMUY 2.0 is the reference scheme for the first complete Yojana Mitra eligibility flow.
2. Use the current official Ujjwala 2.0 top-level conditions and reviewed Deprivation Declaration.
3. Include KYC Version 8.0 citizenship/residence and domestic PNG undertakings.
4. Use the KYC household definition based on family-composition document and common kitchen.
5. Evaluate D13 only once because it overlaps with the existing-LPG condition.
6. Keep eligibility result, verification status and application readiness separate.
7. Use deterministic rule evaluation; LLM explains but does not override eligibility.
8. Support Hindi and English with manual language selection.
9. Voice input receives spoken and written output; text input receives written output with optional voice playback.
10. PM-KISAN and PM-JAY 70+ require separate official-source extraction.

### Open

1. Confirm whether the linked Deprivation Declaration has a newer distributor/OMC-issued revision — Anamika.
2. Validate Hindi question wording and user comprehension — Team.
3. Complete PM-KISAN and PM-JAY 70+ source extraction and rule validation — Ankush and Anamika.

### Assumptions

1. The currently linked official declaration is the applicable declaration for the captured PMUY 2.0 application process; its PDF revision date is not visible.
2. User self-reports are suitable for preliminary assessment but cannot replace distributor verification.
3. The PMUY rule sheet is the reference design for other scheme-specific rule sheets.

### Next phase

**Phase 3 — Product flow, eligibility logic, architecture and technical contracts.**

The first action is to define the complete Yojana Mitra user journey, from scheme selection through interview, assessment and take-away card. Phase 3 should begin only after the user's explicit transition confirmation.
