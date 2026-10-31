"""Unit tests for PMUY Question Bank and Four-Stage Interview Navigator.

Owned by Anamika.
Verifies question uniqueness, stage sequencing, field mapping, language availability,
dimension isolation, and dynamic interview progression.
"""

import re
from pathlib import Path
import pytest

from app.eligibility.models import PMUYAnswers
from app.eligibility.question_bank import QuestionBank, QuestionDefinition


@pytest.fixture
def question_bank() -> QuestionBank:
    """Fixture providing a loaded QuestionBank instance."""
    return QuestionBank()


def test_question_bank_initialization(question_bank: QuestionBank):
    """Test QuestionBank initializes and loads all 21 questions."""
    questions = question_bank.get_all_questions()
    assert len(questions) == 21
    assert isinstance(questions[0], QuestionDefinition)


def test_question_bank_invalid_path_raises():
    """Test QuestionBank raises FileNotFoundError when given a non-existent path."""
    with pytest.raises(FileNotFoundError):
        QuestionBank(data_path="invalid/path/to/nowhere.json")


def test_question_uniqueness(question_bank: QuestionBank):
    """Test all question IDs and orders are strictly unique."""
    questions = question_bank.get_all_questions()

    question_ids = [q.question_id for q in questions]
    assert len(question_ids) == len(set(question_ids)), "Duplicate question_id found"

    # Verify ID format (PMUY-Q01 to PMUY-Q21)
    id_pattern = re.compile(r"^PMUY-Q(0[1-9]|1[0-9]|2[0-1])$")
    for qid in question_ids:
        assert id_pattern.match(qid), f"Invalid question ID format: {qid}"

    orders = [q.order for q in questions]
    assert len(orders) == len(set(orders)), "Duplicate question order found"
    assert orders == list(range(1, 22)), "Question orders must be contiguous 1..21"


def test_stage_sequencing(question_bank: QuestionBank):
    """Test questions are properly partitioned and ordered across Stages 1 to 4."""
    s1 = question_bank.get_stage_questions(1)
    s2 = question_bank.get_stage_questions(2)
    s3 = question_bank.get_stage_questions(3)
    s4 = question_bank.get_stage_questions(4)

    assert len(s1) == 4, "Stage 1 must contain 4 questions (Q01-Q04)"
    assert [q.question_id for q in s1] == ["PMUY-Q01", "PMUY-Q02", "PMUY-Q03", "PMUY-Q04"]
    assert all(q.stage_name == "applicant" for q in s1)

    assert len(s2) == 2, "Stage 2 must contain 2 questions (Q05-Q06)"
    assert [q.question_id for q in s2] == ["PMUY-Q05", "PMUY-Q06"]
    assert all(q.stage_name == "household" for q in s2)

    assert len(s3) == 12, "Stage 3 must contain 12 questions (Q07-Q18)"
    assert [q.question_id for q in s3] == [f"PMUY-Q{i:02d}" for i in range(7, 19)]
    assert all(q.stage_name == "deprivation" for q in s3)

    assert len(s4) == 3, "Stage 4 must contain 3 questions (Q19-Q21)"
    assert [q.question_id for q in s4] == ["PMUY-Q19", "PMUY-Q20", "PMUY-Q21"]
    assert all(q.stage_name == "readiness" for q in s4)

    assert question_bank.get_stage_questions(99) == []


def test_language_availability_and_localization(question_bank: QuestionBank):
    """Test bilingual text availability and localization methods."""
    for q in question_bank.get_all_questions():
        assert q.text_en.strip(), f"{q.question_id} missing English text"
        assert q.text_hi.strip(), f"{q.question_id} missing Hindi text"
        assert q.help_text_en.strip(), f"{q.question_id} missing English help text"
        assert q.help_text_hi.strip(), f"{q.question_id} missing Hindi help text"

        # Check localization method output
        assert q.get_text("en") == q.text_en
        assert q.get_text("hi") == q.text_hi
        assert q.get_text("Hindi") == q.text_hi
        assert q.get_text("unknown") == q.text_en

        assert q.get_help_text("en") == q.help_text_en
        assert q.get_help_text("hi") == q.help_text_hi

        # Ensure no corrupt unicode replacement characters
        assert "\ufffd" not in q.text_hi
        assert "\ufffd" not in q.help_text_hi


