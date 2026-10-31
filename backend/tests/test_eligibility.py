"""Comprehensive automated test suite for PMUY deterministic eligibility engine.

Tests all 12 official baseline cases (PMUY-T01 through PMUY-T12),
verified engineering invariants, and checks for R04, age synchronization, and H3 schema.
"""

import copy
import pytest
from pydantic import ValidationError
from app.eligibility.engine import evaluate_pmuy_eligibility
from app.eligibility.models import (
    EligibilityResult,
    PMUYAnswers,
    ReadinessStatus,
    VerificationStatus,
)


@pytest.fixture
def clean_eligible_payload() -> dict:
    """Returns a baseline dictionary where all criteria pass."""
    return {
        "applicant_is_woman": True,
        "age_18_or_above": True,
        "citizen_and_resident": True,
        "household_has_lpg": False,
        "dwelling_has_png": False,
        "member_earns_above_10k": False,
        "pays_professional_tax": False,
        "pays_income_tax": False,
        "is_govt_employee": False,
        "has_registered_enterprise": False,
        "kcc_limit_above_50k": False,
        "land_gt_2_5_acres_irrigated": False,
        "land_gte_5_acres_irrigated_2seasons": False,
        "land_gte_7_5_acres_irrigated": False,
        "pucca_house_gt_30sqm": False,
        "house_from_govt_scheme": False,
        "has_motorized_vehicle_or_boat": False,
        "has_mechanized_agri_equipment": False,
        "has_ration_card": True,
        "has_bank_account": True,
    }


# ===========================================================================
# Official Baseline Cases: PMUY-T01 to PMUY-T12
# ===========================================================================

def test_pmuy_t01_positive_eligible(clean_eligible_payload):
    """PMUY-T01: Adult woman, Indian resident, all deprivation No, no LPG or PNG."""
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_ELIGIBLE
    assert res.verification_status == VerificationStatus.REQUIRED
    assert res.readiness_status == ReadinessStatus.READY_TO_PREPARE
    assert len(res.missing_information) == 0
    assert len(res.triggered_rules) == 0
    assert "PMUY-R01" in res.passed_rules
    assert "PMUY-R02" in res.passed_rules


def test_pmuy_t02_underage_applicant(clean_eligible_payload):
    """PMUY-T02: Applicant is 17 (under 18)."""
    clean_eligible_payload["applicant_age"] = 17
    clean_eligible_payload["age_18_or_above"] = None
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-R02" in res.triggered_rules


def test_pmuy_t03_male_applicant(clean_eligible_payload):
    """PMUY-T03: Applicant is male."""
    clean_eligible_payload["applicant_is_woman"] = False
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-R01" in res.triggered_rules


def test_pmuy_t04_existing_lpg(clean_eligible_payload):
    """PMUY-T04: Existing LPG connection in defined household."""
    clean_eligible_payload["household_has_lpg"] = True
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-R03" in res.triggered_rules


def test_pmuy_t05_domestic_png(clean_eligible_payload):
    """PMUY-T05: Household has domestic PNG."""
    clean_eligible_payload["dwelling_has_png"] = True
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-R06" in res.triggered_rules


def test_pmuy_t06_member_earns_above_10k(clean_eligible_payload):
    """PMUY-T06: Household member earns ₹12,000/month (above ₹10k threshold)."""
    clean_eligible_payload["member_earns_above_10k"] = True
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-D01" in res.triggered_rules


def test_pmuy_t07_income_tax(clean_eligible_payload):
    """PMUY-T07: Household member pays income tax."""
    clean_eligible_payload["pays_income_tax"] = True
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-D03" in res.triggered_rules


def test_pmuy_t08_government_house_exception(clean_eligible_payload):
    """PMUY-T08: House is above 30 m² but was received under a government scheme."""
    clean_eligible_payload["pucca_house_gt_30sqm"] = True
    clean_eligible_payload["house_from_govt_scheme"] = True
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_ELIGIBLE
    assert "PMUY-D10" not in res.triggered_rules
    assert "PMUY-D10" in res.passed_rules


def test_pmuy_t09_unknown_kcc_limit(clean_eligible_payload):
    """PMUY-T09: Applicant does not know KCC credit limit."""
    clean_eligible_payload["kcc_limit_above_50k"] = None
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.CANNOT_DETERMINE
    assert "kcc_limit_above_50k" in res.missing_information


