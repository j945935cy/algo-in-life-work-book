"""第十二章範例：把 ready 任務指派給合適的人。"""

from __future__ import annotations

from typing import TypedDict


class AssignmentSummary(TypedDict):
    """任務指派摘要。"""

    assignments: dict[str, str]
    unassigned_tasks: list[str]
    idle_workers: list[str]


def _validate_catalogs(
    task_requirements: dict[str, list[str]],
    worker_skills: dict[str, list[str]],
) -> None:
    for task_name, required_skills in task_requirements.items():
        if not isinstance(required_skills, list):
            raise ValueError(f"任務需求必須是技能清單：{task_name}")
        for skill in required_skills:
            if not isinstance(skill, str) or not skill:
                raise ValueError(f"技能名稱必須是非空字串：{task_name}")

    for worker_name, skills in worker_skills.items():
        if not isinstance(skills, list):
            raise ValueError(f"人員技能必須是技能清單：{worker_name}")
        for skill in skills:
            if not isinstance(skill, str) or not skill:
                raise ValueError(f"技能名稱必須是非空字串：{worker_name}")


def _validate_ready_tasks(ready_tasks: list[str], task_requirements: dict[str, list[str]]) -> None:
    seen_tasks: set[str] = set()
    for task in ready_tasks:
        if task in seen_tasks:
            raise ValueError(f"ready 任務不可重複：{task}")
        if task not in task_requirements:
            raise ValueError(f"找不到任務需求定義：{task}")
        seen_tasks.add(task)


def _build_eligible_workers(
    task_requirements: dict[str, list[str]],
    worker_skills: dict[str, list[str]],
) -> dict[str, list[str]]:
    worker_skill_sets = {
        worker_name: set(skills)
        for worker_name, skills in worker_skills.items()
    }
    eligible_workers: dict[str, list[str]] = {}

    for task_name, required_skills in task_requirements.items():
        required_skill_set = set(required_skills)
        eligible_workers[task_name] = [
            worker_name
            for worker_name, skills in worker_skill_sets.items()
            if required_skill_set.issubset(skills)
        ]

    return eligible_workers


def find_maximum_matching(eligible_workers_by_task: dict[str, list[str]]) -> dict[str, str]:
    """回傳一組最多可行的任務與人員配對。"""
    worker_to_task: dict[str, str] = {}
    task_to_worker: dict[str, str] = {}

    def try_assign(task_name: str, seen_workers: set[str]) -> bool:
        for worker_name in eligible_workers_by_task[task_name]:
            if worker_name in seen_workers or worker_name in worker_to_task:
                continue
            seen_workers.add(worker_name)
            worker_to_task[worker_name] = task_name
            task_to_worker[task_name] = worker_name
            return True

        for worker_name in eligible_workers_by_task[task_name]:
            if worker_name in seen_workers:
                continue
            seen_workers.add(worker_name)
            occupied_task = worker_to_task.get(worker_name)
            if occupied_task is None:
                worker_to_task[worker_name] = task_name
                task_to_worker[task_name] = worker_name
                return True
            if try_assign(occupied_task, seen_workers):
                worker_to_task[worker_name] = task_name
                task_to_worker[task_name] = worker_name
                return True

        return False

    for task_name in eligible_workers_by_task:
        try_assign(task_name, set())

    return task_to_worker


def assign_ready_tasks(
    ready_tasks: list[str],
    task_requirements: dict[str, list[str]],
    worker_skills: dict[str, list[str]],
) -> dict[str, str]:
    """根據技能需求，指派目前 ready 的任務。"""
    _validate_catalogs(task_requirements, worker_skills)
    _validate_ready_tasks(ready_tasks, task_requirements)

    eligible_workers = _build_eligible_workers(task_requirements, worker_skills)
    ready_eligible_workers = {
        task_name: eligible_workers[task_name]
        for task_name in ready_tasks
    }
    return find_maximum_matching(ready_eligible_workers)


def list_unassigned_tasks(ready_tasks: list[str], assignments: dict[str, str]) -> list[str]:
    """列出仍未被分配出去的 ready 任務。"""
    return [task_name for task_name in ready_tasks if task_name not in assignments]


def summarize_assignments(
    ready_tasks: list[str],
    task_requirements: dict[str, list[str]],
    worker_skills: dict[str, list[str]],
) -> AssignmentSummary:
    """回傳指派結果、未分配任務與閒置人員。"""
    assignments = assign_ready_tasks(ready_tasks, task_requirements, worker_skills)
    assigned_workers = set(assignments.values())

    return {
        "assignments": assignments,
        "unassigned_tasks": list_unassigned_tasks(ready_tasks, assignments),
        "idle_workers": [
            worker_name
            for worker_name in worker_skills
            if worker_name not in assigned_workers
        ],
    }