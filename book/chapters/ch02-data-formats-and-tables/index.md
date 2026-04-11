# 第二章：資料格式與表格：從 CSV 到 Parquet 與 NumPy 檔

::: advisory
本章目標
:::

- 了解常見資料格式的差異與選擇
- 建立可重現的資料匯入/處理流程
- 透過 Python 建立資料轉換與資料安全的基礎規範

::: advisory
情境與限制
:::

- 情境：你需要整理多種資料來源，並將其轉成一致格式以供後續分析
- 輸入：CSV、Excel、JSON、NumPy、Parquet 形式的資料
- 輸出：可重用的資料檔案與轉換流程
- 限制：需考慮缺值、欄位型別不一致、資料格式安全

::: advisory
可重現規則
:::

- 本章程式碼位置： `examples/ch02/`
- 測試： `pytest -q tests/test_ch02_data_formats_and_tables.py`
- 資料： `data/raw/`、`data/processed/`、`data/synthetic/`

## 本章內容概要

本章將示範如何從日常資料清理需求出發，建立一套簡單但可重現的資料格式轉換流程。從 CSV/Excel 到 Parquet、NumPy 快照，並示範基本的型別正規化與缺值處理方法。

## 實作範例

請參考 `examples/ch02/` 中的 `data_transform.py`。本章將建立可執行的資料轉換腳本，並說明如何在 `data/` 內保存資料快照與處理後資料。

示範流程包含：

- 從 CSV 與 JSON 載入原始資料
- 依照欄位型別定義進行型別正規化
- 輸出 Parquet 檔案與 NumPy 快照檔案
