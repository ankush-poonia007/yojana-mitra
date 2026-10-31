"""Tests for backend/app/ingestion/models.py

Owned by Anamika.

Scope
-----
Tests the PROPOSED PMUYChunk and PMUYDocument Pydantic models in isolation.
No PDF extraction, no database, no network, no chunk-writing occurs here.

These tests verify:
- The model accepts correctly formed input.
- Required fields are enforced.
- to_retrieval_result() produces exactly the 7 §4.9 public fields.
- to_evidence_reference() produces exactly the 5 §4.5 public fields.
- No extra fields beyond the declared schema are accepted (extra='forbid').
- Provenance invariants: publication_date is nullable; retrieval_date is not.
- approved=False is the correct default state for unverified sources.
- The S04/S05 shared-PDF relationship is representable.

Status: PROPOSED model — tests will need re-running after H4 confirmation.
"""

import pytest
from pydantic import ValidationError

from app.ingestion.models import PMUYChunk, PMUYDocument


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def valid_chunk_s03() -> dict:
    """Minimal valid PMUYChunk dict for S03 (Deprivation Declaration, PDF)."""
    return {
        "scheme_id": "pmuy",
        "document_id": "pmuy-s03",
        "chunk_id": "pmuy-s03-p001-c000",
        "text": "Any household member earning more than Rs. 10,000 per month.",
        "source_url": "https://www.pmuy.gov.in/documents/Deprivation_Declaration_for_Poor_Households_English.pdf",
        "page": 1,
        "document_version": "S03-captured-2026-10-30",
        "title": "Deprivation Declaration for Poor Households",
        "section": "Exclusion Criteria",
        "retrieval_date": "2026-10-30",
        "publication_date": None,   # Explicitly null — no date visible in PDF
        "sha256": None,             # Null until file is downloaded
        "approved": False,          # S03 currency unconfirmed
        "sequence": 0,
    }


@pytest.fixture()
def valid_chunk_s01() -> dict:
    """Minimal valid PMUYChunk dict for S01 (HTML page)."""
    return {
        "scheme_id": "pmuy",
        "document_id": "pmuy-s01",
        "chunk_id": "pmuy-s01-sintroduction-c000",
        "text": "To provide deposit-free LPG connections to women from BPL households.",
        "source_url": "https://www.pmuy.gov.in/ujjwala2.html",
        "page": None,               # HTML source — no page number
        "document_version": "S01-captured-2026-10-30",
        "title": "Ujjwala 2.0 New Connection Page",
        "section": "Introduction",
        "retrieval_date": "2026-10-30",
        "publication_date": None,
        "sha256": None,
        "approved": False,
        "sequence": 0,
    }


@pytest.fixture()
def valid_chunk_s04() -> dict:
    """Minimal valid PMUYChunk dict for S04 (KYC PDF, Version 8.0)."""
    return {
        "scheme_id": "pmuy",
        "document_id": "pmuy-s04",
        "chunk_id": "pmuy-s04-p002-c001",
        "text": "The applicant must be an Indian citizen currently residing in India.",
        "source_url": "https://pmuy.gov.in/documents/Ujjwala-KYC_englishnew.pdf",
        "page": 2,
        "document_version": "KYC-V8.0",
        "title": "PMUY KYC Application Form — Version 8.0",
        "section": "Applicant Undertakings",
        "retrieval_date": "2026-10-30",
        "publication_date": None,
        "sha256": None,
        "approved": False,
        "sequence": 1,
    }


# ---------------------------------------------------------------------------
# ING-01: PMUYChunk model accepts valid input
# ---------------------------------------------------------------------------


