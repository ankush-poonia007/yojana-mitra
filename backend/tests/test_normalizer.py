"""Tests for backend/app/eligibility/normalizer.py

Owned by Anamika.

Design principle
----------------
The normalizer MUST return None for any uncertain/unknown input.
None must NEVER be coerced to False by the normalizer itself.

All tests use parametrize for clarity and coverage.
"""

import pytest
from app.eligibility.normalizer import (
    canonical_label,
    normalize_age,
    normalize_answer,
    normalize_boolean,
)


# ===========================================================================
# NRM-B: Boolean normalization — English affirmatives
# ===========================================================================


class TestEnglishAffirmatives:
    """English Yes tokens → True."""

    @pytest.mark.parametrize(
        "raw",
        [
            "yes",
            "Yes",
            "YES",
            "yeah",
            "yep",
            "yup",
            "y",
            "ok",
            "okay",
            "sure",
            "correct",
            "right",
            "true",
            "affirmative",
            "of course",
            "definitely",
            "absolutely",
            "certainly",
            "indeed",
            "agreed",
            "i do",
            "i am",
            "i have",
        ],
    )
    def test_english_yes_tokens(self, raw):
        assert normalize_boolean(raw) is True, f"Expected True for {raw!r}"


# ===========================================================================
# NRM-C: Boolean normalization — English negatives
# ===========================================================================


class TestEnglishNegatives:
    """English No tokens → False."""

    @pytest.mark.parametrize(
        "raw",
        [
            "no",
            "No",
            "NO",
            "nope",
            "nah",
            "false",
            "negative",
            "no way",
            "definitely not",
            "i don't",
            "i dont",
            "i do not",
            "i am not",
        ],
    )
    def test_english_no_tokens(self, raw):
        assert normalize_boolean(raw) is False, f"Expected False for {raw!r}"


# ===========================================================================
# NRM-D: Boolean normalization — Hindi affirmatives
# ===========================================================================


class TestHindiAffirmatives:
    """Hindi Yes tokens → True (Devanagari and romanised)."""

    @pytest.mark.parametrize(
        "raw",
        [
            "हाँ",
            "हां",
            "जी",
            "जी हाँ",
            "जी हां",
            "बिल्कुल",
            "ज़रूर",
            "haan",
            "han",
            "ji",
            "ji haan",
            "bilkul",
            "zaroor",
            "theek hai",
            "sahi",
        ],
    )
    def test_hindi_yes_tokens(self, raw):
        assert normalize_boolean(raw) is True, f"Expected True for {raw!r}"


# ===========================================================================
# NRM-E: Boolean normalization — Hindi negatives
# ===========================================================================


class TestHindiNegatives:
    """Hindi No tokens → False (Devanagari and romanised)."""

    @pytest.mark.parametrize(
        "raw",
        [
            "नहीं",
            "नही",
            "ना",
            "जी नहीं",
            "जी नही",
            "बिल्कुल नहीं",
            "nahi",
            "nahin",
            "nahi ji",
            "na",
            "bilkul nahi",
        ],
    )
    def test_hindi_no_tokens(self, raw):
        assert normalize_boolean(raw) is False, f"Expected False for {raw!r}"


# ===========================================================================
# NRM-U: Uncertain / not-sure inputs → None
# ===========================================================================


