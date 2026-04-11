"""第五章範例：使用 Dijkstra 找最短路徑。"""

from __future__ import annotations

import heapq
from math import inf


def shortest_route(
    graph: dict[str, dict[str, float]],
    start: str,
    goal: str,
) -> tuple[float, list[str]]:
    """回傳最短成本與對應路徑。"""
    if start not in graph:
        raise ValueError(f"起點不存在：{start}")
    if goal not in graph:
        raise ValueError(f"終點不存在：{goal}")

    distances: dict[str, float] = {node: inf for node in graph}
    previous: dict[str, str | None] = {node: None for node in graph}
    distances[start] = 0
    queue: list[tuple[float, str]] = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        if current_node == goal:
            break

        for neighbor, weight in graph[current_node].items():
            new_distance = current_distance + weight
            if new_distance >= distances[neighbor]:
                continue
            distances[neighbor] = new_distance
            previous[neighbor] = current_node
            heapq.heappush(queue, (new_distance, neighbor))

    if distances[goal] == inf:
        raise ValueError(f"找不到從 {start} 到 {goal} 的可行路徑")

    path: list[str] = []
    current: str | None = goal
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    return distances[goal], path