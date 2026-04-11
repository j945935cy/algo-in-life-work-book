"""第七章範例：用 0/1 背包挑出最有價值的方案組合。"""

from __future__ import annotations

from typing import TypedDict


class BudgetItem(TypedDict):
    """有限預算下可選的一個方案。"""

    name: str
    cost: int
    value: int


def _validate_items(items: list[BudgetItem], budget: int) -> None:
    if budget < 0:
        raise ValueError("預算不可為負數")

    for item in items:
        if item["cost"] < 0:
            raise ValueError(f"方案成本不可為負數：{item['name']}")
        if item["value"] < 0:
            raise ValueError(f"方案價值不可為負數：{item['name']}")


def select_best_portfolio(
    items: list[BudgetItem],
    budget: int,
) -> tuple[int, list[BudgetItem]]:
    """回傳固定預算下總價值最高的一組方案。"""
    _validate_items(items, budget)
    if not items or budget == 0:
        return 0, []

    ordered_items = list(items)
    item_count = len(ordered_items)
    best_values = [[0] * (budget + 1) for _ in range(item_count + 1)]

    for index, item in enumerate(ordered_items, start=1):
        cost = item["cost"]
        value = item["value"]
        for capacity in range(budget + 1):
            best_values[index][capacity] = best_values[index - 1][capacity]
            if cost > capacity:
                continue

            candidate = best_values[index - 1][capacity - cost] + value
            if candidate > best_values[index][capacity]:
                best_values[index][capacity] = candidate

    selected: list[BudgetItem] = []
    capacity = budget
    for index in range(item_count, 0, -1):
        if best_values[index][capacity] == best_values[index - 1][capacity]:
            continue

        item = ordered_items[index - 1]
        selected.append(item)
        capacity -= item["cost"]

    selected.reverse()
    return best_values[item_count][budget], selected