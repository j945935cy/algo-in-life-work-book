"""Chapter 04 example package."""

from .deduplication import deduplicate_records, find_duplicate_indices, record_fingerprint

__all__ = ["record_fingerprint", "find_duplicate_indices", "deduplicate_records"]