class TestUncertainInputs:
    """Critical: uncertain answers must return None, NOT False."""

    @pytest.mark.parametrize(
        "raw",
        [
            "not sure",
            "Not Sure",
            "NOT SURE",
            "unsure",
            "i'm not sure",
            "im not sure",
            "i am not sure",
            "don't know",
            "dont know",
            "do not know",
            "i don't know",
            "i dont know",
            "i do not know",
            "unknown",
            "unclear",
            "maybe",
            "perhaps",
            "might",
            "possibly",
            "not certain",
            "no idea",
            "can't say",
            "cant say",
            "cannot say",
            "hard to say",
            "i need to check",
            "need to check",
            "let me check",
            "will check",
            "skip",
            "pass",
            # Hindi uncertain
            "पता नहीं",
            "पता नही",
            "मुझे नहीं पता",
            "शायद",
            "पक्का नहीं",
            "pata nahi",
            "pata nahin",
            "shayad",
            "pakka nahi",
            "nahi pata",
            "malum nahi",
        ],
    )
    def test_uncertain_returns_none(self, raw):
        result = normalize_boolean(raw)
        assert result is None, (
            f"CRITICAL: uncertain input {raw!r} returned {result!r}; "
            "must return None to prevent false eligibility pass"
        )


# ===========================================================================
# NRM-F: Edge inputs that must not crash or return wrong value
# ===========================================================================


class TestEdgeCases:
    """Empty, whitespace, numeric, None → None."""

    @pytest.mark.parametrize(
        "raw",
        [
            "",
            "   ",
            "\t\n",
            "???",
            "...",
            "1",
            "0",
            "true false",     # contradictory — cannot determine
        ],
    )
    def test_edge_returns_none(self, raw):
        assert normalize_boolean(raw) is None, f"Expected None for {raw!r}"

    def test_none_input_returns_none(self):
        # None-typed input should not crash
        assert normalize_boolean(None) is None  # type: ignore[arg-type]

    def test_integer_input_returns_none(self):
        assert normalize_boolean(42) is None  # type: ignore[arg-type]


# ===========================================================================
# NRM-G: Case and whitespace insensitivity
# ===========================================================================


class TestCaseAndWhitespace:
    """Normalizer must ignore case and extra whitespace."""

    def test_uppercase_yes(self):
        assert normalize_boolean("YES") is True

    def test_mixed_case_no(self):
        assert normalize_boolean("No") is False

    def test_leading_trailing_space(self):
        assert normalize_boolean("  yes  ") is True

    def test_extra_internal_space(self):
        assert normalize_boolean("not   sure") is None

    def test_tab_separated(self):
        assert normalize_boolean("\tno\t") is False


# ===========================================================================
# NRM-H: Filler word stripping
# ===========================================================================


class TestFillerStripping:
    """Common conversational fillers are ignored."""

    def test_yes_with_please(self):
        assert normalize_boolean("yes please") is True

    def test_no_with_bhai(self):
        assert normalize_boolean("no bhai") is False

    def test_haan_with_ji(self):
        # "ji" alone is a YES token, but here it appears after haan
        assert normalize_boolean("haan ji") is True


# ===========================================================================
# NRM-I: Not-sure MUST NOT collapse to False
# ===========================================================================


class TestNotSureNotFalse:
    """Regression: 'not sure' contains 'not' but must not resolve to False."""

    def test_not_sure_is_not_false(self):
        result = normalize_boolean("not sure")
        assert result is not False, "'not sure' must never return False"
        assert result is None

    def test_not_certain_is_not_false(self):
        result = normalize_boolean("not certain")
        assert result is not False
        assert result is None

    def test_i_am_not_sure_is_none(self):
        result = normalize_boolean("i am not sure")
        assert result is None


# ===========================================================================
# NRM-J: Age normalization
# ===========================================================================


class TestAgeNormalization:
    """normalize_age extracts non-negative integer from conversational text."""

    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("25", 25),
            ("18", 18),
            ("0", 0),
            ("120", 120),
            ("25 saal", 25),
            ("meri umar 32 hai", 32),
            ("I am 40 years old", 40),
            ("  17  ", 17),
        ],
    )
    def test_valid_ages(self, raw, expected):
        assert normalize_age(raw) == expected

    @pytest.mark.parametrize(
        "raw",
        [
            "",
            "   ",
            "yes",
            "nahi",
            "not sure",
            "abcd",
            "121",     # > 120 — implausible
            "-5",      # negative — no digit found after strip
        ],
    )
    def test_invalid_age_returns_none(self, raw):
        result = normalize_age(raw)
        assert result is None, f"Expected None for age input {raw!r}, got {result!r}"

    def test_none_input_returns_none(self):
        assert normalize_age(None) is None  # type: ignore[arg-type]


