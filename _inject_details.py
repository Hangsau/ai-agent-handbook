#!/usr/bin/env python3
"""
v2：正確版 — 一次找所有匹配位置，從後往前 wrap（避免 offset 移位）。
"""
import re
from pathlib import Path

ROOT = Path("/root/projects/ai-agent-handbook/content/docs")

# 規則：H2 標題符合這些 pattern 的章節整段包成 details
RULES = [
    (r"^##\s+(\d+\.\s+)?引用與延伸閱讀\s*$", "📚 引用與延伸閱讀（點開看完整 reference）"),
    (r"^##\s+(\d+\.\s+)?給.*[的]?啟示[（(]?", "💡 給實作者的啟示（點開看 actionable 建議）"),
    (r"^##\s+(\d+\.\s+)?對\s+Hermes.*啟示[（(]?", "💡 給實作者的啟示（點開看 actionable 建議）"),
    (r"^##\s+(\d+\.\s+)?(可複製性評估|.*限制.*|.*各方案的限制.*)\s*$", "⚠️ 限制與評估（點開看誠實檢討）"),
]

H2_PATTERN = re.compile(r"^##\s+(?!#)(?!\d+\.\d+)(.+?)$", re.MULTILINE)

def find_h2_positions(content):
    return [(m.start(), m.end(), m.group(1).strip()) for m in H2_PATTERN.finditer(content)]

def process_file(path):
    content = path.read_text()

    # 一次找所有 H2 位置
    h2s = find_h2_positions(content)
    if not h2s:
        return 0

    # 找出所有匹配 RULE 的 H2
    to_wrap = []  # (start, end, title)
    for i, (s, e, title_text) in enumerate(h2s):
        h2_line = content[s:e]
        for rule_pat, title_template in RULES:
            if re.match(rule_pat, h2_line.strip()):
                if i + 1 < len(h2s):
                    end = h2s[i + 1][0]
                else:
                    end = len(content)
                to_wrap.append((s, end, title_template))
                break

    if not to_wrap:
        return 0

    # 從後往前 wrap（避免 offset 變化）
    to_wrap.sort(reverse=True)
    for s, e, title in to_wrap:
        section = content[s:e]
        # 移除 H2 開頭
        body = re.sub(r"^##[^\n]*\n", "", section, count=1).lstrip("\n")
        # H2 標題保留（顯示章節標題），body 包成 details
        h2_line = section.split("\n", 1)[0]
        # 用 string concatenation（不用 f-string）避免 {{ 跟 { escape 衝突
        replacement = (
            h2_line + "\n\n"
            + '{{< details title="' + title + '" >}}\n'
            + body + "\n"
            + '{{< /details >}}\n'
        )
        content = content[:s] + replacement + content[e:]

    path.write_text(content)
    return len(to_wrap)

def main():
    print("Wrapping supplementary sections into <details> (v2 correct)...")
    total = 0
    for m_dir in sorted(ROOT.iterdir()):
        if not m_dir.is_dir():
            continue
        p = m_dir / "_index.md"
        if not p.exists():
            continue
        n = process_file(p)
        if n > 0:
            print(f"  {m_dir.name}: wrapped {n} sections")
            total += n
        else:
            print(f"  {m_dir.name}: no matches")
    print(f"\nTotal: {total} sections wrapped")

if __name__ == "__main__":
    main()
