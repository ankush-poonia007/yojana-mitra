"""PMUY source ingestion package.

Owned by Anamika.

Status
------
PROPOSED — pending H4 contract confirmation from Ankush.
Do not write to data/extracted/pmuy_chunks.jsonl until the H4 chunk
schema, embedding field names, and database wiring are agreed.

Package layout
--------------
ingestion/
  __init__.py       — package stub; exposes PMUYChunk and PMUYDocument
  models.py         — proposed PMUYChunk and PMUYDocument Pydantic models
  extractor.py      — PDF/HTML text extraction (STUB — not yet implemented)
  chunker.py        — section-boundary chunking (STUB — not yet implemented)
  ingest_pmuy.py    — orchestration entry point (STUB — not yet implemented)

Dependency boundary
-------------------
- Anamika owns: source artifacts, extracted text, Pydantic chunk models,
  ingestion orchestration, tests.
- Ankush owns: pgvector insertion, embedding generation, retrieval
  integration, backend/app/database/.
- Handoff artifact: data/extracted/pmuy_chunks.jsonl
  (Anamika produces → Ankush consumes; schema TBD via H4).
"""

from app.ingestion.models import PMUYChunk, PMUYDocument

__all__ = ["PMUYChunk", "PMUYDocument"]

