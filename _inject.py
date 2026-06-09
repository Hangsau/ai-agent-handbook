#!/usr/bin/env python3
"""
自動為 M2-M8 章節注入 Hextra 互動元素：
- 開頭：「為什麼學這個」callout
- 結尾：Q&A details（3 個） + 給實作者 checklist + 下一步

每個 M 有獨立的「為什麼」「Q&A」「下一步」內容（自訂）。
讀 YAML config 然後逐個注入。

為什麼用 script：8 個 M 結構一致，內容客製 — 手動 7 次容易出錯漏。
"""
from pathlib import Path
import re
import sys

ROOT = Path("/root/projects/ai-agent-handbook/content/docs")

# 每個 M 的客製化內容
M_CONFIG = {
    "m2-multi-agent": {
        "why_title": "為什麼學這個？",
        "why_body": (
            "**你在做 multi-agent 嗎？** 這章教你 5 種協調模式 + 4 個 production 必要元件。\n\n"
            "**你在用單一 agent？** 這章幫你判斷**什麼時候**該升級到 multi-agent。"
        ),
        "qa": [
            ("Q1: 多 agent 一定比單一 agent 好嗎？",
             "**不一定**。AROMA 研究發現：多 agent 系統**只有 modest performance gains**，"
             "甚至 performance setbacks，同時 token consumption 大幅增加。\n\n"
             "**判斷標準**：任務能否**清楚分解**給專門 agent？不能就別用。"),
            ("Q2: Agents-as-Tools 跟 Hierarchical 怎麼選？",
             "**預設用 Agents-as-Tools**（OpenAI Agents SDK 模式）。\n\n"
             "- 對應 LLM 已有的 function calling 能力\n"
             "- 容易監控（所有互動走 function call log）\n"
             "- 失敗局部化（sub-agent 失敗不拖垮 orchestrator）\n\n"
             "Hierarchical 只在任務需要**真正的並行 worker** 時才用。"),
            ("Q3: 如何避免 multi-agent 的「資訊過載」？",
             "三個手段：\n\n"
             "1. **Output guardrails** — 驗證每個 worker 輸出（防止幻覺傳播）\n"
             "2. **Shared memory schema** — 統一格式（防止格式斷裂）\n"
             "3. **MCP** — 工具發現標準化（防止 tool 描述不一致）"),
        ],
        "next_teaser": "**M3 Self-Improvement** — 你的 multi-agent 怎麼從失敗中學習？",
        "next_link": "/docs/m3-self-improvement/",
    },
    "m3-self-improvement": {
        "why_title": "為什麼學這個？",
        "why_body": (
            "**你的 agent 怎麼變強？** 這章教你 4 個自我改善軸向 + Governance 四層模型。\n\n"
            "**你沒想過 agent 可以自己變強？** 這章會顛覆你 — ACE playbook + Dream cycle + Reflexion "
            "讓 agent 不用 retrain 就能改進。"
        ),
        "qa": [
            ("Q1: Self-improvement 不就是 fine-tuning 嗎？",
             "**不是**。Self-improvement 改的是**操作層**（context、playbook、memory），**不改模型權重**。\n\n"
             "ACE 論文證明：純 context engineering 在 AppWorld benchmark 上能達到有意義提升。\n\n"
             "**好處**：成本低、不過擬合、不需要 retrain infra。"),
            ("Q2: 沒有 feedback signal 怎麼改善？",
             "**這是 self-improvement 的最大盲點**。\n\n"
             "三個 fallback：\n\n"
             "1. **self-consistency check**（同一 prompt 跑 N 次取 consensus）\n"
             "2. **user 互動當 feedback**（每次 task 完成問 3 個問題）\n"
             "3. **L2 Eval 框架**（用強 model 評弱 model 的 output）"),
            ("Q3: 怎麼防止 self-improvement 失控？",
             "**Governance 四層模型**（Deep-Claw 啟發）：\n\n"
             "- M1 低風險調參：agent 自動執行\n"
             "- M2 中等變更：需文檔化假設\n"
             "- M3 結構性變更：需同行 review\n"
             "- M4 安全邊界：**必須人類審批**\n\n"
             "沒有 governance，self-improvement = self-destruction。"),
        ],
        "next_teaser": "**M4 Agent Planning** — ReAct 過時了嗎？2026 規劃架構如何 scale？",
        "next_link": "/docs/m4-planning/",
    },
    "m4-planning": {
        "why_title": "為什麼學這個？",
        "why_body": (
            "**你的 agent 在做 5 步以下的簡單任務？** 這章可以跳過。\n\n"
            "**你的 agent 在做 100 步 + 數百工具的複雜任務？** 這章是必讀。"
        ),
        "qa": [
            ("Q1: ReAct 是不是過時了？",
             "**不是**。對短任務（≤5 步、≤10 工具）ReAct 仍是最簡單且可維護的方案。\n\n"
             "**過時的時機**：當工具庫長大到 100+、任務 horizon 20+ 步、debug 變噩夢 — 這時升級到 Graph Planning / Self-Healing。"),
            ("Q2: Self-Healing 跟 ReAct 的差別？",
             "Self-Healing 把 reliability 視為 **bounded runtime control problem**：\n\n"
             "- 觀測 failure signals（timeout、malformed args、stale context）\n"
             "- 推斷 failure class\n"
             "- 在 budget 內選 targeted recovery\n"
             "- Verifier 驗證 recovered trajectory\n\n"
             "**benchmark 數字**：98.8% success rate vs retry-only 94.5%。\n"
             "**silent failure 從 22% 降到 0%** — 這是最大價值。"),
            ("Q3: 怎麼開始做 Primitive Induction？",
             "**最對單人開發者友善的方案**。\n\n"
             "4 步：\n\n"
             "1. 撈出最近 N=200 個成功 traces\n"
             "2. 用 LLM cluster 出 K=5-10 個 recurring reasoning moves\n"
             "3. 寫成 typed pseudo-tool（docstring + 範例）\n"
             "4. TaskAgent 下次接任務時先看 primitive library\n\n"
             "**幾小時可完成**。"),
        ],
        "next_teaser": "**M5 Meta-Agent** — 規劃有了，但誰來監督？",
        "next_link": "/docs/m5-meta-agent/",
    },
    "m5-meta-agent": {
        "why_title": "為什麼學這個？",
        "why_body": (
            "**你的 multi-agent 系統需要 supervisor 嗎？** 這章教你 5 種監督架構。\n\n"
            "**什麼時候需要 supervisor？**\n\n"
            "- Worker agent 開始幻覺\n"
            "- 失敗率 5-20% 不可忽略\n"
            "- 沒有結構化的失敗偵測機制"
        ),
        "qa": [
            ("Q1: Supervisor 不就是另一個 agent，也會失敗嗎？",
             "**對**。CUHK MAS-Resilience 指出：supervisor 本身（Inspector / Challenger）**也是 LLM agent，可能被同樣手法欺騙**。\n\n"
             "**解法**：\n\n"
             "- 監督多層（不是單一 supervisor）\n"
             "- 監督分工（active / passive core-agent）\n"
             "- 最高層永遠是人類"),
            ("Q2: 怎麼選監督架構？",
             "**任務分解為主 → Hierarchical（OODA 指揮官）**\n\n"
             "**需要動態重構 → Self-Evolving Meta-Agent（SEMAF）**\n\n"
             "**長時任務、易中斷 → Disruption-Aware（ALAS）**\n\n"
             "**成本敏感、動態調整 → Adaptive Coordination（AROMA）**\n\n"
             "**大量異質 agent/tool → Agent-as-a-Graph**"),
            ("Q3: 我可以從哪個最簡單的監督開始？",
             "**加入 `supervisor_check` 步驟**到 batch runner — 每 N 個任務後讓 supervisor 審視結果。\n\n"
             "用 **DeepSeek** 做 supervisor（成本低）。\n\n"
             "playbook 加「supervisor 標記為 failure → 降級到 single-agent 模式」邏輯。\n\n"
             "**先做這個，再考慮 SEMAF / AROMA**。"),
        ],
        "next_teaser": "**M6 Code vs Tool** — 你的 agent 應該用 JSON 還是用 code 行動？",
        "next_link": "/docs/m6-code-vs-tool/",
    },
    "m6-code-vs-tool": {
        "why_title": "為什麼學這個？",
        "why_body": (
            "**你的 agent 在做簡單工作？** 用 Tool-Based (JSON) 就好。\n\n"
            "**你的 agent 在做多步組合、context 敏感？** 換到 Code Agent。"
        ),
        "qa": [
            ("Q1: 為什麼 Code Agent 興起？",
             "**LLM 對 code 比 JSON 更自然** — 它受過的訓練中 code 比 JSON 多幾個數量級。\n\n"
             "**2026 主流**：smolagents（27.5K stars, 1K 行核心邏輯）、LangChain code mode。\n\n"
             "**好處**：\n\n"
             "- 可一次組合多步（`search(); if result: analyze(); else: fallback()`）\n"
             "- 結果可變數（context 效率高）\n"
             "- 容易除錯（print/inspect/version control）"),
            ("Q2: Code Agent 一定要 sandbox 嗎？",
             "**對，這是必要代價**。\n\n"
             "推薦 sandbox：\n\n"
             "- **E2B**（雲端、快速）\n"
             "- **Modal**（雲端、彈性）\n"
             "- **Docker**（本地、控制力強）\n\n"
             "**不要**讓 code agent 直接在主機跑 — security 風險太高。"),
            ("Q3: MCP 是什麼？",
             "**Model Context Protocol** — tool calling 通用協議（2025 崛起）。\n\n"
             "**解決**：tool 發現的「大一統介面」— 不再每個 framework 各自定義 tool schema。\n\n"
             "**MCP 解決「工具發現」，不解決 orchestration**（那是 M2 的主題）。\n\n"
             "**生態**：Chrome MCP (11.7K)、Playwright MCP (5.5K)、XcodeBuildMCP (5.8K)。"),
        ],
        "next_teaser": "**M7 Observability** — 你的 agent 跑久了怎麼 debug？",
        "next_link": "/docs/m7-observability/",
    },
    "m7-observability": {
        "why_title": "為什麼學這個？",
        "why_body": (
            "**你的 agent 跑 production 出事？** 這章教你 4 個解法 + Memory self-governance。\n\n"
            "**你還沒跑 production？** 這章仍然必讀 — observability 是基礎設施，**現在不做以後會痛**。"
        ),
        "qa": [
            ("Q1: 為什麼 Observability 對 agent 特別重要？",
             "**Agent 失敗不是「回答錯」是「不知道為什麼錯」**。\n\n"
             "**沒有 observability 的 agent 系統是黑盒** — 跑 production 就是賭博。\n\n"
             "**4 個必要能力**：\n\n"
             "1. **完整的 trace**（不是 log 海洋）\n"
             "2. **失敗模式分類**（不只「錯了」要說「哪一類錯」）\n"
             "3. **Memory governance**（防矛盾、防毒）\n"
             "4. **可審計**（誰在什麼時候做了什麼）"),
            ("Q2: Memoria 跟 OpenLIT 怎麼選？",
             "**Memoria** — 解決 Memory 自我治理（Git for AI Memory）。需要 version control、branch、contradiction detection 時用。\n\n"
             "**OpenLIT** — 解決 Telemetry 標準化（OpenTelemetry-native）。需要完整 trace + LLM-as-Judge + cost tracking 時用。\n\n"
             "**可以兩個都用**：Memoria 管 memory 層，OpenLIT 管 telemetry 層。"),
            ("Q3: 我可以從最簡單的 observability 開始嗎？",
             "**可以**。先做 3 件事：\n\n"
             "1. **統一 action 格式**（所有 tool call 用同一個 JSON schema）\n"
             "2. **寫 span log**（每次 LLM call 一個 span）\n"
             "3. **加 failure class taxonomy**（失敗時標分類）\n\n"
             "**不要一開始就裝 OpenLIT / Memoria** — 先讓 log 結構化，再評估。"),
        ],
        "next_teaser": "**M8 Bench / Routing / MCP Security** — Production-grade 三大支柱",
        "next_link": "/docs/m8-benchmarks/",
    },
    "m8-benchmarks": {
        "why_title": "為什麼學這個？",
        "why_body": (
            "**你在 production agent 系統？** 這章**必讀**。\n\n"
            "**3 個核心問題**：誰好？誰便宜？誰安全？這章用 3 個 sub-topic 全回答。"
        ),
        "qa": [
            ("Q1: 為什麼 SWE-bench 79.2% 不算解決 agent 問題？",
             "**SABER 論文證明**：benchmark ceiling 是 artifact，不是 model ceiling。\n\n"
             "**三個深層問題**：\n\n"
             "1. **Benchmark ceiling 是 artifact**（用 Verified 修正後分數會掉）\n"
             "2. **Cost-vs-score 曲線無人繪**（leaderboard 只列分數不看成本）\n"
             "3. **「嘗試次數」遊戲**（single-attack vs multi-attack 是 apples-to-oranges）"),
            ("Q2: 沒有 verifier 就不要做 cascade 對嗎？",
             "**對，這是 2026 routing 最重要的警告**。\n\n"
             "**為什麼**：cheap model「自信錯了」是最危險的 — 它把 hallucination 包裝成 high confidence，**比直接用 frontier 更難 debug**。\n\n"
             "**自做 cascade 必要條件**：self-verifier（cheap model 也回 confidence）。"),
            ("Q3: MCP 從 tool bus 變 policy-enforced tool fabric 是什麼意思？",
             "**範式轉移**：\n\n"
             "- 以前：「我能接什麼」=「tool list」\n"
             "- 現在：「我**應該**讓 LLM 看到什麼」=「policy gate」\n\n"
             "**3 層防禦**：\n\n"
             "1. **L1 Tool-list filter** — 危險 tool 不給 LLM 看\n"
             "2. **L2 Call-time policy** — 高風險 tool 需使用者確認\n"
             "3. **L3 Output sanitizer** — 防 indirect prompt injection"),
        ],
        "next_teaser": "🎉 **你看完 8 個 M 了！** 接下來：",
        "next_link": "/learning-path/",  # M8 結尾循環回 learning-path
    },
}

