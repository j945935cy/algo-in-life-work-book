from examples.ch04.deduplication import deduplicate_records, find_duplicate_indices, record_fingerprint


def test_record_fingerprint_normalizes_case_and_spaces() -> None:
    left = {"email": " A@Example.com ", "name": " Alice  Chen "}
    right = {"name": "alice chen", "email": "a@example.com"}

    assert record_fingerprint(left, ["email", "name"]) == record_fingerprint(right, ["email", "name"])


def test_find_duplicate_indices_returns_non_first_duplicates() -> None:
    records = [
        {"email": "amy@example.com", "name": "Amy"},
        {"email": "bob@example.com", "name": "Bob"},
        {"email": " AMY@example.com ", "name": "amy"},
        {"email": "bob@example.com", "name": " Bob "},
    ]

    assert find_duplicate_indices(records, ["email"]) == [2, 3]


def test_deduplicate_records_preserves_first_seen_order() -> None:
    records = [
        {"customer_id": 101, "email": "first@example.com"},
        {"customer_id": 102, "email": "second@example.com"},
        {"customer_id": 999, "email": " first@example.com "},
        {"customer_id": 103, "email": "third@example.com"},
    ]

    unique_records = deduplicate_records(records, ["email"])

    assert unique_records == [
        {"customer_id": 101, "email": "first@example.com"},
        {"customer_id": 102, "email": "second@example.com"},
        {"customer_id": 103, "email": "third@example.com"},
    ]