def test_field_mapping_to_pmuy_answers(question_bank: QuestionBank):
    """Test that question engine fields bind cleanly to PMUYAnswers."""
    questions = question_bank.get_all_questions()

    # All eligibility/readiness questions (Q02-Q21) map to defined PMUYAnswers model fields
    for q in questions:
        assert q.engine_field is not None, f"{q.question_id} missing engine_field"
        if q.question_id != "PMUY-Q01":
            assert q.engine_field in PMUYAnswers.model_fields, (
                f"{q.question_id} engine_field '{q.engine_field}' not found in PMUYAnswers"
            )

    # Q01 is applicant context binding
    q01 = question_bank.get_question("PMUY-Q01")
    assert q01.engine_field == "applies_in_own_name"

    # Verify PMUYAnswers accepts all fields as dictionary payload without crashing
    all_fields_payload = {q.engine_field: True for q in questions}
    answers = PMUYAnswers(**all_fields_payload)
    assert answers.applicant_is_woman is True
    assert answers.household_has_lpg is True


def test_dimension_and_metadata_separation(question_bank: QuestionBank):
    """Test dimensions, answer types, and mandatory flags match approved plan."""
    for q in question_bank.get_all_questions():
        assert q.answer_type in {"boolean", "integer", "choice"}
        assert len(q.allowed_values) > 0

        if q.stage in {1, 2, 3}:
            assert q.dimension == "eligibility"
        elif q.stage == 4:
            assert q.dimension == "readiness"

    # Mandatory flag assertions
    assert question_bank.get_question("PMUY-Q01").is_mandatory is False
    assert question_bank.get_question("PMUY-Q02").is_mandatory is True
    assert question_bank.get_question("PMUY-Q03").is_mandatory is True
    assert question_bank.get_question("PMUY-Q04").is_mandatory is True
    assert question_bank.get_question("PMUY-Q05").is_mandatory is True
    assert question_bank.get_question("PMUY-Q06").is_mandatory is True
    assert question_bank.get_question("PMUY-Q19").is_mandatory is True
    assert question_bank.get_question("PMUY-Q20").is_mandatory is True


def test_exclusion_trigger_specification(question_bank: QuestionBank):
    """Test exclusion trigger polarity across questions."""
    # Stage 1: Disqualifying on 'No' (is_exclusion_trigger_on is False)
    assert question_bank.get_question("PMUY-Q02").is_exclusion_trigger_on is False
    assert question_bank.get_question("PMUY-Q03").is_exclusion_trigger_on is False
    assert question_bank.get_question("PMUY-Q04").is_exclusion_trigger_on is False

    # Stage 2: Disqualifying on 'Yes' (is_exclusion_trigger_on is True)
    assert question_bank.get_question("PMUY-Q05").is_exclusion_trigger_on is True
    assert question_bank.get_question("PMUY-Q06").is_exclusion_trigger_on is True

    # Stage 3: All 12 deprivation criteria disqualify on 'Yes'
    for q in question_bank.get_stage_questions(3):
        assert q.is_exclusion_trigger_on is True, f"{q.question_id} must trigger exclusion on Yes"


def test_get_question_by_id(question_bank: QuestionBank):
    """Test lookup by question ID."""
    q1 = question_bank.get_question("PMUY-Q01")
    assert q1 is not None
    assert q1.question_id == "PMUY-Q01"

    q21 = question_bank.get_question("PMUY-Q21")
    assert q21 is not None
    assert q21.question_id == "PMUY-Q21"

    assert question_bank.get_question("NON-EXISTENT") is None


