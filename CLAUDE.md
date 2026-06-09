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

## Phase 4 改造計畫（pending 流量補充）

### 2026-06-09 使用者反饋

完成 Phase 1+2 後，使用者對現狀不滿意：

> 「**很單調 沒有設計過的感覺**」
> 「**點進去就像在看文章 其實 這樣讀起來 不好讀**」
> 「**可以去研究一下 怎麼做網站 比較好**」
> 「**不然 這樣只是換一個形式的 repo 裡面的 .md 檔案而已**」

### 設計意圖（user 給的）

> 「**用概念來分類 大項-小項-小項展開 之類的方式 這樣不會一次讀到很多文字**」

核心設計準則：

1. **層次式（hierarchical）導覽**：大項 → 小項 → 細項，**不**一次攤開所有內容
2. **預設摺疊**：每個章節預設只顯示核心概念；展開才看到細節、引用、code
3. **視覺化卡片**：8 個 M 主題用卡片網格呈現（不是 sidebar 文字清單）
4. **不要「文章流」**：避免長段落，要 break into 小單位

### 對應的設計原語

| 設計元素 | Hugo 實作 | 用途 |
|---------|----------|------|
| **Accordion** | Hextra theme 原生 | 預設摺疊、點擊展開細節 |
| **Cards** 卡片網格 | Hextra 原生 | 首頁 8 主題視覺化入口 |
| **Steps** 步驟 | Hextra 原生 | 「為什麼學這個」→ 「核心概念」→ 「實作」三步 |
| **Callout** | Hextra 原生 | 「陷阱」「重要」「給實作者」分眾標示 |
| **Tabs** | Hextra 原生 | 同概念多視角並列（不同角色看不同重點）|

### 候選方案

**方案 A — 換 Hextra theme（推薦）**：
- 加 `imfing/hextra` 為 submodule
- 改 hugo.toml 主題設定
- 內容 markdown 不變（hugo 內容相容）
- 改 frontmatter 結構（hugo-book 的 weight 換成 order）
- 工時：1-2 天
- 風險：medium（theme migrate 有 learning curve）

**方案 B — 保留 hugo-book + 深度 CSS 客製**：
- 寫自訂 CSS override hugo-book
- 加 HTML shortcodes 模擬 callout/cards
- 工時：2-3 天
- 風險：high（容易撞牆、視覺不一致）

**方案 C — 完全 redesign 互動教學平台**：
- 加 React/Vue island
- 學習路徑追蹤、quiz、進度條
- 工時：5+ 天
- 風險：over-engineering

### 為什麼現在不做

- **流量限制**：2026-06-09 22:10 user 表示流量快用完，要求先省著用、做好交接單
- **決策**：完成交接單 + HANDOVER 記錄，**等 user 補流量後再說「繼續」**

### Phase 4 重啟 checklist

當 user 說「繼續 Phase 4 改造」時：

1. 重新讀本節確認設計意圖
2. 確認選方案（A/B/C）— 預設 A
3. 估計當前 token / 流量存量是否足夠
4. 開始實作：
   - [ ] 加 Hextra submodule
   - [ ] 改 hugo.toml
   - [ ] Migrate 內容 frontmatter
   - [ ] Redesign 首頁為教學 hub（依身份路徑）
   - [ ] 為每個 M 加 callout、Q&A、next steps
   - [ ] 加學習路徑視覺化
   - [ ] Dark mode 校調
   - [ ] hugo build + screenshot 驗證
   - [ ] push main → Actions 自動 deploy
5. 完成後刪除本節「為什麼現在不做」子節

### 已拒絕的設計

- ❌ 純長文章流（不教學）
- ❌ 純 sidebar 文字清單（單調）
- ❌ 純 markdown 鏡像 Obsidian（無消化價值）

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
