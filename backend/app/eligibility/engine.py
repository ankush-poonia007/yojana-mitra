"""Deterministic PMUY Eligibility Engine.

Owned by Anamika.
Evaluates PMUY 2.0 eligibility without LLM intervention.
Conforms strictly to:
- shared/api-contract.md (§4.4, §4.8)
- docs/research/PMUY/PMUY_RAG_Knowledge_Base.md (§8)
- docs/DECISIONS.md (Phase 4.1 decisions D1-D14)
"""

from typing import Any
from app.eligibility.models import (
    EligibilityResult,
    PMUYAnswers,
    PMUYAssessmentResult,
    ReadinessStatus,
    RuleEvaluation,
    VerificationStatus,
)
from app.eligibility.rules import DEPRIVATION_RULES, PRIMARY_RULES


def evaluate_pmuy_eligibility(
    answers: PMUYAnswers | dict[str, Any],
    language: str = "hi",
) -> PMUYAssessmentResult:
    """Evaluate PMUY 2.0 eligibility deterministically.

    Args:
        answers: PMUYAnswers instance or dictionary of answer keys.
        language: Language code ('hi' or 'en') for generated reasons.

    Returns:
        PMUYAssessmentResult with result, reasons, missing_information,
        triggered_rules, passed_rules, verification_status, and readiness_status.
    """
    if isinstance(answers, dict):
        validated_answers = PMUYAnswers.model_validate(answers)
    elif isinstance(answers, PMUYAnswers):
        validated_answers = answers
    else:
        raise TypeError(f"Expected PMUYAnswers or dict, got {type(answers).__name__}")

    is_hindi = language.lower().startswith("hi")

    # Contradiction check: applicant_age contradicts age_18_or_above (KB §8)
    if validated_answers.age_contradiction:
        reason = (
            "विरोधाभासी जानकारी: दी गई आयु और 18 वर्ष या अधिक के विकल्प में विसंगति है। स्पष्टीकरण आवश्यक है।"
            if is_hindi
            else "Contradictory information: Provided applicant_age contradicts age_18_or_above. Clarification required."
        )
        return PMUYAssessmentResult(
            scheme_id="pmuy",
            result=EligibilityResult.CANNOT_DETERMINE,
            reasons=[reason],
            missing_information=["applicant_age", "age_18_or_above"],
            triggered_rules=["PMUY-R02"],
            passed_rules=[],
            verification_status=VerificationStatus.REQUIRED,
            readiness_status=ReadinessStatus.UNKNOWN,
        )

    # Special handling for family split dispute (PMUY-T11)
    if validated_answers.family_split_dispute is True:
        split_reason = (
            "परिवार अलग हो चुका है लेकिन पुराने एलपीजी कनेक्शन से नाम लिंक है। "
            "रिकॉर्ड सुधार के लिए एलपीजी वितरक/ओएमसी से संपर्क आवश्यक है।"
            if is_hindi
            else "Family has separated but records remain linked to an earlier LPG connection. "
            "Distributor/OMC record resolution is required."
        )
        return PMUYAssessmentResult(
            scheme_id="pmuy",
            result=EligibilityResult.CANNOT_DETERMINE,
            reasons=[split_reason],
            missing_information=["household_linkage_resolution"],
            triggered_rules=["PMUY-VER-04"],
            passed_rules=[],
            verification_status=VerificationStatus.REQUIRED,
            readiness_status=ReadinessStatus.NEEDS_DISTRIBUTOR_GUIDANCE,
        )

    # 1. Evaluate Primary Rules (R01, R02, R03, R05, R06)
    exclusions: list[RuleEvaluation] = []
    missing_fields: list[str] = []
    passed_rules: list[RuleEvaluation] = []

    for rule_fn in PRIMARY_RULES:
        eval_res = rule_fn(validated_answers)
        if eval_res.triggered:
            exclusions.append(eval_res)
        elif eval_res.passed is True:
            passed_rules.append(eval_res)
        elif eval_res.missing_field:
            missing_fields.append(eval_res.missing_field)

    # 2. Evaluate Deprivation Declaration Rules (D01 - D12 under R04)
    deprivation_exclusions: list[RuleEvaluation] = []
    deprivation_missing: list[str] = []

    # Explicit failure of composite poor_household_declaration
    if validated_answers.poor_household_declaration is False:
        deprivation_exclusions.append(
            RuleEvaluation(
                rule_id="PMUY-R04",
                passed=False,
                triggered=True,
                reason_en="Applicant does not meet poor household deprivation declaration conditions.",
                reason_hi="आवेदक वंचित गरीब परिवार घोषणा की शर्तों को पूरा नहीं करता है।",
            )
        )

    for rule_fn in DEPRIVATION_RULES:
        eval_res = rule_fn(validated_answers)
        if eval_res.triggered:
            deprivation_exclusions.append(eval_res)
        elif eval_res.passed is True:
            passed_rules.append(eval_res)
        elif eval_res.missing_field:
            deprivation_missing.append(eval_res.missing_field)

    # Consolidate exclusions
    all_exclusions = exclusions + deprivation_exclusions

    # Consolidate missing information with contract aggregation (shared/api-contract.md §4.8)
    # If all 12 deprivation criteria are unanswered and not explicitly declared,
    # report the composite contract key 'poor_household_declaration'
    if (
        len(deprivation_missing) == len(DEPRIVATION_RULES)
        and validated_answers.poor_household_declaration is not True
    ):
        deprivation_missing_fields = ["poor_household_declaration"]
    elif validated_answers.poor_household_declaration is True and not deprivation_exclusions:
        # User provided an affirmative declaration and no individual exclusions were triggered
        deprivation_missing_fields = []
        passed_rules.append(
            RuleEvaluation(
                rule_id="PMUY-R04",
                passed=True,
                triggered=False,
                reason_en="Poor household deprivation declaration satisfied.",
                reason_hi="वंचित परिवार घोषणा की शर्तें पूरी हैं।",
            )
        )
    else:
        deprivation_missing_fields = deprivation_missing

    all_missing = missing_fields + deprivation_missing_fields

    # Determine eligibility result
    reasons: list[str] = []
    triggered_rule_ids: list[str] = []
    passed_rule_ids: list[str] = [p.rule_id for p in passed_rules]

    if all_exclusions:
        result = EligibilityResult.LIKELY_NOT_ELIGIBLE
        for excl in all_exclusions:
            reasons.append(excl.reason_hi if is_hindi else excl.reason_en)
            triggered_rule_ids.append(excl.rule_id)
    elif all_missing:
        result = EligibilityResult.CANNOT_DETERMINE
        for m_field in all_missing:
            field_desc = (
                f"अधूरी जानकारी: {m_field} की पुष्टि आवश्यक है।"
                if is_hindi
                else f"Missing information: {m_field} must be clarified."
            )
            reasons.append(field_desc)
    else:
        result = EligibilityResult.LIKELY_ELIGIBLE
        if is_hindi:
            reasons.append("आवेदक महिला है और उसकी आयु 18 वर्ष या उससे अधिक है।")
            reasons.append("परिवार के पास पहले से कोई एलपीजी कनेक्शन नहीं है।")
            reasons.append("वंचित परिवार के लिए निर्धारित सभी पात्रता शर्तें पूरी हैं।")
        else:
            reasons.append("Applicant is an adult woman (18+).")
            reasons.append("Household has no existing LPG connection.")
            reasons.append("Applicant meets poor household deprivation declaration conditions.")

    # Resolve Verification Status
    if validated_answers.biometric_authenticated is False:
        verification_status = VerificationStatus.PENDING
    else:
        verification_status = VerificationStatus.REQUIRED

    # Resolve Application Readiness Status (PMUY-R07)
    # Check family document: either ration card or accepted alternative
    has_family_doc = (
        validated_answers.has_ration_card is True
        or validated_answers.has_alternative_family_doc is True
    )
    has_bank = validated_answers.has_bank_account is True

    if validated_answers.has_ration_card is False and validated_answers.has_alternative_family_doc is False:
        readiness_status = ReadinessStatus.DOCUMENTS_INCOMPLETE
    elif validated_answers.has_bank_account is False:
        readiness_status = ReadinessStatus.DOCUMENTS_INCOMPLETE
    elif has_family_doc and has_bank:
        readiness_status = ReadinessStatus.READY_TO_PREPARE
    elif result == EligibilityResult.LIKELY_ELIGIBLE:
        readiness_status = ReadinessStatus.READY_TO_PREPARE
    else:
        readiness_status = ReadinessStatus.UNKNOWN

    return PMUYAssessmentResult(
        scheme_id="pmuy",
        result=result,
        reasons=reasons,
        missing_information=all_missing,
        triggered_rules=triggered_rule_ids,
        passed_rules=passed_rule_ids,
        verification_status=verification_status,
        readiness_status=readiness_status,
    )