class TestPMUYChunkConstruction:
    """ING-01: Valid PMUYChunk instances are accepted without error."""

    def test_construct_pdf_chunk(self, valid_chunk_s03):
        chunk = PMUYChunk(**valid_chunk_s03)
        assert chunk.scheme_id == "pmuy"
        assert chunk.document_id == "pmuy-s03"
        assert chunk.page == 1
        assert chunk.approved is False
        assert chunk.publication_date is None

    def test_construct_html_chunk_no_page(self, valid_chunk_s01):
        chunk = PMUYChunk(**valid_chunk_s01)
        assert chunk.page is None
        assert chunk.section == "Introduction"

    def test_construct_kyc_chunk(self, valid_chunk_s04):
        chunk = PMUYChunk(**valid_chunk_s04)
        assert chunk.document_version == "KYC-V8.0"
        assert chunk.sequence == 1


# ---------------------------------------------------------------------------
# ING-02: Required fields are enforced
# ---------------------------------------------------------------------------


class TestPMUYChunkRequiredFields:
    """ING-02: Missing required fields raise ValidationError."""

    @pytest.mark.parametrize(
        "missing_field",
        [
            "document_id",
            "chunk_id",
            "text",
            "source_url",
            "document_version",
            "title",
            "retrieval_date",
            "approved",
            "sequence",
        ],
    )
    def test_missing_required_field_raises(self, valid_chunk_s03, missing_field):
        data = dict(valid_chunk_s03)
        del data[missing_field]
        with pytest.raises(ValidationError):
            PMUYChunk(**data)

    def test_empty_text_raises(self, valid_chunk_s03):
        """text must be non-empty (min_length=1)."""
        data = dict(valid_chunk_s03)
        data["text"] = ""
        with pytest.raises(ValidationError):
            PMUYChunk(**data)

    def test_extra_field_raises(self, valid_chunk_s03):
        """extra='forbid' means unknown fields are rejected."""
        data = dict(valid_chunk_s03)
        data["unknown_field"] = "should_not_be_accepted"
        with pytest.raises(ValidationError):
            PMUYChunk(**data)


# ---------------------------------------------------------------------------
# ING-03: to_retrieval_result() matches §4.9 exactly
# ---------------------------------------------------------------------------


class TestRetrievalResultShape:
    """ING-03: to_retrieval_result() returns exactly the 7 §4.9 fields."""

    _EXPECTED_KEYS = {
        "scheme_id",
        "document_id",
        "chunk_id",
        "text",
        "source_url",
        "page",
        "document_version",
    }

    def test_pdf_chunk_retrieval_result_keys(self, valid_chunk_s03):
        chunk = PMUYChunk(**valid_chunk_s03)
        result = chunk.to_retrieval_result()
        assert set(result.keys()) == self._EXPECTED_KEYS

    def test_html_chunk_retrieval_result_keys(self, valid_chunk_s01):
        chunk = PMUYChunk(**valid_chunk_s01)
        result = chunk.to_retrieval_result()
        assert set(result.keys()) == self._EXPECTED_KEYS

    def test_retrieval_result_values(self, valid_chunk_s03):
        chunk = PMUYChunk(**valid_chunk_s03)
        result = chunk.to_retrieval_result()
        assert result["scheme_id"] == "pmuy"
        assert result["document_id"] == "pmuy-s03"
        assert result["chunk_id"] == "pmuy-s03-p001-c000"
        assert result["page"] == 1
        assert result["document_version"] == "S03-captured-2026-10-30"
        assert len(result["text"]) > 0

    def test_retrieval_result_does_not_contain_extended_fields(self, valid_chunk_s03):
        """Extended provenance fields must NOT appear in the public retrieval result."""
        chunk = PMUYChunk(**valid_chunk_s03)
        result = chunk.to_retrieval_result()
        for private_field in ("retrieval_date", "publication_date", "sha256", "approved", "sequence"):
            assert private_field not in result, (
                f"Private field {private_field!r} must not appear in §4.9 retrieval result"
            )

    def test_html_page_is_none_in_retrieval_result(self, valid_chunk_s01):
        chunk = PMUYChunk(**valid_chunk_s01)
        result = chunk.to_retrieval_result()
        assert result["page"] is None


