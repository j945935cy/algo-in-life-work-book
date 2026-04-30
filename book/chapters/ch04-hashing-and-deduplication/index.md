---
title: 第四章：雜湊與去重：把重複資料變成可管理的清單
short_title: 第四章：雜湊與去重
---

# 第四章：雜湊與去重：把重複資料變成可管理的清單

::: advisory
本章目標
:::

- 理解雜湊值如何把一筆資料「壓縮」成固定長度的指紋，並用於快速比對
- 了解雜湊碰撞的概念，以及為什麼選對雜湊函式很重要
- 用 Python 建立穩定且可重現的去重流程，並保留原始輸入順序
- 處理大小寫不一致、前後空白、欄位順序不同等常見髒資料問題

::: advisory
情境與限制
:::

- 情境：你要整併多份名單、匯入客戶資料，或清理表單填答紀錄
- 輸入：由字典組成的資料列，每列可能欄位格式不一致、大小寫不同、夾帶空白
- 輸出：去重後資料、重複索引與可重現的指紋值
- 限制：必須保留第一筆有效紀錄，不能因欄位順序不同就誤判為不同資料

::: advisory
可重現規則
:::

- 本章程式碼位置： `examples/ch04/`
- 本章核心模組： `examples/ch04/deduplication.py`
- 測試： `pytest -q tests/test_ch04_hashing_and_dedup.py`
- 典型用途：合併名單、會員資料清理、重複表單去除

## 去重為什麼比想像中難

直覺上，去除重複聽起來很簡單：找出一樣的資料，刪掉後面的。

但真實資料通常長這樣：

```
{"email": "amy@example.com", "name": "Amy"}
{"email": " AMY@example.com ", "name": "amy"}
```

這兩筆是同一個人嗎？幾乎肯定是。但如果直接用字串比對，因為大小寫不同、前後有空白，程式會認為它們是兩筆不同資料。

更麻煩的情況是：

```
{"name": "Alice Chen", "email": "alice@example.com"}
{"email": "alice@example.com", "name": "Alice Chen"}
```

欄位順序不同，但值完全相同。若程式把整列序列化後直接比對，同樣會誤判。

這就是為什麼去重需要一個「先正規化、再比對」的流程，而不是直接比較原始資料。

## 什麼是雜湊

雜湊（hashing）是一種把任意長度的資料，轉換成固定長度字串的函式。

以 SHA-256 為例：

```python
import hashlib

data = "alice@example.com"
fingerprint = hashlib.sha256(data.encode("utf-8")).hexdigest()
# "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
```

不管輸入多長，SHA-256 永遠輸出 64 個十六進位字元（256 bits）。這個固定長度的輸出就叫做**指紋**（fingerprint）。

雜湊的三個核心特性：

| 特性 | 說明 |
| --- | --- |
| **固定長度** | 輸出長度不變，方便儲存和比對 |
| **確定性** | 相同輸入永遠產生相同輸出 |
| **不可逆** | 無法從指紋反推原始資料（單向函式） |

## 雜湊碰撞是什麼

雜湊碰撞（hash collision）是指兩筆**不同的輸入**，卻產生了**相同的雜湊值**。

理論上，任何有限輸出的雜湊函式都可能發生碰撞，因為輸入是無限的，但輸出是有限的。

但實際上，好的雜湊函式（如 SHA-256）的碰撞概率極低——低到在你的整個資料清理工作生涯中，幾乎不會發生。

相比之下，簡單的雜湊函式（如直接取餘數 `len(s) % 100`）碰撞率就很高，因為輸出空間太小，很容易讓兩個不同字串映射到同一個值。

這就是為什麼本章選用 SHA-256，而不是自己寫一個簡單 hash：**穩定、碰撞率極低、且跨語言可重現**。

## 為什麼不直接比對欄位，而是用雜湊

直接比對欄位也可以去重，那為什麼要用雜湊？

| 方法 | 適用情況 | 缺點 |
| --- | --- | --- |
| **直接比對欄位值** | 資料乾淨、欄位結構固定 | 欄位一多，邏輯容易複雜；無法做快速查找 |
| **雜湊指紋比對** | 欄位組合多、資料量大 | 有極低碰撞率（實務可忽略） |

關鍵優勢在於：雜湊比對是 **O(1)**。不論你要比對 3 個欄位還是 30 個欄位，只需比對一個固定長度字串，再加上集合（set）查找，整體去重的時間複雜度是 **O(n)**。

## 正規化：去重前的必要步驟

在產生指紋之前，必須先對欄位值做正規化，讓「實質相同」的資料能產生相同的指紋。

本章使用的正規化規則：

1. 去除前後空白（`.strip()`）
2. 轉為小寫（`.lower()`）
3. 合併中間多餘的空格（`" ".join(value.split())`）
4. `None` 值視為空字串

```python
def _normalize_value(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.strip().lower().split())
    return str(value).strip().lower()
```

正規化之後，`" AMY@example.com "` 和 `"amy@example.com"` 都會變成 `"amy@example.com"`，再計算雜湊時就能得到相同指紋。

## 保留輸入順序的去重

去重有一個容易忽略的細節：**保留原始順序**。

如果你直接用 `set()` 去重，順序就不見了。但在合併客戶名單、清理報名表這類場景，通常第一筆才是最可信的資料（例如最早填寫的表單），後來的才是重複填答。

本章的做法：用 `seen` 集合記錄已看過的指紋，遇到重複就跳過，但只 append 第一次出現的記錄：

```python
seen: set[str] = set()
unique_records = []

for record in records:
    fingerprint = record_fingerprint(record, keys)
    if fingerprint in seen:
        continue
    seen.add(fingerprint)
    unique_records.append(record)
```

這樣的時間複雜度是 O(n)，而且每次執行結果都一樣——這就是「可重現」的去重。

## 實作範例

請參考 `examples/ch04/deduplication.py`。請在專案根目錄執行程式，以確保路徑正確。

```python
from examples.ch04.deduplication import deduplicate_records, find_duplicate_indices

records = [
    {"email": "amy@example.com", "name": "Amy"},
    {"email": "bob@example.com", "name": "Bob"},
    {"email": " AMY@example.com ", "name": "amy"},   # 與第 0 筆重複
    {"email": "bob@example.com", "name": " Bob "},   # 與第 1 筆重複
]

# 找出重複的索引（保留第一筆）
print(find_duplicate_indices(records, ["email"]))
# [2, 3]

# 去重後的乾淨清單
clean = deduplicate_records(records, ["email"])
# [{"email": "amy@example.com", ...}, {"email": "bob@example.com", ...}]
```

示範流程包含：

- 將 email、姓名等欄位做大小寫與空白正規化
- 為指定欄位組合產生 SHA-256 指紋（與欄位順序無關）
- 找出重複資料所在索引位置
- 保留第一筆紀錄並輸出乾淨清單，維持原始輸入順序