"""PMUY source chunker — STUB.

Owned by Anamika.

⚠ STUB — Not implemented. This file is a scaffold only.
   Implementation is blocked on H4 contract confirmation (OPEN-01).

When implemented, this module will:
- Accept raw extracted (page_or_section, text) tuples from PMUYExtractor.
- Split text into chunks that respect section boundaries.
- Assign deterministic chunk IDs using the agreed convention.
- Produce PMUYChunk instances ready for JSONL serialization.

Proposed chunk_id convention (PENDING H4 confirmation):
    PDF:  "{document_id}-p{page:03d}-c{seq:03d}"
    HTML: "{document_id}-s{section_slug}-c{seq:03d}"

Do NOT implement until H4 schema is confirmed (OPEN-01).
"""

from __future__ import annotations


class PMUYChunkerNotImplemented(NotImplementedError):
    """Raised when the chunker is called before implementation is approved."""

    def __init__(self) -> None:
        super().__init__(
            "PMUYChunker is a stub. "
            "Implement only after H4 schema is confirmed (OPEN-01)."
        )


class PMUYChunker:
    """Splits extracted PMUY text into storable chunks.

    ⚠ STUB — all methods raise PMUYChunkerNotImplemented.
    """

    def chunk(self, extracted: list, document_id: str, **metadata) -> list:
        """Produce PMUYChunk objects from extracted text.

        Args:
            extracted: Output of PMUYExtractor (list of page/section+text tuples).
            document_id: Source document ID (e.g. 'pmuy-s03').
            **metadata: Additional provenance fields from PMUYDocument.

        Returns:
            List of PMUYChunk instances.
        """
        raise PMUYChunkerNotImplemented()