def test_pmuy_t10_alternative_family_doc(clean_eligible_payload):
    """PMUY-T10: Applicant has another accepted government family-composition document."""
    clean_eligible_payload["has_ration_card"] = False
    clean_eligible_payload["has_alternative_family_doc"] = True
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_ELIGIBLE
    assert res.readiness_status == ReadinessStatus.READY_TO_PREPARE


def test_pmuy_t11_family_split_dispute(clean_eligible_payload):
    """PMUY-T11: Family has split but members remain linked to old LPG connection."""
    clean_eligible_payload["family_split_dispute"] = True
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.CANNOT_DETERMINE
    assert res.readiness_status == ReadinessStatus.NEEDS_DISTRIBUTOR_GUIDANCE
    assert res.verification_status == VerificationStatus.REQUIRED


def test_pmuy_t12_pending_biometric(clean_eligible_payload):
    """PMUY-T12: Conditions appear satisfied but biometric authentication is pending."""
    clean_eligible_payload["biometric_authenticated"] = False
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_ELIGIBLE
    assert res.verification_status == VerificationStatus.PENDING


# ===========================================================================
# Check 1: R04 Deprivation Aggregation & Short-Circuit Tests
# ===========================================================================

def test_r04_contract_missing_aggregation():
    """Verify verbatim match with shared/api-contract.md §4.8.

    When only woman, age, and LPG are answered, missing_information must include
    'poor_household_declaration'.
    """
    answers = {
        "applicant_is_woman": True,
        "age_18_or_above": True,
        "household_has_lpg": False,
        "citizen_and_resident": True,
        "dwelling_has_png": False,
    }
    res = evaluate_pmuy_eligibility(answers)
    assert res.result == EligibilityResult.CANNOT_DETERMINE
    assert "poor_household_declaration" in res.missing_information


def test_r04_explicit_declaration_failure(clean_eligible_payload):
    """Verify explicit poor_household_declaration=False triggers PMUY-R04 exclusion."""
    clean_eligible_payload["poor_household_declaration"] = False
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-R04" in res.triggered_rules


def test_r04_affirmative_declaration_passes(clean_eligible_payload):
    """Verify affirmative poor_household_declaration passes when no individual exclusion is set."""
    payload = {
        "applicant_is_woman": True,
        "age_18_or_above": True,
        "citizen_and_resident": True,
        "household_has_lpg": False,
        "dwelling_has_png": False,
        "poor_household_declaration": True,
        "has_ration_card": True,
        "has_bank_account": True,
    }
    res = evaluate_pmuy_eligibility(payload)
    assert res.result == EligibilityResult.LIKELY_ELIGIBLE
    assert "PMUY-R04" in res.passed_rules
    assert len(res.missing_information) == 0


def test_r04_single_exclusion_short_circuits_missing_criteria():
    """Verify any single True exclusion triggers not_eligible even if other D rules are None."""
    answers = {
        "applicant_is_woman": True,
        "age_18_or_above": True,
        "household_has_lpg": False,
        "citizen_and_resident": True,
        "dwelling_has_png": False,
        "member_earns_above_10k": True,  # Disqualifying exclusion!
        # All other 11 deprivation fields are None (unanswered)
    }
    res = evaluate_pmuy_eligibility(answers)
    assert res.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-D01" in res.triggered_rules


# ===========================================================================
# Check 2: Age Model Synchronization & Inconsistency Tests
# ===========================================================================

def test_age_contradiction_handling():
    """Verify that contradictory age inputs (age 16 vs age_18_or_above=True) yield cannot_determine."""
    answers = {
        "applicant_is_woman": True,
        "applicant_age": 16,
        "age_18_or_above": True,  # Direct contradiction!
        "household_has_lpg": False,
    }
    res = evaluate_pmuy_eligibility(answers)
    assert res.result == EligibilityResult.CANNOT_DETERMINE
    assert "applicant_age" in res.missing_information
    assert "age_18_or_above" in res.missing_information
    assert "विसंगति" in res.reasons[0] or "contradicts" in res.reasons[0]


def test_age_out_of_bounds_validation():
    """Verify that negative age or impossible age values raise Pydantic ValidationError."""
    with pytest.raises(ValidationError):
        PMUYAnswers(applicant_age=-5)

    with pytest.raises(ValidationError):
        PMUYAnswers(applicant_age=150)


def test_age_synchronization_from_integer():
    """Verify applicant_age=25 sets age_18_or_above=True automatically."""
    answers = PMUYAnswers(applicant_age=25)
    assert answers.age_18_or_above is True

    answers_minor = PMUYAnswers(applicant_age=16)
    assert answers_minor.age_18_or_above is False


