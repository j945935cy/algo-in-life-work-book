---
title: 日常與職場的演算法應用
short_title: 書籍首頁
---

# 日常與職場的演算法應用

把日常與職場中的問題，整理成可以被說明、實作、測試與重現的演算法工作流。

> 這個專案同時是一份書稿、一組可執行範例，也是一條可反覆驗證的出版管線。

## 你現在看到的是什麼

這不是只有章節草稿的目錄，而是一個已經開始落地的書籍 repo。書稿、範例程式、測試、資料與建站設定放在同一個地方，目的是讓每一章都能同時回答三件事：

- 問題是什麼
- 程式怎麼做
- 結果如何驗證

## 目前成果快照

| 項目 | 目前狀態 |
| --- | --- |
| 書稿首頁與前言 | 已完成 |
| 章節骨架 | 已完成第 1 到第 8 章 |
| 可執行範例 | 已完成 8 組 |
| 測試 | `pytest -q` 全綠 |
| HTML 建站 | 已可產出本地站點 |

## 本書的閱讀節奏

每一章都遵循同一個結構，方便讀者快速進入狀況，也方便後續持續擴寫：

1. 從日常或職場情境出發
2. 把問題轉成輸入、輸出與限制
3. 用 Python 做最小可運行實作
4. 用測試固定結果
5. 用練習題延伸思考與應用

## 已完成章節摘要

### 第一章

[第一章：用演算法思維整理日常工作](chapters/ch01-algorithmic-thinking/index)

從待辦排序與時間紀錄切入，建立全書的基本語言：問題抽象化、優先順序與可重現工作流。

### 第二章

[第二章：資料格式與表格：從 CSV 到 Parquet 與 NumPy 檔](chapters/ch02-data-formats-and-tables/index)

聚焦資料匯入與格式轉換，處理欄位型別、缺值與快照保存，建立後續章節共用的資料基礎。

### 第三章

[第三章：排序與搜尋：把「找不到」變成可解的問題](chapters/ch03-sorting-and-searching/index)

示範穩定排序與二分搜尋，讓「先整理、再定位」這件事變成可驗證的實作流程。

### 第四章

[第四章：雜湊與去重：把重複資料變成可管理的清單](chapters/ch04-hashing-and-deduplication/index)

把雜湊指紋、重複判定與穩定去重串成一條資料整理流程，適合處理名單合併、客戶清冊與匯入資料清理。

### 第五章

[第五章：圖與路徑：從流程網路找到最短可行路線](chapters/ch05-graphs-and-routing/index)

把節點、邊、權重與最短路徑觀念帶進日常決策，適合處理通勤規劃、簽核流程與任務依賴鏈。

### 第六章

[第六章：排程與資源分配：把撞期工作排成可執行的一天](chapters/ch06-scheduling-and-allocation/index)

把會議、訪談與外勤安排轉成區間排程問題，先找出互不衝突的可行清單，再進一步用加權排程挑出總效益最高的安排。

### 第七章

[第七章：預算與組合：在有限資源下挑出最值得的方案](chapters/ch07-budgeting-and-combinations/index)

把採購、課程、工具訂閱或功能排程轉成有限預算下的組合選擇，學會用動態規劃找出總價值最高的方案。

### 第八章

[第八章：優先佇列與即時任務：讓插單工作也能穩定處理](chapters/ch08-priority-queues-and-triage/index)

把客服工單、突發支援與臨時需求轉成優先佇列問題，學會在不打亂整體節奏的前提下，先處理最急迫的任務。

## 建議閱讀順序

若你是第一次閱讀，建議依序從前言與前三章往下看；若你是想直接評估 repo 成熟度，可以同步打開 `examples/` 與 `tests/`，對照章節內容與實作。

## 章節導覽

- [前言](preface)
- [第一章：用演算法思維整理日常工作](chapters/ch01-algorithmic-thinking/index)
- [第二章：資料格式與表格：從 CSV 到 Parquet 與 NumPy 檔](chapters/ch02-data-formats-and-tables/index)
- [第三章：排序與搜尋：把「找不到」變成可解的問題](chapters/ch03-sorting-and-searching/index)
- [第四章：雜湊與去重：把重複資料變成可管理的清單](chapters/ch04-hashing-and-deduplication/index)
- [第五章：圖與路徑：從流程網路找到最短可行路線](chapters/ch05-graphs-and-routing/index)
- [第六章：排程與資源分配：把撞期工作排成可執行的一天](chapters/ch06-scheduling-and-allocation/index)
- [第七章：預算與組合：在有限資源下挑出最值得的方案](chapters/ch07-budgeting-and-combinations/index)
- [第八章：優先佇列與即時任務：讓插單工作也能穩定處理](chapters/ch08-priority-queues-and-triage/index)