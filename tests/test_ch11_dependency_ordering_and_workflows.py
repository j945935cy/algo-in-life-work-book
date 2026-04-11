import pytest

from examples.ch11.workflow import group_execution_stages, plan_execution_order


def test_plan_execution_order_returns_valid_topological_order() -> None:
    tasks = {
        "整理需求": [],
        "完成文件": ["整理需求"],
        "送審": ["完成文件"],
        "上線": ["送審"],
        "建立測試資料": ["整理需求"],
    }

    order = plan_execution_order(tasks)

    assert order == ["整理需求", "完成文件", "建立測試資料", "送審", "上線"]


def test_group_execution_stages_returns_parallel_ready_groups() -> None:
    tasks = {
        "整理需求": [],
        "完成文件": ["整理需求"],
        "建立測試資料": ["整理需求"],
        "送審": ["完成文件"],
        "上線": ["送審", "建立測試資料"],
    }

    stages = group_execution_stages(tasks)

    assert stages == [["整理需求"], ["完成文件", "建立測試資料"], ["送審"], ["上線"]]


def test_workflow_functions_allow_multiple_starting_tasks() -> None:
    tasks = {
        "準備簡報": [],
        "匯出數據": [],
        "整理週報": ["匯出數據"],
    }

    assert plan_execution_order(tasks) == ["準備簡報", "匯出數據", "整理週報"]
    assert group_execution_stages(tasks) == [["準備簡報", "匯出數據"], ["整理週報"]]


def test_workflow_functions_raise_for_undefined_dependency() -> None:
    tasks = {"上線": ["送審"]}

    with pytest.raises(ValueError, match="依賴未定義"):
        plan_execution_order(tasks)


def test_workflow_functions_raise_for_cycle() -> None:
    tasks = {
        "A": ["C"],
        "B": ["A"],
        "C": ["B"],
    }

    with pytest.raises(ValueError, match="循環依賴"):
        plan_execution_order(tasks)

    with pytest.raises(ValueError, match="循環依賴"):
        group_execution_stages(tasks)