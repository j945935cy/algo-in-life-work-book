import pytest

from examples.ch10.capacity import merge_time_blocks, peak_concurrent_usage


def test_merge_time_blocks_combines_overlapping_and_touching_blocks() -> None:
    blocks = [
        {"name": "會議室 A", "start": 9, "end": 11},
        {"name": "會議室 A 延長", "start": 11, "end": 12},
        {"name": "設備借用", "start": 10, "end": 13},
        {"name": "下午清潔", "start": 15, "end": 16},
    ]

    merged = merge_time_blocks(blocks)

    assert merged == [
        {"name": "會議室 A + 設備借用 + 會議室 A 延長", "start": 9, "end": 13},
        {"name": "下午清潔", "start": 15, "end": 16},
    ]


def test_merge_time_blocks_returns_empty_for_empty_input() -> None:
    assert merge_time_blocks([]) == []


def test_peak_concurrent_usage_returns_peak_count_and_earliest_peak_range() -> None:
    blocks = [
        {"name": "A", "start": 9, "end": 12},
        {"name": "B", "start": 10, "end": 13},
        {"name": "C", "start": 10, "end": 11},
        {"name": "D", "start": 12, "end": 14},
    ]

    peak_usage, peak_range = peak_concurrent_usage(blocks)

    assert peak_usage == 3
    assert peak_range == (10, 11)


def test_peak_concurrent_usage_returns_zero_for_empty_input() -> None:
    assert peak_concurrent_usage([]) == (0, None)


def test_peak_concurrent_usage_treats_touching_blocks_as_not_overlapping_for_peak() -> None:
    blocks = [
        {"name": "A", "start": 9, "end": 10},
        {"name": "B", "start": 10, "end": 11},
    ]

    peak_usage, peak_range = peak_concurrent_usage(blocks)

    assert peak_usage == 1
    assert peak_range == (9, 10)


def test_capacity_functions_raise_for_invalid_ranges() -> None:
    with pytest.raises(ValueError, match="end > start"):
        merge_time_blocks([{"name": "錯誤資料", "start": 10, "end": 10}])

    with pytest.raises(ValueError, match="開始時間不可為負數"):
        peak_concurrent_usage([{"name": "錯誤資料", "start": -1, "end": 1}])