# examples

此資料夾放置各章節的可執行範例程式。

## 章節對照

- `examples/ch01/time_log.py`：待辦清單排序與時間紀錄範例
- `examples/ch02/data_transform.py`：資料格式轉換與快照輸出
- `examples/ch03/sorting_search.py`：穩定排序與二分搜尋
- `examples/ch04/deduplication.py`：資料指紋與穩定去重
- `examples/ch05/routing.py`：加權圖最短路徑規劃

## 執行方式

```powershell
python -m examples.ch01.time_log --help
python -c "from examples.ch05.routing import shortest_route"
```
