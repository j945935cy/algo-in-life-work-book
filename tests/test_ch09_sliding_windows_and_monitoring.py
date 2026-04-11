import pytest

from examples.ch09.monitoring import find_alert_windows, max_window_sum


def test_find_alert_windows_returns_all_windows_meeting_threshold() -> None:
    values = [3, 5, 4, 8, 6, 2, 7]

    alerts = find_alert_windows(values, window_size=3, threshold=15)

    assert alerts == [
        (1, 4, 17),
        (2, 5, 18),
        (3, 6, 16),
        (4, 7, 15),
    ]


def test_find_alert_windows_returns_empty_when_no_window_exceeds_threshold() -> None:
    assert find_alert_windows([1, 2, 3, 1], window_size=2, threshold=10) == []


def test_max_window_sum_returns_best_window_and_sum() -> None:
    values = [3, 5, 4, 8, 6, 2, 7]

    best_sum, best_range = max_window_sum(values, window_size=3)

    assert best_sum == 18
    assert best_range == (2, 5)


def test_max_window_sum_prefers_earliest_window_on_tie() -> None:
    values = [4, 4, 1, 4, 4]

    best_sum, best_range = max_window_sum(values, window_size=2)

    assert best_sum == 8
    assert best_range == (0, 2)


def test_monitoring_functions_raise_for_invalid_window_size() -> None:
    with pytest.raises(ValueError, match="視窗大小必須大於 0"):
        find_alert_windows([1, 2, 3], window_size=0, threshold=3)

    with pytest.raises(ValueError, match="視窗大小不可超過資料長度"):
        max_window_sum([1, 2, 3], window_size=4)


def test_find_alert_windows_raises_for_negative_threshold() -> None:
    with pytest.raises(ValueError, match="門檻不可為負數"):
        find_alert_windows([1, 2, 3], window_size=2, threshold=-1)


def test_monitoring_functions_raise_for_negative_values() -> None:
    with pytest.raises(ValueError, match="監控數值不可為負數"):
        max_window_sum([1, -2, 3], window_size=2)