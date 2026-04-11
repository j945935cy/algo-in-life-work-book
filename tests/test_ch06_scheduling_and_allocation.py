import pytest

from examples.ch06.scheduling import (
    find_conflicting_tasks,
    select_highest_value_tasks,
    select_non_overlapping_tasks,
)


def test_select_non_overlapping_tasks_returns_max_count_schedule() -> None:
    tasks = [
        {"name": "晨會", "start": 9, "end": 10},
        {"name": "客戶訪談", "start": 9, "end": 12},
        {"name": "文件整理", "start": 10, "end": 11},
        {"name": "外勤拜訪", "start": 11, "end": 13},
        {"name": "內部簡報", "start": 12, "end": 14},
    ]

    selected = select_non_overlapping_tasks(tasks)

    assert [task["name"] for task in selected] == ["晨會", "文件整理", "外勤拜訪"]


def test_select_non_overlapping_tasks_allows_touching_boundaries() -> None:
    tasks = [
        {"name": "A", "start": 9, "end": 10},
        {"name": "B", "start": 10, "end": 11},
        {"name": "C", "start": 11, "end": 12},
    ]

    selected = select_non_overlapping_tasks(tasks)

    assert [task["name"] for task in selected] == ["A", "B", "C"]


def test_select_non_overlapping_tasks_returns_empty_for_empty_input() -> None:
    assert select_non_overlapping_tasks([]) == []


def test_find_conflicting_tasks_reports_overlaps_in_stable_order() -> None:
    tasks = [
        {"name": "晨會", "start": 9, "end": 10},
        {"name": "訪談", "start": 9, "end": 11},
        {"name": "報表", "start": 10, "end": 12},
        {"name": "寄送", "start": 12, "end": 13},
    ]

    conflicts = find_conflicting_tasks(tasks)

    assert conflicts == [("晨會", "訪談"), ("訪談", "報表")]


def test_select_non_overlapping_tasks_raises_for_invalid_range() -> None:
    tasks = [{"name": "錯誤資料", "start": 14, "end": 11}]

    with pytest.raises(ValueError, match="時間區間無效"):
        select_non_overlapping_tasks(tasks)


def test_select_highest_value_tasks_prefers_total_value_over_count() -> None:
    tasks = [
        {"name": "晨會", "start": 9, "end": 10, "value": 2},
        {"name": "長談", "start": 9, "end": 12, "value": 9},
        {"name": "文件整理", "start": 10, "end": 11, "value": 2},
        {"name": "客戶拜訪", "start": 11, "end": 12, "value": 2},
    ]

    total_value, selected = select_highest_value_tasks(tasks)

    assert total_value == 9
    assert [task["name"] for task in selected] == ["長談"]


def test_select_highest_value_tasks_returns_best_compatible_chain() -> None:
    tasks = [
        {"name": "A", "start": 9, "end": 10, "value": 3},
        {"name": "B", "start": 10, "end": 11, "value": 4},
        {"name": "C", "start": 9, "end": 11, "value": 6},
        {"name": "D", "start": 11, "end": 12, "value": 5},
    ]

    total_value, selected = select_highest_value_tasks(tasks)

    assert total_value == 12
    assert [task["name"] for task in selected] == ["A", "B", "D"]


def test_select_highest_value_tasks_returns_empty_for_empty_input() -> None:
    total_value, selected = select_highest_value_tasks([])

    assert total_value == 0
    assert selected == []


def test_select_highest_value_tasks_raises_for_negative_value() -> None:
    tasks = [{"name": "錯誤資料", "start": 9, "end": 10, "value": -1}]

    with pytest.raises(ValueError, match="效益不可為負數"):
        select_highest_value_tasks(tasks)