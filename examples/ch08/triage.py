"""第八章範例：用優先佇列安排即時插單任務。"""

from __future__ import annotations

from heapq import heappop, heappush
from typing import TypedDict


class TriageTask(TypedDict):
    """單一待處理任務。"""

    name: str
    priority: int
    arrived_at: int
    duration: int


class WaitingSummary(TypedDict):
    """等待時間摘要。"""

    average_wait: float
    longest_wait_task: str | None
    longest_wait: int


def _validate_tasks(tasks: list[TriageTask]) -> None:
    for task in tasks:
        if task["priority"] < 0:
            raise ValueError(f"任務優先等級不可為負數：{task['name']}")
        if task["arrived_at"] < 0:
            raise ValueError(f"任務到達時間不可為負數：{task['name']}")
        if task["duration"] <= 0:
            raise ValueError(f"任務處理時長必須大於 0：{task['name']}")


def build_triage_order(tasks: list[TriageTask]) -> list[TriageTask]:
    """回傳非搶占式優先佇列下的處理順序。"""
    _validate_tasks(tasks)
    if not tasks:
        return []

    waiting_heap: list[tuple[int, int, int, TriageTask]] = []
    ordered_by_arrival = sorted(
        enumerate(tasks),
        key=lambda item: (item[1]["arrived_at"], item[0]),
    )
    current_time = ordered_by_arrival[0][1]["arrived_at"]
    arrival_index = 0
    processing_order: list[TriageTask] = []

    while arrival_index < len(ordered_by_arrival) or waiting_heap:
        while (
            arrival_index < len(ordered_by_arrival)
            and ordered_by_arrival[arrival_index][1]["arrived_at"] <= current_time
        ):
            original_index, task = ordered_by_arrival[arrival_index]
            heappush(
                waiting_heap,
                (-task["priority"], task["arrived_at"], original_index, task),
            )
            arrival_index += 1

        if not waiting_heap:
            current_time = ordered_by_arrival[arrival_index][1]["arrived_at"]
            continue

        _, _, _, task = heappop(waiting_heap)
        processing_order.append(task)
        current_time += task["duration"]

    return processing_order


def estimate_waiting_times(tasks: list[TriageTask]) -> dict[str, int]:
    """回傳每個任務從到達到開始處理之間的等待時間。"""
    _validate_tasks(tasks)
    if not tasks:
        return {}

    waiting_heap: list[tuple[int, int, int, TriageTask]] = []
    ordered_by_arrival = sorted(
        enumerate(tasks),
        key=lambda item: (item[1]["arrived_at"], item[0]),
    )
    current_time = ordered_by_arrival[0][1]["arrived_at"]
    arrival_index = 0
    waiting_times: dict[str, int] = {}

    while arrival_index < len(ordered_by_arrival) or waiting_heap:
        while (
            arrival_index < len(ordered_by_arrival)
            and ordered_by_arrival[arrival_index][1]["arrived_at"] <= current_time
        ):
            original_index, task = ordered_by_arrival[arrival_index]
            heappush(
                waiting_heap,
                (-task["priority"], task["arrived_at"], original_index, task),
            )
            arrival_index += 1

        if not waiting_heap:
            current_time = ordered_by_arrival[arrival_index][1]["arrived_at"]
            continue

        _, _, _, task = heappop(waiting_heap)
        waiting_times[task["name"]] = current_time - task["arrived_at"]
        current_time += task["duration"]

    return waiting_times


def summarize_waiting_times(tasks: list[TriageTask]) -> WaitingSummary:
    """回傳整體平均等待時間與最久等待任務摘要。"""
    waiting_times = estimate_waiting_times(tasks)
    if not waiting_times:
        return {
            "average_wait": 0.0,
            "longest_wait_task": None,
            "longest_wait": 0,
        }

    longest_wait_task, longest_wait = max(
        waiting_times.items(),
        key=lambda item: (item[1], item[0]),
    )
    average_wait = sum(waiting_times.values()) / len(waiting_times)
    return {
        "average_wait": average_wait,
        "longest_wait_task": longest_wait_task,
        "longest_wait": longest_wait,
    }