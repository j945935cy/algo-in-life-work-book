import pytest

from examples.ch08.triage import (
    build_triage_order,
    estimate_waiting_times,
    summarize_waiting_times,
)


def test_build_triage_order_prefers_high_priority_after_current_task_finishes() -> None:
    tasks = [
        {"name": "例行回覆", "priority": 1, "arrived_at": 0, "duration": 3},
        {"name": "VIP 客訴", "priority": 5, "arrived_at": 1, "duration": 1},
        {"name": "系統告警", "priority": 4, "arrived_at": 3, "duration": 2},
    ]

    order = build_triage_order(tasks)

    assert [task["name"] for task in order] == ["例行回覆", "VIP 客訴", "系統告警"]


def test_build_triage_order_uses_arrival_order_when_priority_ties() -> None:
    tasks = [
        {"name": "A", "priority": 3, "arrived_at": 0, "duration": 2},
        {"name": "B", "priority": 3, "arrived_at": 0, "duration": 1},
        {"name": "C", "priority": 3, "arrived_at": 1, "duration": 1},
    ]

    order = build_triage_order(tasks)

    assert [task["name"] for task in order] == ["A", "B", "C"]


def test_build_triage_order_jumps_forward_when_queue_is_empty() -> None:
    tasks = [
        {"name": "上午例行", "priority": 1, "arrived_at": 0, "duration": 1},
        {"name": "下午插單", "priority": 4, "arrived_at": 5, "duration": 1},
    ]

    order = build_triage_order(tasks)

    assert [task["name"] for task in order] == ["上午例行", "下午插單"]


def test_estimate_waiting_times_returns_wait_per_task() -> None:
    tasks = [
        {"name": "例行回覆", "priority": 1, "arrived_at": 0, "duration": 3},
        {"name": "VIP 客訴", "priority": 5, "arrived_at": 1, "duration": 1},
        {"name": "系統告警", "priority": 4, "arrived_at": 3, "duration": 2},
    ]

    waiting_times = estimate_waiting_times(tasks)

    assert waiting_times == {"例行回覆": 0, "VIP 客訴": 2, "系統告警": 1}


def test_summarize_waiting_times_returns_average_and_longest_wait() -> None:
    tasks = [
        {"name": "例行回覆", "priority": 1, "arrived_at": 0, "duration": 3},
        {"name": "VIP 客訴", "priority": 5, "arrived_at": 1, "duration": 1},
        {"name": "系統告警", "priority": 4, "arrived_at": 3, "duration": 2},
    ]

    summary = summarize_waiting_times(tasks)

    assert summary == {
        "average_wait": 1.0,
        "longest_wait_task": "VIP 客訴",
        "longest_wait": 2,
    }


def test_build_triage_order_returns_empty_for_empty_input() -> None:
    assert build_triage_order([]) == []
    assert estimate_waiting_times([]) == {}
    assert summarize_waiting_times([]) == {
        "average_wait": 0.0,
        "longest_wait_task": None,
        "longest_wait": 0,
    }


def test_build_triage_order_raises_for_negative_priority() -> None:
    tasks = [{"name": "錯誤資料", "priority": -1, "arrived_at": 0, "duration": 1}]

    with pytest.raises(ValueError, match="優先等級不可為負數"):
        build_triage_order(tasks)


def test_build_triage_order_raises_for_non_positive_duration() -> None:
    tasks = [{"name": "錯誤資料", "priority": 1, "arrived_at": 0, "duration": 0}]

    with pytest.raises(ValueError, match="處理時長必須大於 0"):
        estimate_waiting_times(tasks)