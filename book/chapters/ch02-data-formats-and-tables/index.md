---
title: 第二章：資料格式與表格：從 CSV 到 Parquet 與 NumPy 檔
short_title: 第二章：資料格式與表格
---

# 第二章：資料格式與表格：從 CSV 到 Parquet 與 NumPy 檔

::: advisory
本章目標
:::

- 了解常見資料格式的差異，以及各自適合的使用時機
- 建立可重現的資料匯入與型別正規化流程
- 處理缺值、格式錯誤等常見髒資料問題
- 透過 Parquet 和 NumPy 快照，讓處理後的資料可以穩定保存與重用

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
- 本章核心模組： `examples/ch02/data_transform.py`
- 測試： `pytest -q tests/test_ch02_data_formats_and_tables.py`
- 資料： `data/raw/`、`data/processed/`、`data/synthetic/`

## 資料格式讓你頭大的真正原因

很多人第一次碰資料問題，卡住的地方其實不是分析，而是資料本身就已經亂掉了。

常見的狀況：

- 同一欄有些列是數字、有些列是文字
- 日期有人寫 `2026-04-01`、有人寫 `04/01/2026`、有人只填年份
- 「空白格」不一定是真的缺值，有時只是一個空字串
- 兩份資料來源欄位名稱長得像，但意思不同

這些問題如果不先整理，後面做再多分析都很容易歪掉。本章的核心不是介紹所有格式，而是建立一套**讀入 → 正規化 → 儲存快照**的可重現流程。

## 常見資料格式的選擇時機

不同格式在可讀性、效能與跨系統相容性之間各有取捨。以下是實務上最常遇到的五種格式：

| 格式 | 適合用途 | 不適合 | 備註 |
| --- | --- | --- | --- |
| **CSV** | 原始資料交換、人工閱讀、小型資料集 | 大型資料集、含複雜型別（如日期） | 所有欄位讀進來都是字串，需要手動轉型 |
| **JSON** | API 回傳資料、巢狀結構資料 | 大型表格資料 | 適合「不規則欄位」，但讀取效能不佳 |
| **Excel (.xlsx)** | 人工填寫表單、需要公式或樣式的報表 | 程式自動化流程 | 同一欄可能混合多種格式，需特別處理 |
| **Parquet** | 處理後的分析用快照、大型資料集 | 人工直接開啟閱讀 | 欄位型別明確儲存，查詢速度快 |
| **NumPy (.npy)** | 數值計算快照、機器學習資料前處理 | 含非數值欄位的一般表格 | 保留結構化陣列格式，適合重複載入 |

**實務原則**：原始資料保留 CSV/JSON（保真），處理後存成 Parquet（效能），數值快照用 NumPy（計算用）。不要把三個角色的檔案混放在同一個目錄。

## 缺值：最常被忽略的問題

缺值（missing value）在不同格式裡長得不一樣：

| 格式 | 缺值的樣子 |
| --- | --- |
| CSV | 空欄位（`,`）、空字串（`""`）、`NA`、`N/A` |
| JSON | `null`、欄位完全不存在 |
| Excel | 空白儲存格 |
| Parquet / NumPy | `NaN`（浮點數）、`pd.NA`（Pandas 擴充型別） |

本章使用 `pd.to_numeric(errors="coerce")` 和 `pd.to_datetime(errors="coerce")` 的模式，把無法轉型的值自動標記為 `NaN`，而不是讓程式崩潰。

```python
# "invalid" 日期字串不會拋錯，而是轉成 NaT（Not a Time）
df["joined"] = pd.to_datetime(df["joined"], errors="coerce")
```

這讓你可以先完成整批資料的型別轉換，再統一決定缺值的處理策略（填補、移除、保留），而不是在讀取階段就卡住。

## Schema：先定義欄位應該長什麼樣子

在讀取任何資料之前，最值得養成的習慣是：**先定義每個欄位應該是什麼型別**。

本章用一個 `schema` 字典來描述：

```python
schema = {
    "user_id": "int",
    "score": "float",
    "joined": "datetime",
    "status": "string",
}
```

`normalize_table()` 會依照這份 schema，把每個欄位轉成對應的 Pandas 型別，並在欄位不存在時自動補上 `pd.NA`，確保輸出的 DataFrame 結構永遠一致。

這個設計的好處是：**無論輸入是哪種格式（CSV、JSON、Excel），只要經過 `normalize_table()`，出來的結構都相同**——後續的分析程式碼不需要對每種輸入格式各寫一版。

## 原始資料、處理中資料、分析用快照的三層分離

一個常見的混亂來源是：把所有版本的資料都放在同一個資料夾，或是直接覆蓋原始資料。

建議明確區分三個角色：

| 層次 | 路徑 | 內容 | 規則 |
| --- | --- | --- | --- |
| **原始資料** | `data/raw/` | 從外部取得的原始檔案 | **絕對不修改**，保留原貌 |
| **處理後資料** | `data/processed/` | 經過清理與型別轉換的 Parquet 檔 | 可重新產生，不手動編輯 |
| **分析用快照** | `data/synthetic/` | 數值型 NumPy 快照 | 用於後續計算，需與 processed 版本對應 |

本章的 `transform_file()` 函式把這個流程串成一個單一入口：

```python
processed_path, snapshot_path = transform_file(
    source_path=raw_csv,
    processed_path=processed_dir / "ch02_data.parquet",
    snapshot_path=processed_dir / "ch02_data.npy",
    schema=schema,
)
```

只要輸入相同，輸出永遠相同——這就是可重現的資料流程。

## 實作範例

請參考 `examples/ch02/data_transform.py`。

測試案例示範了一個含缺值與格式錯誤的 CSV 轉換流程：

```
user_id,score,joined,status
1,10,2026-04-01,active
2,,2026-03-15,inactive      ← score 缺值
3,7,invalid,pending         ← joined 格式錯誤
```

轉換後：
- `score` 第 2 列為 `NaN`（缺值保留）
- `joined` 第 3 列為 `NaT`（無效日期自動標記）
- Parquet 欄位型別明確，NumPy 快照保留完整結構

示範流程包含：

- 讀取 CSV、JSON、Excel、NumPy、Parquet 六種格式（統一入口）
- 依照 schema 定義進行欄位型別正規化
- 缺值與格式錯誤自動標記，不中斷轉換
- 輸出 Parquet 檔（欄位型別完整保留）與 NumPy 快照
