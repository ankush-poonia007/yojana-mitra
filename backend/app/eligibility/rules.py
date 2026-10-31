"""Pure Python rule evaluation functions for PMUY 2.0.

Owned by Anamika.
Encodes rules R01-R06 and declarations D01-D12 strictly from:
- docs/research/PMUY/PMUY_RAG_Knowledge_Base.md (§4, §5)
- docs/DECISIONS.md (Phase 4.1 decisions D1-D14)
"""

from typing import Callable
from app.eligibility.models import PMUYAnswers, RuleEvaluation


def check_r01_woman(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-R01: Applicant must be a woman."""
    if answers.applicant_is_woman is True:
        return RuleEvaluation(
            rule_id="PMUY-R01",
            passed=True,
            triggered=False,
            reason_en="Applicant is a woman.",
            reason_hi="आवेदक महिला है।",
        )
    if answers.applicant_is_woman is False:
        return RuleEvaluation(
            rule_id="PMUY-R01",
            passed=False,
            triggered=True,
            reason_en="Applicant is not a woman. PMUY requires the applicant to be a woman.",
            reason_hi="आवेदक महिला नहीं है। उज्ज्वला योजना में केवल महिला के नाम पर कनेक्शन जारी होता है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-R01",
        passed=None,
        triggered=False,
        missing_field="applicant_is_woman",
        reason_en="Applicant gender is unknown.",
        reason_hi="आवेदक का लिंग ज्ञात नहीं है।",
    )


def check_r02_age(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-R02: Applicant must have attained 18 years of age."""
    if answers.age_18_or_above is True:
        return RuleEvaluation(
            rule_id="PMUY-R02",
            passed=True,
            triggered=False,
            reason_en="Applicant has attained 18 years of age.",
            reason_hi="आवेदक की आयु 18 वर्ष या उससे अधिक है।",
        )
    if answers.age_18_or_above is False:
        return RuleEvaluation(
            rule_id="PMUY-R02",
            passed=False,
            triggered=True,
            reason_en="Applicant is under 18 years of age. PMUY requires the applicant to be at least 18.",
            reason_hi="आवेदक की आयु 18 वर्ष से कम है। उज्ज्वला योजना के लिए न्यूनतम आयु 18 वर्ष होना अनिवार्य है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-R02",
        passed=None,
        triggered=False,
        missing_field="age_18_or_above",
        reason_en="Applicant age is unknown.",
        reason_hi="आवेदक की आयु ज्ञात नहीं है।",
    )


def check_r03_lpg(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-R03 & PMUY-D13: No other LPG connection in the defined household.

    D13 is evaluated once strictly through this rule per Decision D2.
    """
    if answers.household_has_lpg is False:
        return RuleEvaluation(
            rule_id="PMUY-R03",
            passed=True,
            triggered=False,
            reason_en="No existing LPG connection in the defined household.",
            reason_hi="परिवार के पास पहले से कोई एलपीजी कनेक्शन नहीं है।",
        )
    if answers.household_has_lpg is True:
        return RuleEvaluation(
            rule_id="PMUY-R03",
            passed=False,
            triggered=True,
            reason_en="Household already has an LPG connection from an Oil Marketing Company (OMC).",
            reason_hi="परिवार के पास पहले से एलपीजी कनेक्शन मौजूद है। योजना के नियमों के तहत एक परिवार में दूसरा कनेक्शन नहीं मिल सकता।",
        )
    return RuleEvaluation(
        rule_id="PMUY-R03",
        passed=None,
        triggered=False,
        missing_field="household_has_lpg",
        reason_en="Household LPG connection status is unknown.",
        reason_hi="परिवार में मौजूदा एलपीजी कनेक्शन की स्थिति ज्ञात नहीं है।",
    )


def check_r05_citizenship(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-R05: KYC Indian citizenship and residence undertaking.

    Per Decision D3: Clear failure maps to likely_not_eligible; uncertain maps to cannot_determine.
    """
    if answers.citizen_and_resident is True:
        return RuleEvaluation(
            rule_id="PMUY-R05",
            passed=True,
            triggered=False,
            reason_en="Applicant satisfies Indian citizenship and residence undertaking.",
            reason_hi="आवेदक भारतीय नागरिकता और निवास की शर्त पूरी करती है।",
        )
    if answers.citizen_and_resident is False:
        return RuleEvaluation(
            rule_id="PMUY-R05",
            passed=False,
            triggered=True,
            reason_en="Applicant does not satisfy Indian citizenship and residence undertaking.",
            reason_hi="आवेदक भारतीय नागरिकता और निवास की शर्त पूरी नहीं करती है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-R05",
        passed=None,
        triggered=False,
        missing_field="citizen_and_resident",
        reason_en="Citizenship and residence undertaking status is unknown.",
        reason_hi="नागरिकता और निवास की स्थिति स्पष्ट नहीं है।",
    )


def check_r06_png(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-R06: Domestic Piped Natural Gas (PNG) connection restriction.

    Per Decision D4: PNG in dwelling unit means likely not eligible for subsidised LPG
    (subject to distributor confirmation).
    """
    if answers.dwelling_has_png is False:
        return RuleEvaluation(
            rule_id="PMUY-R06",
            passed=True,
            triggered=False,
            reason_en="No domestic Piped Natural Gas (PNG) connection in dwelling unit.",
            reason_hi="आवास में कोई घरेलू पाइप्ड नेचुरल गैस (PNG) कनेक्शन नहीं है।",
        )
    if answers.dwelling_has_png is True:
        return RuleEvaluation(
            rule_id="PMUY-R06",
            passed=False,
            triggered=True,
            reason_en="Domestic PNG connection in dwelling unit excludes household from subsidised LPG (subject to distributor confirmation).",
            reason_hi="आवास में घरेलू पीएनजी कनेक्शन होने पर रियायती एलपीजी कनेक्शन की पात्रता नहीं मिलती (वितरक पुष्टि के अधीन)।",
        )
    return RuleEvaluation(
        rule_id="PMUY-R06",
        passed=None,
        triggered=False,
        missing_field="dwelling_has_png",
        reason_en="Domestic PNG connection status is unknown.",
        reason_hi="घरेलू पीएनजी कनेक्शन की स्थिति ज्ञात नहीं है।",
    )


# ---------------------------------------------------------------------------
# Deprivation Declaration Criteria D01 - D12 (evaluated under PMUY-R04)
# ---------------------------------------------------------------------------

def check_d01_income(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D01: Any household member earns > ₹10,000/month."""
    if answers.member_earns_above_10k is True:
        return RuleEvaluation(
            rule_id="PMUY-D01",
            passed=False,
            triggered=True,
            reason_en="Household member earns more than ₹10,000 per month.",
            reason_hi="परिवार का कोई सदस्य प्रति माह ₹10,000 से अधिक कमाता है।",
        )
    if answers.member_earns_above_10k is False:
        return RuleEvaluation(
            rule_id="PMUY-D01",
            passed=True,
            triggered=False,
            reason_en="No household member earns above ₹10,000 per month.",
            reason_hi="परिवार का कोई भी सदस्य प्रति माह ₹10,000 से अधिक नहीं कमाता।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D01",
        passed=None,
        triggered=False,
        missing_field="member_earns_above_10k",
        reason_en="Monthly member earning status is unknown.",
        reason_hi="मासिक आय की स्थिति ज्ञात नहीं है।",
    )


def check_d02_professional_tax(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D02: Household member pays professional tax."""
    if answers.pays_professional_tax is True:
        return RuleEvaluation(
            rule_id="PMUY-D02",
            passed=False,
            triggered=True,
            reason_en="Household member pays professional tax.",
            reason_hi="परिवार का सदस्य व्यावसायिक कर (Professional Tax) चुकाता है।",
        )
    if answers.pays_professional_tax is False:
        return RuleEvaluation(
            rule_id="PMUY-D02",
            passed=True,
            triggered=False,
            reason_en="No household member pays professional tax.",
            reason_hi="परिवार का कोई सदस्य व्यावसायिक कर नहीं चुकाता।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D02",
        passed=None,
        triggered=False,
        missing_field="pays_professional_tax",
        reason_en="Professional tax payment status is unknown.",
        reason_hi="व्यावसायिक कर की स्थिति ज्ञात नहीं है।",
    )


def check_d03_income_tax(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D03: Household member pays income tax."""
    if answers.pays_income_tax is True:
        return RuleEvaluation(
            rule_id="PMUY-D03",
            passed=False,
            triggered=True,
            reason_en="Household member pays income tax.",
            reason_hi="परिवार का सदस्य आयकर (Income Tax) चुकाता है।",
        )
    if answers.pays_income_tax is False:
        return RuleEvaluation(
            rule_id="PMUY-D03",
            passed=True,
            triggered=False,
            reason_en="No household member pays income tax.",
            reason_hi="परिवार का कोई सदस्य आयकर नहीं चुकाता।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D03",
        passed=None,
        triggered=False,
        missing_field="pays_income_tax",
        reason_en="Income tax payment status is unknown.",
        reason_hi="आयकर की स्थिति ज्ञात नहीं है।",
    )


def check_d04_govt_employee(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D04: Household member is a government employee."""
    if answers.is_govt_employee is True:
        return RuleEvaluation(
            rule_id="PMUY-D04",
            passed=False,
            triggered=True,
            reason_en="Household member is a government employee.",
            reason_hi="परिवार का सदस्य सरकारी कर्मचारी है।",
        )
    if answers.is_govt_employee is False:
        return RuleEvaluation(
            rule_id="PMUY-D04",
            passed=True,
            triggered=False,
            reason_en="No household member is a government employee.",
            reason_hi="परिवार का कोई सदस्य सरकारी कर्मचारी नहीं है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D04",
        passed=None,
        triggered=False,
        missing_field="is_govt_employee",
        reason_en="Government employment status is unknown.",
        reason_hi="सरकारी नौकरी की स्थिति ज्ञात नहीं है।",
    )


def check_d05_registered_enterprise(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D05: Household has a government-registered non-agricultural enterprise."""
    if answers.has_registered_enterprise is True:
        return RuleEvaluation(
            rule_id="PMUY-D05",
            passed=False,
            triggered=True,
            reason_en="Household has a registered non-agricultural enterprise.",
            reason_hi="परिवार का सरकार के साथ पंजीकृत गैर-कृषि व्यवसाय है।",
        )
    if answers.has_registered_enterprise is False:
        return RuleEvaluation(
            rule_id="PMUY-D05",
            passed=True,
            triggered=False,
            reason_en="No registered non-agricultural enterprise.",
            reason_hi="कोई पंजीकृत गैर-कृषि व्यवसाय नहीं है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D05",
        passed=None,
        triggered=False,
        missing_field="has_registered_enterprise",
        reason_en="Enterprise registration status is unknown.",
        reason_hi="पंजीकृत व्यवसाय की स्थिति ज्ञात नहीं है।",
    )


def check_d06_kcc_limit(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D06: Kisan Credit Card with credit limit above ₹50,000."""
    if answers.kcc_limit_above_50k is True:
        return RuleEvaluation(
            rule_id="PMUY-D06",
            passed=False,
            triggered=True,
            reason_en="Kisan Credit Card credit limit exceeds ₹50,000.",
            reason_hi="किसान क्रेडिट कार्ड की सीमा ₹50,000 से अधिक है।",
        )
    if answers.kcc_limit_above_50k is False:
        return RuleEvaluation(
            rule_id="PMUY-D06",
            passed=True,
            triggered=False,
            reason_en="KCC credit limit is not above ₹50,000 (or no KCC).",
            reason_hi="किसान क्रेडिट कार्ड की सीमा ₹50,000 से अधिक नहीं है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D06",
        passed=None,
        triggered=False,
        missing_field="kcc_limit_above_50k",
        reason_en="Kisan Credit Card credit limit is unknown.",
        reason_hi="किसान क्रेडिट कार्ड सीमा की स्थिति ज्ञात नहीं है।",
    )


def check_d07_land_irrigated_2_5(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D07: > 2.5 acres irrigated land with one irrigation equipment."""
    if answers.land_gt_2_5_acres_irrigated is True:
        return RuleEvaluation(
            rule_id="PMUY-D07",
            passed=False,
            triggered=True,
            reason_en="Household owns more than 2.5 acres of irrigated land with irrigation equipment.",
            reason_hi="परिवार के पास सिंचाई उपकरण सहित 2.5 एकड़ से अधिक सिंचित भूमि है।",
        )
    if answers.land_gt_2_5_acres_irrigated is False:
        return RuleEvaluation(
            rule_id="PMUY-D07",
            passed=True,
            triggered=False,
            reason_en="Household does not own > 2.5 acres irrigated land with equipment.",
            reason_hi="परिवार के पास उपकरण सहित 2.5 एकड़ से अधिक सिंचित भूमि नहीं है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D07",
        passed=None,
        triggered=False,
        missing_field="land_gt_2_5_acres_irrigated",
        reason_en="Irrigated land area (2.5 acre threshold) is unknown.",
        reason_hi="2.5 एकड़ सिंचित भूमि की स्थिति ज्ञात नहीं है।",
    )


def check_d08_land_irrigated_5(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D08: >= 5 acres irrigated land for two or more crop seasons."""
    if answers.land_gte_5_acres_irrigated_2seasons is True:
        return RuleEvaluation(
            rule_id="PMUY-D08",
            passed=False,
            triggered=True,
            reason_en="Household owns 5 or more acres of irrigated land for 2+ crop seasons.",
            reason_hi="परिवार के पास दो या अधिक फसलों के लिए 5 एकड़ या उससे अधिक सिंचित भूमि है।",
        )
    if answers.land_gte_5_acres_irrigated_2seasons is False:
        return RuleEvaluation(
            rule_id="PMUY-D08",
            passed=True,
            triggered=False,
            reason_en="Household does not own >= 5 acres irrigated land for 2+ seasons.",
            reason_hi="परिवार के पास 5 एकड़ या उससे अधिक दो-फसली सिंचित भूमि नहीं है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D08",
        passed=None,
        triggered=False,
        missing_field="land_gte_5_acres_irrigated_2seasons",
        reason_en="Two-season irrigated land area is unknown.",
        reason_hi="5 एकड़ दो-फसली सिंचित भूमि की स्थिति ज्ञात नहीं है।",
    )


def check_d09_land_irrigated_7_5(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D09: >= 7.5 acres land with at least one irrigation equipment."""
    if answers.land_gte_7_5_acres_irrigated is True:
        return RuleEvaluation(
            rule_id="PMUY-D09",
            passed=False,
            triggered=True,
            reason_en="Household owns at least 7.5 acres of land with irrigation equipment.",
            reason_hi="परिवार के पास सिंचाई उपकरण सहित कम से कम 7.5 एकड़ भूमि है।",
        )
    if answers.land_gte_7_5_acres_irrigated is False:
        return RuleEvaluation(
            rule_id="PMUY-D09",
            passed=True,
            triggered=False,
            reason_en="Household does not own >= 7.5 acres land with equipment.",
            reason_hi="परिवार के पास उपकरण सहित 7.5 एकड़ या उससे अधिक भूमि नहीं है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D09",
        passed=None,
        triggered=False,
        missing_field="land_gte_7_5_acres_irrigated",
        reason_en="Land area (7.5 acre threshold) is unknown.",
        reason_hi="7.5 एकड़ भूमि की स्थिति ज्ञात नहीं है।",
    )


def check_d10_housing(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D10: House > 30 sq metres carpet area, except from a government scheme."""
    if answers.pucca_house_gt_30sqm is True:
        # Check government scheme exception
        if answers.house_from_govt_scheme is True:
            return RuleEvaluation(
                rule_id="PMUY-D10",
                passed=True,
                triggered=False,
                reason_en="House is above 30 sq metres but received under a government scheme (exception applies).",
                reason_hi="घर 30 वर्ग मीटर से बड़ा है, लेकिन सरकारी योजना के तहत मिला है (छूट लागू)।",
            )
        if answers.house_from_govt_scheme is False:
            return RuleEvaluation(
                rule_id="PMUY-D10",
                passed=False,
                triggered=True,
                reason_en="Household owns a house with more than 30 sq metres carpet area (not from government scheme).",
                reason_hi="परिवार के पास 30 वर्ग मीटर से अधिक का पक्का मकान है (सरकारी योजना के बिना)।",
            )
        return RuleEvaluation(
            rule_id="PMUY-D10",
            passed=None,
            triggered=False,
            missing_field="house_from_govt_scheme",
            reason_en="Whether the house was received under a government scheme is unknown.",
            reason_hi="घर सरकारी योजना के तहत मिला है या नहीं, यह ज्ञात नहीं है।",
        )
    if answers.pucca_house_gt_30sqm is False:
        return RuleEvaluation(
            rule_id="PMUY-D10",
            passed=True,
            triggered=False,
            reason_en="Household does not own a house with > 30 sq metres carpet area.",
            reason_hi="परिवार के पास 30 वर्ग मीटर से अधिक का मकान नहीं है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D10",
        passed=None,
        triggered=False,
        missing_field="pucca_house_gt_30sqm",
        reason_en="House carpet area is unknown.",
        reason_hi="मकान के क्षेत्रफल की स्थिति ज्ञात नहीं है।",
    )


def check_d11_motorized_vehicle(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D11: Motorized three-/four-wheeler or fishing boat."""
    if answers.has_motorized_vehicle_or_boat is True:
        return RuleEvaluation(
            rule_id="PMUY-D11",
            passed=False,
            triggered=True,
            reason_en="Household owns a motorized three/four-wheeler or fishing boat.",
            reason_hi="परिवार के पास तिपहिया/चार पहिया मोटर वाहन या मछली पकड़ने की नाव है।",
        )
    if answers.has_motorized_vehicle_or_boat is False:
        return RuleEvaluation(
            rule_id="PMUY-D11",
            passed=True,
            triggered=False,
            reason_en="No motorized three/four-wheeler or boat.",
            reason_hi="परिवार के पास कोई मोटर वाहन या नाव नहीं है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D11",
        passed=None,
        triggered=False,
        missing_field="has_motorized_vehicle_or_boat",
        reason_en="Motorized vehicle ownership status is unknown.",
        reason_hi="वाहन स्वामित्व की स्थिति ज्ञात नहीं है।",
    )


def check_d12_mechanized_agri(answers: PMUYAnswers) -> RuleEvaluation:
    """PMUY-D12: Mechanized agricultural equipment."""
    if answers.has_mechanized_agri_equipment is True:
        return RuleEvaluation(
            rule_id="PMUY-D12",
            passed=False,
            triggered=True,
            reason_en="Household owns mechanized agricultural equipment.",
            reason_hi="परिवार के पास यंत्रीकृत कृषि उपकरण (ट्रैक्टर/हार्वेस्टर आदि) है।",
        )
    if answers.has_mechanized_agri_equipment is False:
        return RuleEvaluation(
            rule_id="PMUY-D12",
            passed=True,
            triggered=False,
            reason_en="No mechanized agricultural equipment.",
            reason_hi="परिवार के पास कोई यंत्रीकृत कृषि उपकरण नहीं है।",
        )
    return RuleEvaluation(
        rule_id="PMUY-D12",
        passed=None,
        triggered=False,
        missing_field="has_mechanized_agri_equipment",
        reason_en="Mechanized agricultural equipment status is unknown.",
        reason_hi="यंत्रीकृत कृषि उपकरण की स्थिति ज्ञात नहीं है।",
    )


# Ordered evaluation lists
PRIMARY_RULES: list[Callable[[PMUYAnswers], RuleEvaluation]] = [
    check_r01_woman,
    check_r02_age,
    check_r03_lpg,
    check_r05_citizenship,
    check_r06_png,
]

DEPRIVATION_RULES: list[Callable[[PMUYAnswers], RuleEvaluation]] = [
    check_d01_income,
    check_d02_professional_tax,
    check_d03_income_tax,
    check_d04_govt_employee,
    check_d05_registered_enterprise,
    check_d06_kcc_limit,
    check_d07_land_irrigated_2_5,
    check_d08_land_irrigated_5,
    check_d09_land_irrigated_7_5,
    check_d10_housing,
    check_d11_motorized_vehicle,
    check_d12_mechanized_agri,
]

