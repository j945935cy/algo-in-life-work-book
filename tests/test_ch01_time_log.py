import json
from pathlib import Path

from algo_in_life.time_log import sort_tasks


def test_sort_tasks_by_priority_and_due_date(tmp_path: Path) -> None:
    tasks = [
        {"title": "B", "priority": 2, "due_date": "2026-04-20", "estimate_hours": 2},
        {"title": "A", "priority": 1, "due_date": "2026-04-21", "estimate_hours": 1},
    ]

    sorted_tasks = sort_tasks(tasks)

    assert sorted_tasks[0]["title"] == "A"
    assert sorted_tasks[1]["title"] == "B"


def test_task_output_file(tmp_path: Path) -> None:
    output_path = tmp_path / "sorted_tasks.json"
    tasks = [
        {"title": "A", "priority": 1, "due_date": "2026-04-20", "estimate_hours": 1},
    ]

    output_path.write_text(json.dumps(tasks), encoding="utf-8")
    loaded = json.loads(output_path.read_text(encoding="utf-8"))

    assert loaded[0]["title"] == "A"
