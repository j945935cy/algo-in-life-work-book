# algo-in-life-work-book

這是一個以「日常與職場的演算法應用」為主題的書籍專案。它不只是存放章節草稿，而是把書稿、範例程式、測試、資料與建站流程整合在同一個 repo 中，讓每一章都能被閱讀、執行與驗證。

## 目前進度

- 已完成前言與第 1 到第 7 章書稿骨架
- 已完成 7 組對應範例程式
- 已建立 7 組章節測試，`pytest -q` 全綠
- 已完成新版 Jupyter Book / MyST HTML 本地建站
- 已補上 GitHub Pages 發布流程

## 成果展示重點

- 書稿首頁：`book/index.md`
- 前言：`book/preface.md`
- 章節內容：`book/chapters/`
- 執行範例：`examples/`
- 測試：`tests/`
- HTML 站點輸出：`book/_build/html/`

## 專案結構

- `book/`：書稿、章節與建站設定
- `examples/`：各章節可直接執行的範例程式
- `src/`：可重用核心模組
- `tests/`：pytest 單元測試
- `data/`：原始、處理後與合成資料
- `scripts/`：建書與資料生成腳本
- `publication/`：出版與授權相關資產

## 快速開始

```powershell
# 安裝相依套件
python -m pip install -r requirements.txt
python -m pip install -e .

# 執行第一章範例
python -m examples.ch01.time_log --help

# 執行第二章範例
python -c "from examples.ch02.data_transform import transform_file; print(transform_file)"

# 執行第三章範例
python -c "from examples.ch03.sorting_search import stable_sort, binary_search; print(stable_sort([3, 1, 2]), binary_search([1, 2, 3], 2))"

# 執行第四章範例
python -c "from examples.ch04.deduplication import deduplicate_records; print(deduplicate_records([{'email': 'A@EXAMPLE.COM '}, {'email': 'a@example.com'}], ['email']))"

# 執行第五章範例
python -c "from examples.ch05.routing import shortest_route; graph={'A': {'B': 4, 'C': 2}, 'B': {'D': 5}, 'C': {'B': 1, 'D': 8}, 'D': {}}; print(shortest_route(graph, 'A', 'D'))"

# 執行第六章範例
python -c "from examples.ch06.scheduling import select_highest_value_tasks; tasks=[{'name':'晨會','start':9,'end':10,'value':2},{'name':'訪談','start':9,'end':12,'value':9},{'name':'報表','start':10,'end':11,'value':2}]; print(select_highest_value_tasks(tasks))"

# 執行第七章範例
python -c "from examples.ch07.budgeting import select_best_portfolio; items=[{'name':'廣告','cost':5,'value':9},{'name':'客服訓練','cost':4,'value':7},{'name':'報表工具','cost':3,'value':4}]; print(select_best_portfolio(items, 8))"

# 執行全部測試
pytest -q
```

## 建立 HTML 書站

```powershell
pwsh -File .\scripts\build_book.ps1
```

建置完成後，請不要直接雙擊 `book/_build/html/index.html` 或其他子頁 HTML 檔案。

MyST 產生的靜態站點需要透過 HTTP 伺服器預覽，否則瀏覽器會把 `/build/...` 這類網站根路徑誤解成磁碟根目錄，進而出現 `BASE_URL` 錯誤提示。

## 本地預覽書站

```powershell
pwsh -File .\scripts\preview_book.ps1
```

接著用瀏覽器開啟 `http://127.0.0.1:8000/`。

若要在發布前做一鍵檢查，可執行 VS Code task `Release Check`，或直接執行下列指令：

```powershell
pwsh -File .\scripts\release_check.ps1
```

## 發布到 GitHub Pages

repo 推送到 `master` 後，GitHub Actions 會自動執行 `.github/workflows/deploy-pages.yml`，建出帶有正確 `BASE_URL` 的靜態站點並部署到 GitHub Pages。
