"""第十章範例：用區間合併與掃描線分析容量尖峰。"""

from __future__ import annotations

from collections import defaultdict
from typing import TypedDict


class TimeBlock(TypedDict):
    """單一占用時段。"""

    name: str
    start: int
    end: int


def _validate_blocks(blocks: list[TimeBlock]) -> None:
    for block in blocks:
        if block["start"] < 0:
            raise ValueError(f"開始時間不可為負數：{block['name']}")
        if block["end"] <= block["start"]:
            raise ValueError(f"時段區間必須滿足 end > start：{block['name']}")


def merge_time_blocks(blocks: list[TimeBlock]) -> list[TimeBlock]:
    """合併所有重疊或首尾相接的時段。"""
    _validate_blocks(blocks)
    if not blocks:
        return []

    ordered_blocks = sorted(blocks, key=lambda block: (block["start"], block["end"], block["name"]))
    merged: list[TimeBlock] = [dict(ordered_blocks[0])]

    for block in ordered_blocks[1:]:
        current = merged[-1]
        if block["start"] <= current["end"]:
            current["end"] = max(current["end"], block["end"])
            current["name"] = f"{current['name']} + {block['name']}"
            continue
        merged.append(dict(block))

    return merged


def peak_concurrent_usage(blocks: list[TimeBlock]) -> tuple[int, tuple[int, int] | None]:
    """回傳尖峰同時使用量與最早出現的尖峰區間。"""
    _validate_blocks(blocks)
    if not blocks:
        return 0, None

    events: dict[int, int] = defaultdict(int)
    for block in blocks:
        events[block["start"]] += 1
        events[block["end"]] -= 1

    ordered_times = sorted(events)
    current_usage = 0
    peak_usage = 0
    peak_range: tuple[int, int] | None = None

    for index, time in enumerate(ordered_times[:-1]):
        current_usage += events[time]
        next_time = ordered_times[index + 1]
        if current_usage > peak_usage and next_time > time:
            peak_usage = current_usage
            peak_range = (time, next_time)

    return peak_usage, peak_range