"""PMUY ingestion orchestrator — STUB.

Owned by Anamika.

⚠ STUB — Not implemented. This script is a scaffold only.
   Running it raises an error until all blockers are resolved.

Blockers before this can be implemented:
    OPEN-01: H4 chunk/embedding schema must be confirmed with Ankush.
    OPEN-02: S03 (Deprivation Declaration) currency must be confirmed
             with a distributor/OMC.
    OPEN-05: All source files must be downloaded and SHA-256 verified.

When all blockers are resolved, this script will:
1. Load source_manifest.json.
2. For each source where file_on_disk is set and sha256 is verified:
   a. Call PMUYExtractor to extract text.
   b. Call PMUYChunker to produce PMUYChunk instances.
   c. Serialize to data/extracted/pmuy_chunks.jsonl (one JSON per line).
3. Log counts, errors, and skipped sources.
4. Never overwrite an existing output without explicit --force flag.

Ownership boundary:
    This script writes to data/extracted/pmuy_chunks.jsonl.
    Ankush's database wiring reads from that file.
    This script does NOT insert into any database or generate embeddings.

Usage (once implemented):
    python -m app.ingestion.ingest_pmuy [--force] [--source pmuy-s03]
"""

import sys


def main() -> None:
    print(
        "ERROR: ingest_pmuy.py is a stub.\n"
        "Implement only after:\n"
        "  OPEN-01: H4 schema confirmed with Ankush.\n"
        "  OPEN-02: S03 currency confirmed with distributor/OMC.\n"
        "  OPEN-05: Source files downloaded and SHA-256 verified.\n",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()