# ===========================================================================
# NRM-K: normalize_answer dispatcher
# ===========================================================================


class TestNormalizeAnswerDispatcher:
    """normalize_answer dispatches by answer_type."""

    def test_boolean_yes(self):
        assert normalize_answer("yes", "boolean") is True

    def test_boolean_no(self):
        assert normalize_answer("no", "boolean") is False

    def test_boolean_not_sure(self):
        assert normalize_answer("not sure", "boolean") is None

    def test_integer_age(self):
        assert normalize_answer("25", "integer") == 25

    def test_integer_invalid(self):
        assert normalize_answer("pata nahi", "integer") is None

    def test_unknown_type_returns_none(self):
        assert normalize_answer("yes", "freetext") is None

    def test_unknown_type_does_not_raise(self):
        # Must never raise
        result = normalize_answer("anything", "unsupported_type")
        assert result is None


# ===========================================================================
# NRM-L: canonical_label round-trip
# ===========================================================================


class TestCanonicalLabel:
    """canonical_label maps normalised values to question-bank allowed_values."""

    def test_true_is_yes(self):
        assert canonical_label(True) == "yes"

    def test_false_is_no(self):
        assert canonical_label(False) == "no"

    def test_none_is_not_sure(self):
        assert canonical_label(None) == "not_sure"

    def test_round_trip_yes(self):
        assert canonical_label(normalize_boolean("yes")) == "yes"

    def test_round_trip_no(self):
        assert canonical_label(normalize_boolean("nahi")) == "no"

    def test_round_trip_not_sure(self):
        assert canonical_label(normalize_boolean("shayad")) == "not_sure"

    @pytest.mark.parametrize(
        "raw, expected_label",
        [
            ("हाँ", "yes"),
            ("नहीं", "no"),
            ("पता नहीं", "not_sure"),
            ("haan", "yes"),
            ("nahi", "no"),
            ("pata nahi", "not_sure"),
        ],
    )
    def test_hindi_round_trips(self, raw, expected_label):
        assert canonical_label(normalize_boolean(raw)) == expected_label


# ===========================================================================
# NRM-M: PMUYAnswers field compatibility
# ===========================================================================


class TestPMUYAnswersCompatibility:
    """Normalizer output must be accepted by PMUYAnswers without error."""

    def test_boolean_true_accepted_by_pmuy_answers(self):
        from app.eligibility.models import PMUYAnswers

        answers = PMUYAnswers(applicant_is_woman=normalize_boolean("yes"))
        assert answers.applicant_is_woman is True

    def test_boolean_false_accepted(self):
        from app.eligibility.models import PMUYAnswers

        answers = PMUYAnswers(applicant_is_woman=normalize_boolean("no"))
        assert answers.applicant_is_woman is False

    def test_none_accepted_for_optional_field(self):
        from app.eligibility.models import PMUYAnswers

        answers = PMUYAnswers(applicant_is_woman=normalize_boolean("not sure"))
        assert answers.applicant_is_woman is None

    def test_none_from_uncertain_not_treated_as_false_by_engine(self):
        """Critical integration check: None in → CANNOT_DETERMINE out."""
        from app.eligibility.engine import evaluate_pmuy_eligibility
        from app.eligibility.models import PMUYAnswers

        # Provide only one field; everything else unknown
        raw_answers = PMUYAnswers(
            applicant_is_woman=normalize_boolean("not sure")
        )
        result = evaluate_pmuy_eligibility(raw_answers)
        # Must be CANNOT_DETERMINE, not LIKELY_NOT_ELIGIBLE
        assert result.result.value == "cannot_determine", (
            "None input from normalizer must not produce LIKELY_NOT_ELIGIBLE"
        )

