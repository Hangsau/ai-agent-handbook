# AI Agent Handbook — Project CLAUDE.md

> 跨 session 接手這個 project 時，先讀這份。
> **這是交接單，不是 README**（README 給人看、CLAUDE.md 給 AI 看）。
> 最後更新：2026-06-09

---

## 目標

把 `/root/obsidian-vault/research/` 內的 AI agent 研究知識
（11 份 core-concepts + 37 篇 reports + 102 篇 insights），
轉化成**教學性網站**，讓讀者從「不知道 AI agent」到「理解 2026 主流範式」。

**核心精神**：消化後重新呈現，不是 1:1 鏡像 Obsidian。
**調性**：AI agent 第一人稱視角（從 agent 角度看自己）。
**會持續長大**：知識庫會增加，網站要能動態維護。

---

## 技術棧

| 元件 | 選擇 | 原因 |
|------|------|------|
| 靜態站生成器 | Hugo v0.162.1+extended | Build 速度、Markdown 原生、GitHub Pages 一鍵部署 |
| 主題 | hugo-book | 教學文件導向、UI 極簡、search 內建、左側 sidebar 自動 |
| 圖表 | Mermaid | 流程圖/時序圖原生 Hugo shortcode 支援 |
| 部署 | GitHub Pages | `peaceiris/actions-hugo` action |
| Build trigger | push 到 main → GitHub Actions | — |

---

## 內容架構（4 層）

```
L1 入門層        — 給「不知道 AI agent 是什麼」的讀者
  ├─ 什麼是 AI Agent
  ├─ Agent vs LLM vs Workflow
  └─ 為什麼 2026 是 agent 元年

L2 核心概念層    — 基於 8 個 M 主題
  ├─ M1 Memory + Context
  ├─ M2 Multi-Agent Coordination
  ├─ M3 Self-Improvement
  ├─ M4 Agent Planning
  ├─ M5 Meta-Agent Supervision
  ├─ M6 Code vs Tool-based Agents
  ├─ M7 Observability + Trace
  └─ M8 Benchmarks + Routing + MCP Security

L3 原始研究層    — 想深挖的人
  └─ 37 篇研究報告（reports/）的引用頁 + 完整摘要

L4 時序層        — 2026 H1 AI agent 領域全景
  └─ 時間軸 + 關鍵論文 / 系統發表
```

**Phase 1 範圍**（現在）：L1 首頁 + L2 M1 Memory + L3 1 篇 sample
**Phase 2 範圍**（未來）：L2 其餘 7 個 M + L3 完整 37 篇
**Phase 3 範圍**（未來）：L4 時序層 + 守護者自動消化

---

## 內容 / 資料來源（canonical source）

| 原料 | 路徑 | 角色 |
|------|------|------|
| 8 份 core-concepts 整合文 | `~/obsidian-vault/research/agent/*-core-concepts.md` | L2 教學文基底 |
| 閱讀導覽 | `~/obsidian-vault/research/agent/agent-knowledge-map.md` | L1 首頁基底 |
| 37 篇研究報告 | `~/obsidian-vault/research/reports/*.md` | L3 引用頁原料 |
| 102 篇每日洞察 | `~/obsidian-vault/research/insights/2026-{05,06}/*.md` | L4 時序軸原料 |

**規則**：canonical 永遠是 Obsidian，網站是 derived view。修改內容 → 先改 Obsidian → 再重新生成網站。

---

## 維護機制

### 開發流程

```bash
cd ~/projects/ai-agent-handbook
hugo server -D          # 本地預覽（http://localhost:1313）
# 改內容
hugo                    # 產生 public/
git add . && git commit -m "..." && git push   # 觸發 GitHub Actions
```

### Phase 1 → Phase 2 升級條件

- Phase 1 三頁上線，讀者反饋 OK
- Obsidian vault 內的整合文（M2-M8）已被我或 Hermes agent 確認完整
- 守護者監聽 `~/obsidian-vault/research/` 新檔案機制實作

### Phase 3 自動維護（規劃中）

- 守護者監聽 vault 新研究報告 → 觸發我（Claude）做消化
- 消化結果以 PR 形式提交到本 repo
- 自動 build + 部署

---

## 已知問題

1. **M# 編號不一致**：`agent-knowledge-map.md` v2 跟 `agent-core-concepts.md` 內的 M# 編號不一致（v2: M1=M2=MultiAgent, v1: M2=Governance）。**以 v2 為準**。
2. **M6 code-vs-tool 整合文較薄**（127 行 vs M1 的 ~500 行），未來可能要回到原始研究報告補強。
3. **「互動」目前只規劃 Mermaid 流程圖**，未來可加 Hugo shortcode 嵌入示意圖/CodePen iframe。
4. **GitHub Pages deploy config** 還沒設定（Phase 1 只本地看）。

---

## 不要做的事

- ❌ **不要 1:1 鏡像 Obsidian 內容** — 網站是消化後的教學，不是 mirror
- ❌ **不要寫還沒準備好的 M 主題** — 用 `Coming soon` placeholder 標記
- ❌ **不要在 Phase 1 寫自動消化 pipeline** — 那是 Phase 3 的事
- ❌ **不要碰 Obsidian vault 的內容** — 永遠只讀不改
- ❌ **不要裝 AUR helper**（yay/paru）— 維持系統乾淨（CLAUDE.md §6.1）
- ❌ **不要不主動 commit** — 改完先放著等 review（CLAUDE.md §6.1），本 project 例外可以 stage 但不 push main
