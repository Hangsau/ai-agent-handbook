#!/usr/bin/env python3
"""
v3 — 把每章的 H2 章節（包括核心章節 1-11）都包成 <details>，
預設收起來，讀者一打開只看到：
- 開頭 callout
- 章節地圖（視覺化導覽）
- 結語
- Q&A（已是 details）
- checklist
- 下一步 CTA
- 引用（已是 details）

每章的視覺長度大幅縮短，讀者按需展開。
"""
import re
from pathlib import Path

ROOT = Path("/root/projects/ai-agent-handbook/content/docs")

# 規則：H2 章節符合這些 pattern 的**不包**（保留展開可見）
KEEP_OPEN = [
    r"^##\s+Q&A\s+",  # Q&A 章節保留（裡面有 details）
    r"^##\s+給實作者的\s*checklist\s*$",  # checklist 保留
    r"^##\s+下一步學什麼\s*$",  # CTA 保留
    r"^##\s+引用與延伸閱讀\s*$",  # 引用已被 details 包了
    r"^##\s+結語.*",  # 結語保留
]

H2_PATTERN = re.compile(r"^##\s+(?!#)(?!\d+\.\d+)(.+?)$", re.MULTILINE)

def process_file(path):
    content = path.read_text()
    h2s = list(H2_PATTERN.finditer(content))
    if not h2s:
        return 0

    # 找出要 wrap 的章節
    to_wrap = []
    for i, m in enumerate(h2s):
        h2_text = m.group(0).strip()
        should_keep = any(re.match(p, h2_text) for p in KEEP_OPEN)
        if not should_keep:
            if i + 1 < len(h2s):
                end = h2s[i + 1].start()
            else:
                end = len(content)
            to_wrap.append((m.start(), end, h2_text))

    if not to_wrap:
        return 0

    # 從後往前 wrap
    to_wrap.sort(reverse=True)
    for s, e, h2_line in to_wrap:
        # 取得 section 內文
        section = content[s:e]
        # 移除 H2 開頭，body 取出
        body = re.sub(r"^##[^\n]*\n", "", section, count=1)
        # 移除 body 開頭多餘空行
        body = body.lstrip("\n")
        # H2 標題作為 summary（拿掉 # 跟編號空白，給更乾淨的 summary）
        h2_title = re.sub(r"^##\s*\d+\.\s*", "", h2_line).strip()
        # 替換：H2 標題 + 摺疊內容
        # 把 H2 變 H3 視覺（讓它在摺疊區之上，summary 樣式）
        replacement = (
            '<details class="handbook-chapter-details">\n'
            '<summary>' + h2_title + '</summary>\n\n'
            + body
            + '\n</details>\n'
        )
        content = content[:s] + replacement + content[e:]

    path.write_text(content)
    return len(to_wrap)

def main():
    print("Wrapping ALL H2 sections into <details> (except keep-open list)...")
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
            print(f"  {m_dir.name}: no changes")
    print(f"\nTotal: {total} sections wrapped (default collapsed)")

if __name__ == "__main__":
    main()
