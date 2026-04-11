"""第一章範例：待辦清單排序與時間紀錄工具"""

from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path
from typing import Any

TASKS = [
    {
        "title": "完成專案提案",
        "priority": 1,
        "due_date": "2026-04-20",
        "estimate_hours": 3,
    },
    {
        "title": "整理週會紀錄",
        "priority": 2,
        "due_date": "2026-04-18",
        "estimate_hours": 1,
    },
]


def parse_date(value: str) -> datetime.date:
    return datetime.datetime.strptime(value, "%Y-%m-%d").date()


def sort_tasks(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for task in tasks:
        task["due_date"] = parse_date(task["due_date"])

    return sorted(tasks, key=lambda item: (item["priority"], item["due_date"]))


def format_tasks(tasks: list[dict[str, Any]]) -> list[str]:
    return [
        f"{item['due_date'].isoformat()} | P{item['priority']} | {item['title']} ({item['estimate_hours']}h)"
        for item in tasks
    ]


def save_tasks(tasks: list[dict[str, Any]], output_path: Path) -> None:
    output_path.write_text(json.dumps(tasks, default=str, indent=2), encoding="utf-8")


def main(args: argparse.Namespace) -> int:
    tasks = TASKS
    sorted_tasks = sort_tasks(tasks)

    if args.output:
        save_tasks(sorted_tasks, Path(args.output))
        print(f"已輸出排序任務至：{args.output}")
    else:
        for line in format_tasks(sorted_tasks):
            print(line)

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="待辦清單排序與時間記錄工具")
    parser.add_argument("--output", help="輸出排序結果的 JSON 檔案路徑")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main(parse_args()))
