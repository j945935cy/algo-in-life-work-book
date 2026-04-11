import pytest

from examples.ch07.budgeting import select_best_portfolio


def test_select_best_portfolio_prefers_best_combination_under_budget() -> None:
    items = [
        {"name": "廣告投放", "cost": 5, "value": 9},
        {"name": "客服訓練", "cost": 4, "value": 7},
        {"name": "報表工具", "cost": 3, "value": 4},
        {"name": "流程顧問", "cost": 6, "value": 10},
    ]

    total_value, selected = select_best_portfolio(items, budget=8)

    assert total_value == 13
    assert [item["name"] for item in selected] == ["廣告投放", "報表工具"]


def test_select_best_portfolio_returns_exact_fit_when_it_is_optimal() -> None:
    items = [
        {"name": "A", "cost": 2, "value": 3},
        {"name": "B", "cost": 3, "value": 4},
        {"name": "C", "cost": 5, "value": 8},
    ]

    total_value, selected = select_best_portfolio(items, budget=5)

    assert total_value == 8
    assert [item["name"] for item in selected] == ["C"]


def test_select_best_portfolio_returns_empty_for_zero_budget() -> None:
    total_value, selected = select_best_portfolio(
        [{"name": "A", "cost": 1, "value": 2}],
        budget=0,
    )

    assert total_value == 0
    assert selected == []


def test_select_best_portfolio_returns_empty_for_empty_items() -> None:
    assert select_best_portfolio([], budget=10) == (0, [])


def test_select_best_portfolio_raises_for_negative_budget() -> None:
    with pytest.raises(ValueError, match="預算不可為負數"):
        select_best_portfolio([], budget=-1)


def test_select_best_portfolio_raises_for_negative_cost() -> None:
    items = [{"name": "錯誤資料", "cost": -1, "value": 3}]

    with pytest.raises(ValueError, match="成本不可為負數"):
        select_best_portfolio(items, budget=10)


def test_select_best_portfolio_raises_for_negative_value() -> None:
    items = [{"name": "錯誤資料", "cost": 1, "value": -3}]

    with pytest.raises(ValueError, match="價值不可為負數"):
        select_best_portfolio(items, budget=10)