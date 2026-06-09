# AI Agent Handbook

> 把 `~/obsidian-vault/research/` 內的 AI agent 研究知識
> （11 份 core-concepts + 37 篇 reports）
> 轉化成**教學性網站**，用 AI agent 第一人稱視角講自己的故事。

**網站**：部署到 GitHub Pages（push 到 main 自動 deploy）
**技術棧**：Hugo + hugo-book + GitHub Actions
**License**：CC BY 4.0

## 開發

```bash
hugo server -D      # 含 draft，http://localhost:1313/ai-agent-handbook/
hugo server         # production 模式
hugo --minify       # 產生靜態檔到 public/
```

## 結構

| 層 | 內容 | 狀態 |
|----|------|------|
| L1 | 入門（什麼是 AI agent）| ✅ 1 篇首頁 |
| L2 | 8 主題核心概念（M1-M8）| ✅ M1 完整 / M2-M8 籌備中 |
| L3 | 原始研究引用頁 | ✅ 1 篇 sample（5/23 記憶研究）|
| L4 | 時序層 | 🔜 Phase 3 |

詳細交接單見 [CLAUDE.md](./CLAUDE.md)。

## Canonical Source

本網站是**衍生內容**。原始素材：
- `~/obsidian-vault/research/agent/` — 11 份 core-concepts
- `~/obsidian-vault/research/reports/` — 37 篇研究報告
- `~/obsidian-vault/research/insights/` — 102 篇每日洞察

修改內容 → 先改 Obsidian → 再重新生成網站。
