import pytest

from examples.ch12.assignment import (
    assign_ready_tasks,
    find_maximum_matching,
    list_unassigned_tasks,
    summarize_assignments,
)


def test_find_maximum_matching_prefers_unassigned_workers_first() -> None:
    eligible_workers_by_task = {
        "整理數據": ["小安", "小傑"],
        "製作簡報": ["小安", "小傑"],
    }

    assignments = find_maximum_matching(eligible_workers_by_task)

    assert assignments == {
        "整理數據": "小安",
        "製作簡報": "小傑",
    }


def test_assign_ready_tasks_handles_full_matching() -> None:
    ready_tasks = ["整理數據", "製作簡報", "法務檢查"]
    task_requirements = {
        "整理數據": ["數據"],
        "製作簡報": ["簡報"],
        "法務檢查": ["法務"],
    }
    worker_skills = {
        "小安": ["數據", "簡報"],
        "小美": ["法務"],
        "小傑": ["簡報"],
    }

    assignments = assign_ready_tasks(ready_tasks, task_requirements, worker_skills)

    assert assignments == {
        "整理數據": "小安",
        "製作簡報": "小傑",
        "法務檢查": "小美",
    }


def test_assign_ready_tasks_returns_partial_matching_when_people_are_insufficient() -> None:
    ready_tasks = ["主持會議", "整理數據", "法務審閱"]
    task_requirements = {
        "主持會議": ["主持"],
        "整理數據": ["數據"],
        "法務審閱": ["法務"],
    }
    worker_skills = {
        "小安": ["數據"],
        "小美": ["主持"],
    }

    summary = summarize_assignments(ready_tasks, task_requirements, worker_skills)

    assert summary == {
        "assignments": {
            "主持會議": "小美",
            "整理數據": "小安",
        },
        "unassigned_tasks": ["法務審閱"],
        "idle_workers": [],
    }


def test_list_unassigned_tasks_keeps_ready_order() -> None:
    ready_tasks = ["文案草稿", "簡報整理", "法務確認"]
    assignments = {
        "文案草稿": "小安",
        "法務確認": "小美",
    }

    assert list_unassigned_tasks(ready_tasks, assignments) == ["簡報整理"]


def test_assign_ready_tasks_raises_for_undefined_task() -> None:
    with pytest.raises(ValueError, match="找不到任務需求定義"):
        assign_ready_tasks(["未定義任務"], {}, {"小安": ["數據"]})


def test_assign_ready_tasks_raises_for_duplicate_ready_task() -> None:
    with pytest.raises(ValueError, match="ready 任務不可重複"):
        assign_ready_tasks(
            ["整理數據", "整理數據"],
            {"整理數據": ["數據"]},
            {"小安": ["數據"]},
        )