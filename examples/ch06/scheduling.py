"""第六章範例：用區間排程與加權排程安排任務。"""

from __future__ import annotations

from bisect import bisect_right
from typing import TypedDict


class Task(TypedDict):
    """簡化後的任務定義。"""

    name: str
    start: int
    end: int


class WeightedTask(Task):
    """帶有效益值的任務定義。"""

    value: int


def _validate_tasks(tasks: list[Task]) -> None:
    for task in tasks:
        if task["start"] > task["end"]:
            raise ValueError(f"任務時間區間無效：{task['name']}")


def _validate_weighted_tasks(tasks: list[WeightedTask]) -> None:
    _validate_tasks(tasks)
    for task in tasks:
        if task["value"] < 0:
            raise ValueError(f"任務效益不可為負數：{task['name']}")


def select_non_overlapping_tasks(tasks: list[Task]) -> list[Task]:
    """回傳一組互不衝突且數量最多的任務。"""
    _validate_tasks(tasks)

    ordered_tasks = sorted(
        tasks,
        key=lambda task: (task["end"], task["start"], task["name"]),
    )
    selected: list[Task] = []
    current_end: int | None = None

    for task in ordered_tasks:
        if current_end is not None and task["start"] < current_end:
            continue
        selected.append(task)
        current_end = task["end"]

    return selected


def find_conflicting_tasks(tasks: list[Task]) -> list[tuple[str, str]]:
    """回傳所有彼此衝突的任務名稱配對。"""
    _validate_tasks(tasks)

    conflicts: list[tuple[str, str]] = []
    for index, left_task in enumerate(tasks):
        for right_task in tasks[index + 1 :]:
            overlaps = (
                left_task["start"] < right_task["end"]
                and right_task["start"] < left_task["end"]
            )
            if overlaps:
                conflicts.append((left_task["name"], right_task["name"]))

    return conflicts


def select_highest_value_tasks(tasks: list[WeightedTask]) -> tuple[int, list[WeightedTask]]:
    """回傳總效益最高的一組互不衝突任務。"""
    _validate_weighted_tasks(tasks)
    if not tasks:
        return 0, []

    ordered_tasks = sorted(
        tasks,
        key=lambda task: (task["end"], task["start"], task["name"]),
    )
    ends = [task["end"] for task in ordered_tasks]
    compatible_indexes = [
        bisect_right(ends, task["start"], hi=index) - 1
        for index, task in enumerate(ordered_tasks)
    ]

    best_values: list[int] = [0] * len(ordered_tasks)
    choose_task: list[bool] = [False] * len(ordered_tasks)

    for index, task in enumerate(ordered_tasks):
        include_value = task["value"]
        previous_index = compatible_indexes[index]
        if previous_index >= 0:
            include_value += best_values[previous_index]

        exclude_value = best_values[index - 1] if index > 0 else 0
        if include_value > exclude_value:
            best_values[index] = include_value
            choose_task[index] = True
        else:
            best_values[index] = exclude_value

    selected: list[WeightedTask] = []
    index = len(ordered_tasks) - 1
    while index >= 0:
        if not choose_task[index]:
            index -= 1
            continue

        selected.append(ordered_tasks[index])
        index = compatible_indexes[index]

    selected.reverse()
    return best_values[-1], selected