NEXT_LINK_OVERRIDE = {
    "m8-benchmarks": ("回到學習路徑，看下一步方向", "/learning-path/"),
}

def make_callout(title, body):
    return f'\n{{< callout type="info" title="{title}" >}}\n{body}\n{{< /callout >}}\n'

def make_qa_section(qa_pairs):
    out = ['\n## Q&A — 給實作者的常見問題\n']
    for title, body in qa_pairs:
        out.append(f'{{< details title="{title}" >}}\n{body}\n{{< /details >}}\n')
    return "\n".join(out)

def make_checklist(m_key):
    return f"""---

## 給實作者的 checklist

> 評估你的 **{m_key.upper()}** 系統是否 production-grade：

- [ ] 有對應的設計元素實作
- [ ] 失敗模式有被識別
- [ ] 可量化的評估指標
- [ ] 跨來源的設計 pattern 驗證
- [ ] 邊界情況有處理

---

"""

def inject(m_key, cfg):
    path = ROOT / m_key / "_index.md"
    if not path.exists():
        print(f"[SKIP] {m_key}: not found")
        return False

    content = path.read_text()

    # 1. 注入開頭 callout（找第一個 # 標題前面）
    why_callout = make_callout(cfg["why_title"], cfg["why_body"])
    # 找第一個 "# " (level 1 heading) 之前插入
    first_h1 = re.search(r'^# ', content, re.MULTILINE)
    if first_h1:
        content = content[:first_h1.start()] + why_callout + "\n" + content[first_h1.start():]
    else:
        print(f"[WARN] {m_key}: no H1 found, skipping why_callout")

    # 2. 注入 Q&A + checklist + next step（找「## 引用與延伸閱讀」之前插入）
    next_title, next_link = NEXT_LINK_OVERRIDE.get(m_key, (cfg["next_teaser"], cfg["next_link"]))
    next_section = f"""## 下一步學什麼

{next_title}

→ [繼續 →]({next_link})

"""
    qa = make_qa_section(cfg["qa"])
    checklist = make_checklist(m_key)
    insertion = qa + "\n" + checklist + next_section

    cite_marker = "## 引用與延伸閱讀"
    if cite_marker in content:
        content = content.replace(cite_marker, insertion + cite_marker)
    else:
        print(f"[WARN] {m_key}: no 引用與延伸閱讀 marker, appending at end")
        content += "\n" + insertion

    path.write_text(content)
    print(f"[OK] {m_key}: injected ({len(content)} chars)")
    return True

def main():
    print(f"Injecting Hextra interactive elements into {len(M_CONFIG)} M topics...")
    for m_key, cfg in M_CONFIG.items():
        inject(m_key, cfg)
    print("Done.")

if __name__ == "__main__":
    main()
