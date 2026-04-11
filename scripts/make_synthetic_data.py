"""生成合成待辦任務資料。"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path


def make_tasks(count: int) -> list[dict[str, object]]:
    base_date = date.today()
    return [
        {
            "title": f"任務 {i}",
            "priority": (i % 3) + 1,
            "due_date": (base_date + timedelta(days=i % 7)).isoformat(),
            "estimate_hours": (i % 4) + 1,
        }
        for i in range(1, count + 1)
    ]


def main() -> None:
    target = Path(__file__).resolve().parent.parent / "data" / "synthetic" / "ch01_tasks.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    tasks = make_tasks(20)
    target.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已生成合成資料：{target}")


if __name__ == "__main__":
    main()