# ---------------------------------------------------------------------------
# ING-04: to_evidence_reference() matches §4.5 exactly
# ---------------------------------------------------------------------------


class TestEvidenceReferenceShape:
    """ING-04: to_evidence_reference() returns exactly the 5 §4.5 fields."""

    _EXPECTED_KEYS = {"document_id", "title", "url", "page", "section"}

    def test_evidence_reference_keys(self, valid_chunk_s03):
        chunk = PMUYChunk(**valid_chunk_s03)
        ref = chunk.to_evidence_reference()
        assert set(ref.keys()) == self._EXPECTED_KEYS

    def test_evidence_reference_values(self, valid_chunk_s03):
        chunk = PMUYChunk(**valid_chunk_s03)
        ref = chunk.to_evidence_reference()
        assert ref["document_id"] == "pmuy-s03"
        assert ref["title"] == "Deprivation Declaration for Poor Households"
        assert ref["url"] == valid_chunk_s03["source_url"]
        assert ref["page"] == 1
        assert ref["section"] == "Exclusion Criteria"

    def test_evidence_reference_html_section_none(self):
        """Section is optional — None is valid."""
        chunk = PMUYChunk(
            scheme_id="pmuy",
            document_id="pmuy-s01",
            chunk_id="pmuy-s01-c000",
            text="Some text.",
            source_url="https://www.pmuy.gov.in/ujjwala2.html",
            page=None,
            document_version="S01-captured-2026-10-30",
            title="Ujjwala 2.0 New Connection Page",
            section=None,
            retrieval_date="2026-10-30",
            publication_date=None,
            sha256=None,
            approved=False,
            sequence=0,
        )
        ref = chunk.to_evidence_reference()
        assert ref["section"] is None


# ---------------------------------------------------------------------------
# ING-05: Provenance invariants
# ---------------------------------------------------------------------------


class TestProvenanceInvariants:
    """ING-05: Provenance fields behave correctly for unverified sources."""

    def test_approved_false_is_valid_for_unverified_source(self, valid_chunk_s03):
        """All S03 chunks must start with approved=False (currency unconfirmed)."""
        chunk = PMUYChunk(**valid_chunk_s03)
        assert chunk.approved is False

    def test_sha256_none_allowed_before_download(self, valid_chunk_s03):
        chunk = PMUYChunk(**valid_chunk_s03)
        assert chunk.sha256 is None

    def test_publication_date_none_allowed(self, valid_chunk_s03):
        """S03 has no visible publication date — None is the correct value."""
        chunk = PMUYChunk(**valid_chunk_s03)
        assert chunk.publication_date is None

    def test_retrieval_date_present(self, valid_chunk_s03):
        chunk = PMUYChunk(**valid_chunk_s03)
        assert chunk.retrieval_date == "2026-10-30"

    def test_retrieval_date_is_not_treated_as_publication_date(self, valid_chunk_s03):
        """Retrieval date and publication date are separate fields and must never be conflated."""
        chunk = PMUYChunk(**valid_chunk_s03)
        assert chunk.retrieval_date != chunk.publication_date or chunk.publication_date is None

    def test_negative_sequence_rejected(self, valid_chunk_s03):
        data = dict(valid_chunk_s03)
        data["sequence"] = -1
        with pytest.raises(ValidationError):
            PMUYChunk(**data)


# ---------------------------------------------------------------------------
# ING-06: S04/S05 shared-PDF relationship
# ---------------------------------------------------------------------------


