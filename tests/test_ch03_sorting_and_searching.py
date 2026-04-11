from examples.ch03.sorting_search import binary_search, stable_sort


def test_stable_sort_numbers() -> None:
    values = [3, 1, 4, 2, 2]
    assert stable_sort(values) == [1, 2, 2, 3, 4]


def test_stable_sort_with_key() -> None:
    data = ["b", "A", "c"]
    assert stable_sort(data, key=str.lower) == ["A", "b", "c"]


def test_binary_search_found() -> None:
    items = [1, 3, 5, 7, 9]
    assert binary_search(items, 5) == 2


def test_binary_search_not_found() -> None:
    items = [1, 3, 5, 7, 9]
    assert binary_search(items, 2) == -1


def test_binary_search_with_key() -> None:
    items = ["apple", "banana", "cherry"]
    assert binary_search(items, "Banana", key=str.lower) == 1