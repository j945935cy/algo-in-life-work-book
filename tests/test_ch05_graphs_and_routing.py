import pytest

from examples.ch05.routing import shortest_route


def test_shortest_route_returns_lowest_cost_path() -> None:
    graph = {
        "A": {"B": 4, "C": 2},
        "B": {"D": 5},
        "C": {"B": 1, "D": 8},
        "D": {},
    }

    cost, path = shortest_route(graph, "A", "D")

    assert cost == 8
    assert path == ["A", "C", "B", "D"]


def test_shortest_route_raises_for_unreachable_goal() -> None:
    graph = {
        "A": {"B": 1},
        "B": {},
        "C": {},
    }

    with pytest.raises(ValueError, match="可行路徑"):
        shortest_route(graph, "A", "C")


def test_shortest_route_raises_for_missing_node() -> None:
    graph = {
        "A": {"B": 1},
        "B": {},
    }

    with pytest.raises(ValueError, match="終點不存在"):
        shortest_route(graph, "A", "Z")