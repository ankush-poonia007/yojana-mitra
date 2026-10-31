"""PMUY source extractor — STUB.

Owned by Anamika.

⚠ STUB — Not implemented. This file is a scaffold only.
   Implementation is blocked on:
   - Source files being downloaded and SHA-256 verified (OPEN-05).
   - H4 contract confirmation (OPEN-01).

When implemented, this module will:
- Extract text from HTML sources (S01, S02) using html.parser / lxml.
- Extract text from PDF sources (S03, S04/S05) using pypdf (already installed:
  pypdf 6.14.2 confirmed in backend/requirements.txt).
- Preserve page numbers for PDF sources.
- Identify section headings for structured extraction.
- Return raw extracted content as a list of (page_or_section, text) tuples.

Do NOT implement until:
1. Ankush confirms the H4 schema (OPEN-01).
2. Source files are downloaded and their SHA-256 hashes recorded (OPEN-05).
3. S03 currency is confirmed with a distributor/OMC (OPEN-02).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


class PMUYExtractorNotImplemented(NotImplementedError):
    """Raised when the extractor is called before implementation is approved."""

    def __init__(self) -> None:
        super().__init__(
            "PMUYExtractor is a stub. "
            "Implement only after H4 schema is confirmed (OPEN-01) and "
            "source files are on disk with verified SHA-256 hashes (OPEN-05)."
        )


class PMUYExtractor:
    """Extracts raw text from PMUY official source documents.

    ⚠ STUB — all methods raise PMUYExtractorNotImplemented.
    """

    def extract_pdf(
        self, file_path: Path, source_id: str
    ) -> list[tuple[int, str]]:
        """Extract text by page from a PDF.

        Returns:
            List of (page_number: int, text: str) tuples.
            page_number is 1-based.
        """
        raise PMUYExtractorNotImplemented()

    def extract_html(
        self, file_path: Path, source_id: str
    ) -> list[tuple[Optional[str], str]]:
        """Extract text by section from an HTML snapshot.

        Returns:
            List of (section_heading: str | None, text: str) tuples.
        """
        raise PMUYExtractorNotImplemented()

