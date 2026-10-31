"""Conversational Answer Normalizer for PMUY eligibility interviews.

Owned by Anamika.

Purpose
-------
Convert raw user utterances — typed or transcribed speech — into the canonical
boolean values expected by the PMUY eligibility engine (``True``, ``False``, or
``None`` for unknown/uncertain).

Design constraints (from PMUY Knowledge Base §9 and DECISIONS.md D3)
---------------------------------------------------------------------
- Supported answer values per question bank: ``yes``, ``no``, ``not_sure``.
- Unknown or uncertain answers must NEVER be coerced to ``False`` (No).
- Missing, unclear, contradictory, or uncertain input must return ``None``
  so the engine can produce ``CANNOT_DETERMINE``, not a false pass.
- Hindi and English tokens are both accepted.
- Normalisation is purely lexical/heuristic; no LLM call is made here.
- The normalizer is stateless and deterministic.
- A raw age string (digits) is normalized to ``int`` for ``applicant_age``.
- No Aadhaar, bank account, or sensitive identifiers are processed here.

Output contract
---------------
``normalize_boolean(raw)`` → ``True | False | None``
``normalize_age(raw)`` → ``int | None``
``normalize_answer(raw, answer_type)`` → ``True | False | int | None``

This module has no dependency on the engine, question bank, or database.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Optional

# ---------------------------------------------------------------------------
# Token tables (English and Hindi)
# ---------------------------------------------------------------------------

# All tokens are lowercased, NFKC-normalised before matching.

_YES_TOKENS: frozenset[str] = frozenset(
    {
        # English affirmatives
        "yes",
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
        "i will",
        # Hindi affirmatives (Devanagari and common romanisations)
        "हाँ",
        "हां",
        "हाँ जी",
        "हां जी",
        "जी",
        "जी हाँ",
        "जी हां",
        "हा",
        "बिल्कुल",
        "ज़रूर",
        "ठीक है",
        "सही",
        "हाँ सही",
        "हां सही",
        # Romanised Hindi
        "haan",
        "han",
        "ha",
        "ji",
        "ji haan",
        "ji han",
        "bilkul",
        "zaroor",
        "sahi",
        "theek hai",
        "thik hai",
        "thik",
    }
)

_NO_TOKENS: frozenset[str] = frozenset(
    {
        # English negatives
        "no",
        "nope",
        "nah",
        "n",
        "not",
        "false",
        "negative",
        "no way",
        "definitely not",
        "absolutely not",
        "certainly not",
        "i don't",
        "i dont",
        "i do not",
        "i am not",
        "i have not",
        "i haven't",
        # Hindi negatives (Devanagari and common romanisations)
        "नहीं",
        "नही",
        "ना",
        "न",
        "जी नहीं",
        "जी नही",
        "नहीं जी",
        "नही जी",
        "बिल्कुल नहीं",
        "बिल्कुल नही",
        # Romanised Hindi
        "nahi",
        "nahin",
        "nahi ji",
        "nahin ji",
        "na",
        "bilkul nahi",
        "bilkul nahin",
    }
)

_UNSURE_TOKENS: frozenset[str] = frozenset(
    {
        # English uncertain
        "not sure",
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
        "don't know",
        "unknown",
        "not known",
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
        "i'll check",
        "skip",
        "pass",
        # Hindi uncertain (Devanagari)
        "पता नहीं",
        "पता नही",
        "मुझे नहीं पता",
        "मुझे नही पता",
        "मालूम नहीं",
        "मालूम नही",
        "शायद",
        "पक्का नहीं",
        "पक्का नही",
        "ठीक से नहीं पता",
        "ठीक से नही पता",
        "जाँचना पड़ेगा",
        # Romanised Hindi
        "pata nahi",
        "pata nahin",
        "mujhe nahi pata",
        "mujhe nahin pata",
        "malum nahi",
        "malum nahin",
        "shayad",
        "pakka nahi",
        "pakka nahin",
        "nahi pata",
    }
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_WHITESPACE_RE = re.compile(r"\s+")


def _clean(text: str) -> str:
    """NFKC-normalise, lowercase, and collapse whitespace."""
    text = unicodedata.normalize("NFKC", text)
    text = text.lower().strip()
    text = _WHITESPACE_RE.sub(" ", text)
    return text


def _strip_filler(text: str) -> str:
    """Remove common conversational fillers that do not change the meaning."""
    fillers = (
        "please",
        "bhai",
        "yaar",
        "please",
        "sir",
        "madam",
        "didi",
        "uh",
        "um",
        "hmm",
        "acha",
        "achha",
        "okay so",
        "well",
    )
    for filler in fillers:
        text = re.sub(r"\b" + re.escape(filler) + r"\b", " ", text)
    return _WHITESPACE_RE.sub(" ", text).strip()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def normalize_boolean(raw: str) -> Optional[bool]:
    """Normalise a raw conversational answer to ``True``, ``False``, or ``None``.

    ``None`` means the answer is unknown, unclear, or uncertain. It must NOT
    be interpreted as ``False`` by the caller.

    Parameters
    ----------
    raw:
        Raw text as received from the user (typed or speech-transcribed).

    Returns
    -------
    ``True``  — affirmative (Yes)
    ``False`` — negative (No)
    ``None``  — unknown / uncertain / not sure / skip
    """
    if not isinstance(raw, str):
        return None
    cleaned = _clean(raw)
    if not cleaned:
        return None
    stripped = _strip_filler(cleaned)
    if not stripped:
        return None

    # 1. Exact match against the full cleaned/stripped text
    if stripped in _UNSURE_TOKENS:
        return None
    if stripped in _YES_TOKENS:
        return True
    if stripped in _NO_TOKENS:
        return False

    # 2. Exact match against the original cleaned text (before filler removal)
    if cleaned in _UNSURE_TOKENS:
        return None
    if cleaned in _YES_TOKENS:
        return True
    if cleaned in _NO_TOKENS:
        return False

    # 3. Check for unsure sub-phrases first (to prevent "not sure" → False via "not")
    for token in sorted(_UNSURE_TOKENS, key=len, reverse=True):
        if token in stripped:
            return None

    # 4. Contradictory: text contains both affirmative and negative whole-word tokens
    #    → cannot determine (return None, not False)
    words = set(_WHITESPACE_RE.split(stripped))
    has_yes = any(
        (" " not in t and t in words) or (t == stripped)
        for t in _YES_TOKENS
    )
    has_no = any(
        (" " not in t and t in words) or (t == stripped)
        for t in _NO_TOKENS
    )
    if has_yes and has_no:
        return None

    # 5. Whole-word match for single-word yes/no tokens in stripped text
    # Check no tokens (whole word, e.g. "नहीं" or "no")
    for token in _NO_TOKENS:
        if " " not in token and token in words:
            return False
    # Check yes tokens (whole word)
    for token in _YES_TOKENS:
        if " " not in token and token in words:
            return True

    # 6. Heuristic: check whether the first meaningful word is affirmative/negative
    first_word = stripped.split()[0] if stripped else ""
    if first_word in _YES_TOKENS:
        return True
    if first_word in _NO_TOKENS:
        return False

    # 7. Cannot determine — return None (not False)
    return None


def normalize_age(raw: str) -> Optional[int]:
    """Extract an age integer from a raw string.

    Returns ``None`` if the string does not contain a valid non-negative integer.

    Parameters
    ----------
    raw:
        Raw text such as ``"25"``, ``"25 saal"``, ``"meri umar 32 hai"``.

    Returns
    -------
    Non-negative integer age, or ``None``.
    """
    if not isinstance(raw, str):
        return None
    # Find digit sequences not preceded by a minus sign (negative numbers → reject)
    # Strategy: find all occurrences of (optional sign)(digits), then skip negatives
    matches = re.findall(r"(?<!\d)-?\d+", raw.strip())
    if not matches:
        return None
    for match in matches:
        if match.startswith("-"):
            continue  # negative number — not a valid age
        try:
            age = int(match)
        except ValueError:
            continue
        if 0 <= age <= 120:
            return age
    return None


def normalize_answer(raw: str, answer_type: str) -> "Optional[bool | int]":
    """Dispatch normalization by ``answer_type``.

    Supported types
    ---------------
    ``"boolean"``
        Returns ``True``, ``False``, or ``None``.
    ``"integer"``
        Returns ``int`` or ``None`` (used for ``applicant_age``).

    Any other ``answer_type`` returns ``None`` without raising.

    Parameters
    ----------
    raw:
        Raw user utterance.
    answer_type:
        The ``answer_type`` field from the question definition (e.g. ``"boolean"``).

    Returns
    -------
    Normalised value or ``None``.
    """
    if answer_type == "boolean":
        return normalize_boolean(raw)
    if answer_type == "integer":
        return normalize_age(raw)
    return None


# ---------------------------------------------------------------------------
# Canonical token label (for question-bank display / LLM explanation use)
# ---------------------------------------------------------------------------

_CANONICAL_LABEL: dict[Optional[bool], str] = {
    True: "yes",
    False: "no",
    None: "not_sure",
}


def canonical_label(value: Optional[bool]) -> str:
    """Return the canonical ``allowed_values`` label for a normalised value.

    Matches the ``allowed_values`` field in the question bank:
    ``'yes'``, ``'no'``, ``'not_sure'``.
    """
    return _CANONICAL_LABEL.get(value, "not_sure")
