from __future__ import annotations

import datetime
from typing import Any


def parse_date(value: str) -> datetime.date:
    return datetime.datetime.strptime(value, "%Y-%m-%d").date()


def sort_tasks(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parsed = []
    for task in tasks:
        parsed.append(
            {
                **task,
                "due_date": parse_date(task["due_date"]),
            }
        )
    return sorted(parsed, key=lambda item: (item["priority"], item["due_date"]))
