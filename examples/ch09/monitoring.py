"""第九章範例：用滑動視窗找出異常區段。"""

from __future__ import annotations


def _validate_inputs(values: list[int], window_size: int, threshold: int | None = None) -> None:
    if window_size <= 0:
        raise ValueError("視窗大小必須大於 0")
    if window_size > len(values):
        raise ValueError("視窗大小不可超過資料長度")
    if threshold is not None and threshold < 0:
        raise ValueError("門檻不可為負數")
    for value in values:
        if value < 0:
            raise ValueError("監控數值不可為負數")


def find_alert_windows(
    values: list[int],
    window_size: int,
    threshold: int,
) -> list[tuple[int, int, int]]:
    """回傳所有總量超過門檻的固定視窗區段。"""
    _validate_inputs(values, window_size, threshold)

    current_sum = sum(values[:window_size])
    alerts: list[tuple[int, int, int]] = []
    if current_sum >= threshold:
        alerts.append((0, window_size, current_sum))

    for right in range(window_size, len(values)):
        left = right - window_size
        current_sum += values[right] - values[left]
        start = left + 1
        end = right + 1
        if current_sum >= threshold:
            alerts.append((start, end, current_sum))

    return alerts


def max_window_sum(values: list[int], window_size: int) -> tuple[int, tuple[int, int] | None]:
    """回傳固定視窗下的最大總量與對應區間。"""
    _validate_inputs(values, window_size)

    current_sum = sum(values[:window_size])
    best_sum = current_sum
    best_range = (0, window_size)

    for right in range(window_size, len(values)):
        left = right - window_size
        current_sum += values[right] - values[left]
        start = left + 1
        end = right + 1
        if current_sum > best_sum:
            best_sum = current_sum
            best_range = (start, end)

    return best_sum, best_range