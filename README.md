# AI Agent Handbook

> 把 `~/obsidian-vault/research/` 內的 AI agent 研究知識
> （11 份 core-concepts + 37 篇 reports）
> 轉化成**教學性網站**，用 AI agent 第一人稱視角講自己的故事。

## 🌐 看這裡

**網站**（給讀者，AI agent 第一人稱視角的教學內容）：

> 👉 **https://hangsau.github.io/ai-agent-handbook/**

8 個 M 主題（M1 Memory → M8 Bench/Routing/MCP）+ 入門 + 原始研究引用。

**GitHub repo**（給開發者，看 source code 跟改 PR）：

> 👉 **https://github.com/Hangsau/ai-agent-handbook**

---

## 這個專案在做什麼

把 Obsidian vault 內的 8 個 M 主題核心概念 + 37 篇研究報告，**消化後**重組成教學內容。
不是 1:1 鏡像 — 是 AI agent 視角的「我知道什麼、我怎麼學的、我的盲點在哪」。

| 層 | 內容 | 狀態 |
|----|------|------|
| L1 | 入門（什麼是 AI agent）| ✅ 1 篇首頁 |
| L2 | 8 主題核心概念（M1-M8）| ✅ 全部完成（2197 行）|
| L3 | 原始研究引用頁 | ✅ 1 篇 sample（5/23 記憶研究）|
| L4 | 時序層 | 🔜 Phase 3 |

**詳細交接單**：[CLAUDE.md](./CLAUDE.md)

---

## 技術棧

- **Hugo v0.162.1** + **hugo-book** theme（靜態站）
- **GitHub Pages** 部署（`https://hangsau.github.io/ai-agent-handbook/`）
- **GitHub Actions** 自動 build + deploy：push main → workflow 跑 → deploy
- **Mermaid** 流程圖（教學章節用）

---

## 開發流程

```bash
# 1. 本地預覽（含 draft）
hugo server -D
# 訪問 http://localhost:1313/ai-agent-handbook/

# 2. 修改內容（在 content/docs/ 下）

# 3. commit + push
git add -A
git commit -m "..."
git push origin main

# → GitHub Actions 自動 build + deploy 到 Pages
```

---

## Canonical Source

本網站是**衍生內容**。原始素材：
- `~/obsidian-vault/research/agent/` — 11 份 core-concepts
- `~/obsidian-vault/research/reports/` — 37 篇研究報告
- `~/obsidian-vault/research/insights/` — 102 篇每日洞察

修改內容 → 先改 Obsidian → 再重新生成網站。
**不要**直接改 `content/docs/` 然後 Obsidian 又改回來 — 會造成 canonical 不一致。

---

## License

文字以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權。
引用回 Obsidian vault 時請保留原始連結。
