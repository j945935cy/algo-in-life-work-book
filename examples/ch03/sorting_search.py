"""第三章範例：排序與搜尋實作。"""

from __future__ import annotations

from typing import Any, Callable, Iterable


def stable_sort(items: list[Any], key: Callable[[Any], Any] | None = None) -> list[Any]:
    """使用穩定排序回傳排序結果。"""
    return sorted(items, key=key)


def binary_search(
    sorted_items: list[Any],
    target: Any,
    key: Callable[[Any], Any] | None = None,
) -> int:
    """在已排序清單中執行二分搜尋，找不到時回傳 -1。"""
    left = 0
    right = len(sorted_items) - 1
    while left <= right:
        mid = (left + right) // 2
        value = sorted_items[mid]
        compare = key(value) if key else value
        target_val = key(target) if key else target

        if compare == target_val:
            return mid
        if compare < target_val:
            left = mid + 1
        else:
            right = mid - 1
    return -1