"""Pydantic data models and enums for PMUY deterministic eligibility assessment.

Owned by Anamika.
Conforms to frozen Phase 3.3 / Phase 4.1 schemas in shared/api-contract.md.
"""

from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class EligibilityResult(str, Enum):
    """Frozen eligibility evaluation outcome values (shared/api-contract.md §4.4)."""

    LIKELY_ELIGIBLE = "likely_eligible"
    LIKELY_NOT_ELIGIBLE = "likely_not_eligible"
    CANNOT_DETERMINE = "cannot_determine"


class VerificationStatus(str, Enum):
    """Official verification status dimension (PMUY Knowledge Base §8)."""

    REQUIRED = "REQUIRED"
    PENDING = "PENDING"
    NOT_STARTED = "NOT_STARTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ReadinessStatus(str, Enum):
    """Application and document readiness dimension (PMUY Knowledge Base §8)."""

    READY_TO_PREPARE = "READY_TO_PREPARE"
    DOCUMENTS_INCOMPLETE = "DOCUMENTS_INCOMPLETE"
    NEEDS_DISTRIBUTOR_GUIDANCE = "NEEDS_DISTRIBUTOR_GUIDANCE"
    UNKNOWN = "UNKNOWN"


class RuleEvaluation(BaseModel):
    """Outcome of evaluating a single PMUY eligibility rule or deprivation criterion."""

    rule_id: str
    passed: Optional[bool] = None
    triggered: bool = False
    reason_en: str = ""
    reason_hi: str = ""
    missing_field: Optional[str] = None


class PMUYAnswers(BaseModel):
    """Normalized user answers for PMUY 2.0 eligibility evaluation.

    Supports optional values (None = unknown/unanswered).
    Extra fields are ignored to tolerate workflow metadata pass-through.
    """

    model_config = ConfigDict(extra="ignore")

    # Stage 1: Mandatory Applicant Conditions (R01, R02, R05)
    applies_in_own_name: Optional[bool] = None  # Q01 — applicant applying in own name
    applicant_is_woman: Optional[bool] = None
    applicant_age: Optional[int] = Field(default=None, ge=0, le=120)
    age_18_or_above: Optional[bool] = None
    citizen_and_resident: Optional[bool] = None

    # Stage 2: Household & Connections (R03, R06, D13)
    household_has_lpg: Optional[bool] = None
    dwelling_has_png: Optional[bool] = None

    # Stage 3: Deprivation Declaration Criteria D01 - D12 (R04)
    poor_household_declaration: Optional[bool] = None  # Composite R04 declaration
    member_earns_above_10k: Optional[bool] = None  # D01
    pays_professional_tax: Optional[bool] = None   # D02
    pays_income_tax: Optional[bool] = None         # D03
    is_govt_employee: Optional[bool] = None        # D04
    has_registered_enterprise: Optional[bool] = None  # D05
    kcc_limit_above_50k: Optional[bool] = None     # D06
    land_gt_2_5_acres_irrigated: Optional[bool] = None  # D07
    land_gte_5_acres_irrigated_2seasons: Optional[bool] = None  # D08
    land_gte_7_5_acres_irrigated: Optional[bool] = None  # D09
    pucca_house_gt_30sqm: Optional[bool] = None    # D10
    house_from_govt_scheme: Optional[bool] = False  # D10 exception
    has_motorized_vehicle_or_boat: Optional[bool] = None  # D11
    has_mechanized_agri_equipment: Optional[bool] = None  # D12

    # Stage 4: Application Readiness & Verification Attributes (R07)
    has_ration_card: Optional[bool] = None
    has_alternative_family_doc: Optional[bool] = None
    has_bank_account: Optional[bool] = None
    adult_members_aadhaar_available: Optional[bool] = None
    is_migrant: Optional[bool] = None
    family_split_dispute: Optional[bool] = None
    biometric_authenticated: Optional[bool] = None

    # Internal contradiction tracking
    age_contradiction: bool = False

    @model_validator(mode="before")
    @classmethod
    def sync_and_validate_age(cls, values: Any) -> Any:
        """Synchronize applicant_age and age_18_or_above and detect contradictions."""
        if isinstance(values, dict):
            age = values.get("applicant_age")
            age_18 = values.get("age_18_or_above")
            if age is not None and age_18 is not None:
                try:
                    is_adult = int(age) >= 18
                    if is_adult != bool(age_18):
                        values["age_contradiction"] = True
                except (ValueError, TypeError):
                    pass
            elif age is not None and age_18 is None:
                try:
                    values["age_18_or_above"] = int(age) >= 18
                except (ValueError, TypeError):
                    pass
        return values


class PMUYAssessmentResult(BaseModel):
    """Result of PMUY deterministic eligibility assessment.

    Matches shared/api-contract.md §4.4, enriched with verification and readiness.
    """

    model_config = ConfigDict(extra="ignore")

    scheme_id: str = "pmuy"
    result: EligibilityResult
    reasons: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    triggered_rules: list[str] = Field(default_factory=list)
    passed_rules: list[str] = Field(default_factory=list)
    verification_status: VerificationStatus = VerificationStatus.REQUIRED
    readiness_status: ReadinessStatus = ReadinessStatus.UNKNOWN

    def to_api_assessment(self) -> dict[str, Any]:
        """Strict 4-field contract dictionary for public API (shared/api-contract.md §4.4)."""
        return {
            "scheme_id": self.scheme_id,
            "result": self.result.value,
            "reasons": self.reasons,
            "missing_information": self.missing_information,
        }

    def to_workflow_context(self) -> dict[str, Any]:
        """Complete dictionary including verification and readiness for LangGraph workflow."""
        return self.model_dump()
