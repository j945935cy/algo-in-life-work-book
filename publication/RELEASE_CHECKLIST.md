# Repo 發布檢查清單

## 內容完整性

- [ ] 書稿首頁、前言與已完成章節摘要已同步更新
- [ ] `book/myst.yml` 的 TOC 與實際章節一致
- [ ] 每一章都有對應的 `examples/` 範例與 `tests/` 測試

## 技術驗證

- [ ] 本地執行 `pytest -q` 全部通過
- [ ] 本地執行 `& .\scripts\build_book.ps1` 可成功建書
- [ ] 本地執行 `& .\scripts\preview_book.ps1` 可正常預覽
- [ ] GitHub Actions 的 CI 與 Pages workflow 都顯示成功

## 對外資訊

- [ ] [README.md](../README.md) 的快速開始、章節進度與預覽方式為最新狀態
- [ ] [CITATION.cff](../CITATION.cff) 的作者資訊已確認為正式發布用資料
- [ ] [LICENSE](../LICENSE) 的版權人名稱已確認
- [ ] GitHub Pages 網址與 repo 描述已更新到最新版本

## 發布收尾

- [ ] 確認 `.gitignore` 沒有漏掉建置產物
- [ ] 不需要納入版控的輸出檔未被提交
- [ ] 發布 tag、release note 與里程碑版本號已更新