class TestS04S05SharedPDF:
    """ING-06: S04 and S05 share the same URL; chunks must differ only by document_id."""

    def test_s04_and_s05_chunks_have_same_source_url(self, valid_chunk_s04):
        chunk_s04 = PMUYChunk(**valid_chunk_s04)
        chunk_s05 = PMUYChunk(
            scheme_id="pmuy",
            document_id="pmuy-s05",
            chunk_id="pmuy-s05-p003-c000",
            text="Migrant applicant self-declaration — Annexure I.",
            source_url="https://pmuy.gov.in/documents/Ujjwala-KYC_englishnew.pdf",
            page=3,
            document_version="KYC-V8.0",
            title="Migrant Self-Declaration / Annexure I",
            section="Annexure I",
            retrieval_date="2026-10-30",
            publication_date=None,
            sha256=None,
            approved=False,
            sequence=0,
        )
        assert chunk_s04.source_url == chunk_s05.source_url
        assert chunk_s04.document_id != chunk_s05.document_id

    def test_s04_and_s05_chunk_ids_are_distinct(self, valid_chunk_s04):
        chunk_s04 = PMUYChunk(**valid_chunk_s04)
        chunk_s05_id = "pmuy-s05-p003-c000"
        assert chunk_s04.chunk_id != chunk_s05_id


# ---------------------------------------------------------------------------
# ING-07: PMUYDocument model
# ---------------------------------------------------------------------------


class TestPMUYDocumentModel:
    """ING-07: PMUYDocument represents pre-ingestion source artifact metadata."""

    def test_construct_pdf_document(self):
        doc = PMUYDocument(
            source_id="pmuy-s03",
            short_name="Deprivation Declaration for Poor Households",
            url="https://www.pmuy.gov.in/documents/Deprivation_Declaration_for_Poor_Households_English.pdf",
            source_type="official_pdf",
            format="pdf",
            retrieval_date="2026-10-30",
            file_on_disk=None,
            sha256=None,
            form_version_in_document=None,
            approved=False,
            shares_file_with=None,
        )
        assert doc.approved is False
        assert doc.file_on_disk is None

    def test_construct_annexure_document_shares_file(self):
        doc = PMUYDocument(
            source_id="pmuy-s05",
            short_name="Migrant Self-Declaration / Annexure I",
            url="https://pmuy.gov.in/documents/Ujjwala-KYC_englishnew.pdf",
            source_type="official_pdf_annexure",
            format="pdf",
            retrieval_date="2026-10-30",
            file_on_disk=None,
            sha256=None,
            form_version_in_document="Version 8.0 (same file as pmuy-s04)",
            approved=False,
            shares_file_with="pmuy-s04",
        )
        assert doc.shares_file_with == "pmuy-s04"

    def test_extra_field_rejected(self):
        with pytest.raises(ValidationError):
            PMUYDocument(
                source_id="pmuy-s01",
                short_name="Test",
                url="https://example.gov.in",
                source_type="official_portal_page",
                format="html",
                retrieval_date="2026-10-30",
                approved=False,
                unexpected_field="should_fail",
            )


# ---------------------------------------------------------------------------
# ING-08: Stub guards — extractor and chunker must raise NotImplementedError
# ---------------------------------------------------------------------------


class TestStubGuards:
    """ING-08: Stub classes raise the correct not-implemented errors."""

    def test_extractor_pdf_raises(self):
        from app.ingestion.extractor import PMUYExtractor, PMUYExtractorNotImplemented
        from pathlib import Path
        with pytest.raises(PMUYExtractorNotImplemented):
            PMUYExtractor().extract_pdf(Path("fake.pdf"), "pmuy-s03")

    def test_extractor_html_raises(self):
        from app.ingestion.extractor import PMUYExtractor, PMUYExtractorNotImplemented
        from pathlib import Path
        with pytest.raises(PMUYExtractorNotImplemented):
            PMUYExtractor().extract_html(Path("fake.html"), "pmuy-s01")

    def test_chunker_raises(self):
        from app.ingestion.chunker import PMUYChunker, PMUYChunkerNotImplemented
        with pytest.raises(PMUYChunkerNotImplemented):
            PMUYChunker().chunk([], "pmuy-s03")

