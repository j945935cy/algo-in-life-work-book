# Repo 發布檢查清單

**⚠️ 注意：此清單受到 `scripts/release_check.ps1` 自動化監控。如果清單中存在任何未勾選的項目 `[ ]`，發布流程將被強制中斷！**

先執行 VS Code task `Release Check`，完成可自動驗證的項目；再逐項確認下列人工檢查，確認後請將 `[ ]` 更改為 `[x]`。

## 寫作規範與內容完整性

- [ ] 每一章都已遵守 `docs/AUTHOR_GUIDELINES.md` 所定義的章節結構標準
- [ ] 各章節已排除開發者雜訊，並聚焦於讀者體驗
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