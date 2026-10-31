"""Proposed PMUY ingestion data models.

Owned by Anamika.

⚠ PROPOSED — Schema is locked to shared/api-contract.md §4.9 and §4.5.
   It must be confirmed with Ankush (H4 contract) before any chunk is
   written to data/extracted/pmuy_chunks.jsonl or the database.
   Do not change eligibility rules, shared contracts, or Ankush's files.

Contract anchors
----------------
shared/api-contract.md §4.9 — Retrieval result (7 public fields):
    scheme_id, document_id, chunk_id, text, source_url, page,
    document_version

shared/api-contract.md §4.5 — Evidence reference (5 public fields):
    document_id, title, url, page, section

OPEN items that require H4 confirmation before implementation:
    - Exact chunk_id format convention
    - Whether embeddings are stored in this model or computed by Ankush
    - pgvector table DDL and field names
    - Whether output is JSONL, a service call, or another format
    - How to represent unverified source currency in the stored metadata
    - How extraction failures and empty chunks are handled
    - Deduplication behavior for the shared S04/S05 PDF
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PMUYChunk(BaseModel):
    """A single extracted text chunk from an official PMUY source document.

    Fields are derived from shared/api-contract.md §4.9 (retrieval result)
    and augmented with provenance metadata required by DECISIONS.md D12
    (preserve source IDs, page/section, version, retrieval date).

    ⚠ PROPOSED — field names and types must be confirmed via H4 contract.
    """

    model_config = ConfigDict(extra="forbid")

    # --- Public retrieval fields (§4.9) ---
    scheme_id: str = Field(
        default="pmuy",
        description="Scheme identifier. Fixed to 'pmuy' for all PMUY sources.",
    )
    document_id: str = Field(
        description=(
            "Stable document identifier. Proposed convention: "
            "'pmuy-s01', 'pmuy-s02', 'pmuy-s03', 'pmuy-s04', 'pmuy-s05'. "
            "OPEN: confirm with Ankush whether this matches the DB primary key."
        )
    )
    chunk_id: str = Field(
        description=(
            "Stable, deterministic chunk identifier. Proposed convention: "
            "'{document_id}-p{page:03d}-c{sequence:03d}' for PDF pages, "
            "'{document_id}-s{section_slug}-c{sequence:03d}' for HTML sections. "
            "OPEN: confirm format with Ankush."
        )
    )
    text: str = Field(
        description="Non-empty extracted text passage from the source document.",
        min_length=1,
    )
    source_url: str = Field(
        description="Canonical URL of the source document (from source_manifest.json).",
    )
    page: Optional[int] = Field(
        default=None,
        description=(
            "1-based page number for PDF sources; null for HTML sources. "
            "Matches §4.9 and §4.5 field name."
        ),
    )
    document_version: str = Field(
        description=(
            "Human-readable version or capture label. Examples: "
            "'KYC-V8.0', 'S03-captured-2026-10-30'. "
            "OPEN: confirm whether this must match a DB column exactly."
        )
    )

    # --- Extended provenance metadata (§4.5 + DECISIONS.md D12) ---
    title: str = Field(
        description="Document short name as recorded in source_manifest.json.",
    )
    section: Optional[str] = Field(
        default=None,
        description=(
            "Section heading or identifier within the document. "
            "Matches §4.5 'section' field."
        ),
    )
    retrieval_date: str = Field(
        description=(
            "ISO 8601 date the source was retrieved from the official URL. "
            "Format: 'YYYY-MM-DD'. Must not be confused with publication date."
        )
    )
    publication_date: Optional[str] = Field(
        default=None,
        description=(
            "Publication or revision date of the source document, "
            "if stated in the document. Null if not visible. "
            "Must NOT be inferred from retrieval_date."
        ),
    )
    sha256: Optional[str] = Field(
        default=None,
        description=(
            "SHA-256 hex digest of the downloaded source file. "
            "Required before ingestion is marked complete. Null until computed."
        ),
    )
    approved: bool = Field(
        description=(
            "True only if this chunk's source has passed all currency and "
            "provenance checks required by the source manifest open items. "
            "Must default to False for S03 until distributor/OMC confirms "
            "the declaration version."
        )
    )

    # --- Internal tracking ---
    sequence: int = Field(
        description="0-based sequence number of this chunk within its document.",
        ge=0,
    )

    def to_retrieval_result(self) -> dict:
        """Return the §4.9 public retrieval result dictionary.

        This is the shape LangGraph places into retrieved_evidence state.
        Only the 7 frozen §4.9 fields are included; extended provenance
        fields are not exposed in the public API response.
        """
        return {
            "scheme_id": self.scheme_id,
            "document_id": self.document_id,
            "chunk_id": self.chunk_id,
            "text": self.text,
            "source_url": self.source_url,
            "page": self.page,
            "document_version": self.document_version,
        }

    def to_evidence_reference(self) -> dict:
        """Return the §4.5 evidence reference dictionary.

        Used in the public API response 'evidence' array.
        """
        return {
            "document_id": self.document_id,
            "title": self.title,
            "url": self.source_url,
            "page": self.page,
            "section": self.section,
        }


class PMUYDocument(BaseModel):
    """Metadata for a single official PMUY source document pre-ingestion.

    Represents the state after download and before chunking.
    Derived from source_manifest.json entries.
    """

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(
        description="Source ID from source_manifest.json (e.g. 'pmuy-s01')."
    )
    short_name: str
    url: str
    source_type: str = Field(
        description="One of: official_portal_page, official_portal_faq, "
                    "official_pdf, official_pdf_annexure."
    )
    format: str = Field(description="'html' or 'pdf'.")
    retrieval_date: str
    file_on_disk: Optional[str] = Field(
        default=None,
        description="Relative path to the downloaded file, or null if not yet downloaded.",
    )
    sha256: Optional[str] = Field(
        default=None,
        description="SHA-256 hex digest of the file_on_disk, or null.",
    )
    form_version_in_document: Optional[str] = Field(
        default=None,
        description="Version label found inside the document (e.g. 'Version 8.0'). "
                    "Does not imply the version is current.",
    )
    approved: bool = Field(
        default=False,
        description="True only when all source_manifest.json open items for this "
                    "source are resolved.",
    )
    shares_file_with: Optional[str] = Field(
        default=None,
        description="source_id of another entry that shares the same physical file. "
                    "For pmuy-s05, this is 'pmuy-s04'.",
    )

