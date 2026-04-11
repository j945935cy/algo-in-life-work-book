# examples

此資料夾放置各章節的可執行範例程式。

## 章節對照

- `examples/ch01/time_log.py`：待辦清單排序與時間紀錄範例
- `examples/ch02/data_transform.py`：資料格式轉換與快照輸出
- `examples/ch03/sorting_search.py`：穩定排序與二分搜尋
- `examples/ch04/deduplication.py`：資料指紋與穩定去重
- `examples/ch05/routing.py`：加權圖最短路徑規劃
- `examples/ch06/scheduling.py`：區間排程、加權排程與衝突檢查
- `examples/ch07/budgeting.py`：有限預算下的方案組合與最佳化選擇

## 執行方式

```powershell
python -m examples.ch01.time_log --help
python -c "from examples.ch05.routing import shortest_route"
python -c "from examples.ch06.scheduling import select_highest_value_tasks"
python -c "from examples.ch07.budgeting import select_best_portfolio"
```