def test_get_next_question_progression(question_bank: QuestionBank):
    """Test step-by-step interview progression from Stage 1 through Stage 4."""
    # Initially, interview starts with Q01
    answers = {}
    next_q = question_bank.get_next_question(answers)
    assert next_q is not None
    assert next_q.question_id == "PMUY-Q01"

    # User answers Q01 -> Q02
    answers["applies_in_own_name"] = True
    next_q = question_bank.get_next_question(answers)
    assert next_q.question_id == "PMUY-Q02"

    # User answers Q02 -> Q03
    answers["applicant_is_woman"] = True
    next_q = question_bank.get_next_question(answers)
    assert next_q.question_id == "PMUY-Q03"

    # User answers Q03 with integer age 28 -> advances to Q04
    answers["applicant_age"] = 28
    next_q = question_bank.get_next_question(answers)
    assert next_q.question_id == "PMUY-Q04"

    # User completes Stage 1 -> moves to Stage 2 (Q05)
    answers["citizen_and_resident"] = True
    next_q = question_bank.get_next_question(answers)
    assert next_q.question_id == "PMUY-Q05"

    # User completes Stage 2 without exclusions -> moves to Stage 3 (Q07)
    answers["household_has_lpg"] = False
    answers["dwelling_has_png"] = False
    next_q = question_bank.get_next_question(answers)
    assert next_q.question_id == "PMUY-Q07"

    # User answers all Stage 3 questions as False (no deprivation exclusions)
    for q in question_bank.get_stage_questions(3):
        answers[q.engine_field] = False
    next_q = question_bank.get_next_question(answers)
    assert next_q.question_id == "PMUY-Q19"  # Moves to Stage 4

    # User completes Stage 4
    answers["has_ration_card"] = True
    answers["has_bank_account"] = True
    answers["adult_members_aadhaar_available"] = True
    next_q = question_bank.get_next_question(answers)
    assert next_q is None, "Interview must be complete when all questions answered"


def test_get_next_question_early_exclusion_exit(question_bank: QuestionBank):
    """Test early termination when hard exclusion criteria are triggered."""
    # Stage 1 exclusion: applicant is not a woman
    disqualified_stage1 = {
        "applies_in_own_name": True,
        "applicant_is_woman": False,
    }
    assert question_bank.get_next_question(disqualified_stage1) is None
    # When stop_on_exclusion=False, interview continues
    assert question_bank.get_next_question(
        disqualified_stage1, stop_on_exclusion=False
    ).question_id == "PMUY-Q03"

    # Stage 1 exclusion: applicant is underage (age 16)
    disqualified_age = {
        "applies_in_own_name": True,
        "applicant_is_woman": True,
        "applicant_age": 16,
    }
    assert question_bank.get_next_question(disqualified_age) is None

    # Stage 2 exclusion: household already has LPG
    disqualified_lpg = {
        "applies_in_own_name": True,
        "applicant_is_woman": True,
        "age_18_or_above": True,
        "citizen_and_resident": True,
        "household_has_lpg": True,
    }
    assert question_bank.get_next_question(disqualified_lpg) is None

    # Stage 2 exclusion: dwelling has PNG
    disqualified_png = {
        "applies_in_own_name": True,
        "applicant_is_woman": True,
        "age_18_or_above": True,
        "citizen_and_resident": True,
        "household_has_lpg": False,
        "dwelling_has_png": True,
    }
    assert question_bank.get_next_question(disqualified_png) is None

    # Stage 3 exclusion: member earns > 10k
    disqualified_stage3 = {
        "applies_in_own_name": True,
        "applicant_is_woman": True,
        "age_18_or_above": True,
        "citizen_and_resident": True,
        "household_has_lpg": False,
        "dwelling_has_png": False,
        "member_earns_above_10k": True,
    }
    assert question_bank.get_next_question(disqualified_stage3) is None


def test_pmuy_answers_model_input_compatibility(question_bank: QuestionBank):
    """Test passing PMUYAnswers instance directly to get_next_question."""
    model_input = PMUYAnswers(
        applicant_is_woman=True,
        age_18_or_above=True,
        citizen_and_resident=True,
    )
    # Q01 is unanswered because applies_in_own_name was not provided
    next_q = question_bank.get_next_question(model_input)
    assert next_q.question_id == "PMUY-Q01"

