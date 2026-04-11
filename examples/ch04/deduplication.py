"""第四章範例：使用雜湊指紋做穩定去重。"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable, Mapping


def _normalize_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.strip().lower().split())
    return str(value).strip().lower()


def record_fingerprint(record: Mapping[str, Any], keys: Iterable[str]) -> str:
    """為指定欄位建立穩定雜湊值。"""
    normalized_payload = {
        key: _normalize_value(record.get(key))
        for key in keys
    }
    encoded = json.dumps(normalized_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def find_duplicate_indices(records: list[Mapping[str, Any]], keys: Iterable[str]) -> list[int]:
    """找出重複資料的索引，保留第一筆視為主紀錄。"""
    seen: set[str] = set()
    duplicate_indices: list[int] = []

    for index, record in enumerate(records):
        fingerprint = record_fingerprint(record, keys)
        if fingerprint in seen:
            duplicate_indices.append(index)
            continue
        seen.add(fingerprint)

    return duplicate_indices


def deduplicate_records(
    records: list[Mapping[str, Any]],
    keys: Iterable[str],
) -> list[Mapping[str, Any]]:
    """依指定欄位去重，並保留原始資料順序。"""
    seen: set[str] = set()
    unique_records: list[Mapping[str, Any]] = []

    for record in records:
        fingerprint = record_fingerprint(record, keys)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        unique_records.append(record)

    return unique_records