# ===========================================================================
# Check 3: Exact Result Schema Compatibility with H3 & API
# ===========================================================================

def test_to_api_assessment_strict_schema(clean_eligible_payload):
    """Verify to_api_assessment() returns strictly the 4 frozen contract fields."""
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    api_dict = res.to_api_assessment()

    # Must match shared/api-contract.md §4.4 keys exactly
    expected_keys = {"scheme_id", "result", "reasons", "missing_information"}
    assert set(api_dict.keys()) == expected_keys
    assert api_dict["scheme_id"] == "pmuy"
    assert api_dict["result"] == "likely_eligible"
    assert isinstance(api_dict["reasons"], list)
    assert isinstance(api_dict["missing_information"], list)


def test_workflow_context_contains_all_dimensions(clean_eligible_payload):
    """Verify to_workflow_context() carries verification and readiness for LangGraph."""
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    wf_dict = res.to_workflow_context()

    assert "verification_status" in wf_dict
    assert "readiness_status" in wf_dict
    assert "triggered_rules" in wf_dict
    assert "passed_rules" in wf_dict


# ===========================================================================
# Engineering Invariant & Safeguard Tests
# ===========================================================================

def test_unknown_does_not_coerce_to_no():
    """Verify unknown required answer produces cannot_determine, never likely_eligible."""
    answers = PMUYAnswers(
        applicant_is_woman=True,
        age_18_or_above=True,
        household_has_lpg=None,  # Unknown!
    )
    res = evaluate_pmuy_eligibility(answers)
    assert res.result == EligibilityResult.CANNOT_DETERMINE
    assert "household_has_lpg" in res.missing_information


def test_r05_ternary_behavior(clean_eligible_payload):
    """Verify Decision D3: R05 clear failure -> not eligible; unknown -> cannot determine."""
    payload_fail = dict(clean_eligible_payload)
    payload_fail["citizen_and_resident"] = False
    res_fail = evaluate_pmuy_eligibility(payload_fail)
    assert res_fail.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-R05" in res_fail.triggered_rules

    payload_unknown = dict(clean_eligible_payload)
    payload_unknown["citizen_and_resident"] = None
    res_unknown = evaluate_pmuy_eligibility(payload_unknown)
    assert res_unknown.result == EligibilityResult.CANNOT_DETERMINE
    assert "citizen_and_resident" in res_unknown.missing_information

    payload_pass = dict(clean_eligible_payload)
    payload_pass["citizen_and_resident"] = True
    res_pass = evaluate_pmuy_eligibility(payload_pass)
    assert res_pass.result == EligibilityResult.LIKELY_ELIGIBLE


def test_d10_unexcepted_house_excludes(clean_eligible_payload):
    """Verify D10 triggers exclusion if > 30 sqm and NOT from government scheme."""
    clean_eligible_payload["pucca_house_gt_30sqm"] = True
    clean_eligible_payload["house_from_govt_scheme"] = False
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_NOT_ELIGIBLE
    assert "PMUY-D10" in res.triggered_rules


def test_r07_readiness_separation_missing_bank(clean_eligible_payload):
    """Verify missing document affects readiness (DOCUMENTS_INCOMPLETE), NOT eligibility."""
    clean_eligible_payload["has_bank_account"] = False
    res = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert res.result == EligibilityResult.LIKELY_ELIGIBLE
    assert res.readiness_status == ReadinessStatus.DOCUMENTS_INCOMPLETE


def test_input_immutability(clean_eligible_payload):
    """Verify that evaluate_pmuy_eligibility does not mutate input dictionary."""
    original = copy.deepcopy(clean_eligible_payload)
    _ = evaluate_pmuy_eligibility(clean_eligible_payload)
    assert clean_eligible_payload == original


def test_deterministic_repeatability(clean_eligible_payload):
    """Verify identical results over 100 repeated runs."""
    first_run = evaluate_pmuy_eligibility(clean_eligible_payload).model_dump()
    for _ in range(100):
        assert evaluate_pmuy_eligibility(clean_eligible_payload).model_dump() == first_run


def test_language_localization(clean_eligible_payload):
    """Verify English and Hindi reason generation."""
    res_hi = evaluate_pmuy_eligibility(clean_eligible_payload, language="hi")
    res_en = evaluate_pmuy_eligibility(clean_eligible_payload, language="en")

    assert any("महिला" in r for r in res_hi.reasons)
    assert any("woman" in r for r in res_en.reasons)
