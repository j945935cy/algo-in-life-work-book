"""第十一章範例：用拓樸排序安排有依賴關係的流程。"""

from __future__ import annotations

from collections import deque


def _validate_dependencies(tasks: dict[str, list[str]]) -> None:
    for task, dependencies in tasks.items():
        for dependency in dependencies:
            if dependency not in tasks:
                raise ValueError(f"任務依賴未定義：{task} -> {dependency}")


def _build_graph(tasks: dict[str, list[str]]) -> tuple[dict[str, list[str]], dict[str, int]]:
    _validate_dependencies(tasks)
    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}

    for task, dependencies in tasks.items():
        for dependency in dependencies:
            graph[dependency].append(task)
            in_degree[task] += 1

    return graph, in_degree


def plan_execution_order(tasks: dict[str, list[str]]) -> list[str]:
    """回傳一條可執行的任務順序。"""
    graph, in_degree = _build_graph(tasks)
    ready = deque(task for task, degree in in_degree.items() if degree == 0)
    order: list[str] = []

    while ready:
        task = ready.popleft()
        order.append(task)

        for follower in graph[task]:
            in_degree[follower] -= 1
            if in_degree[follower] == 0:
                ready.append(follower)

    if len(order) != len(tasks):
        raise ValueError("流程存在循環依賴，無法排出可執行順序")

    return order


def group_execution_stages(tasks: dict[str, list[str]]) -> list[list[str]]:
    """回傳依批次分組的可執行階段。"""
    graph, in_degree = _build_graph(tasks)
    ready = [task for task, degree in in_degree.items() if degree == 0]
    stages: list[list[str]] = []
    processed_count = 0

    while ready:
        current_stage = ready
        stages.append(current_stage)
        next_ready: list[str] = []

        for task in current_stage:
            processed_count += 1
            for follower in graph[task]:
                in_degree[follower] -= 1
                if in_degree[follower] == 0:
                    next_ready.append(follower)

        ready = next_ready

    if processed_count != len(tasks):
        raise ValueError("流程存在循環依賴，無法分組執行階段")

    return stages