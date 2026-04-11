---
title: 第三章：排序與搜尋：把「找不到」變成可解的問題
short_title: 第三章：排序與搜尋
---

# 第三章：排序與搜尋：把「找不到」變成可解的問題

::: advisory
本章目標
:::

- 理解排序與搜尋在日常資料處理中的核心角色
- 用 Python 建立可重現的排序與搜尋流程
- 透過測試檢查結果正確性與搜尋穩定性

::: advisory
情境與限制
:::

- 情境：你必須從大量紀錄中找到特定項目，或把資料依某些關鍵欄位排列
- 輸入：結構化資料表、清單、查詢值
- 輸出：排序後結果、搜尋索引或搜尋位置
- 限制：資料可能有重複值、欄位格式不一致、需要保持穩定性

::: advisory
可重現規則
:::

- 本章程式碼位置： `examples/ch03/`
- 本章核心模組： `examples/ch03/sorting_search.py`
- 測試： `pytest -q tests/test_ch03_sorting_and_searching.py`
- 資料： `data/synthetic/`（可用 `scripts/make_synthetic_data.py` 擴充）

## 本章內容概要

本章將示範排序與搜尋在工作流程中的實際應用，從資料排序策略、穩定排序概念，到二分搜尋與鍵值搜尋的實作。透過可測試的 Python 函式，讓讀者理解「先整理再找」這個常見流程。 

## 實作範例

請參考 `examples/ch03/sorting_search.py`。