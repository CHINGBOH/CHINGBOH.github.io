#!/usr/bin/env python3
"""把 data/monographs/*.yaml 文字层转换为干净可读的研报专案 Markdown。

YAML schema（由 build_monographs_yaml.py 抽取）：
  meta: {source_file, slug, title}
  blocks:
    - {type: h,  level: int, text: str}      # 标题
    - {type: p,  text: str}                   # 段落
    - {type: table_row, cells: [str, ...]}    # 表格行（cells[0] 若非空视为表头）

输出：data/monographs_md/<slug>.md，图表/排版保留在源 HTML（YAML 仅文字层）。
用法：python3 scripts/build_monographs_md.py [--rebuild]
"""
import glob
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML_DIR = os.path.join(REPO, "data", "monographs")
OUT_DIR = os.path.join(REPO, "data", "monographs_md")


def main():
    import yaml

    os.makedirs(OUT_DIR, exist_ok=True)
    files = sorted(glob.glob(os.path.join(YAML_DIR, "*.yaml")))
    if not files:
        print("[WARN] data/monographs/ 下无 YAML，先跑 build_monographs_yaml.py")
        return

    produced = []
    for path in files:
        doc = yaml.safe_load(open(path, encoding="utf-8"))
        slug = doc["meta"]["slug"]
        title = doc["meta"]["title"]
        blocks = doc.get("blocks", [])

        L = [f"# {title}", ""]

        def tidy(t):
            # 剥离 SOURCES 证据段里混入的 SQL 命令块(ATTACH/.read/SELECT)
            t = re.split(r"\s*(?:📊)?\s*数据查询参考\s+ATTACH\b", t)[0]
            t = re.split(r"\s*ATTACH\s+'data/", t)[0]
            # 剥离正文里残留的章节编号引用(§ 3 / §4)
            t = re.sub(r"\s*§\s*\d+\s*", " ", t)
            # 剥离 bullet 符号
            t = t.replace("• ", "").replace("•", "")
            # 清理 emoji 装饰符
            t = re.sub(r"[📊🏛️🔑✨📌🎯💡⚡✅❗️]+", "", t)
            return re.sub(r"\s{2,}", " ", t).strip()

        # 表格分组：连续 table_row 聚成一个 markdown 表格，第一行视为表头
        i = 0
        while i < len(blocks):
            b = blocks[i]
            t = b["type"]
            if t == "h":
                L.append(f"{'#' * (b['level'] + 1)} {tidy(b['text'])}")
                L.append("")
            elif t == "p":
                pt = tidy(b["text"])
                if pt:
                    L.append(pt)
                    L.append("")
            elif t == "table_row":
                # 收集连续 rows
                rows = []
                while i < len(blocks) and blocks[i]["type"] == "table_row":
                    rows.append([tidy(c) for c in blocks[i]["cells"]])
                    i += 1
                # 表头 = 首行；全空跳过
                rows = [r for r in rows if any(c.strip() for c in r)]
                if rows:
                    header = rows[0]
                    body = rows[1:]
                    n = max(len(r) for r in rows)
                    L.append("| " + " | ".join(header) + " |")
                    L.append("| " + " | ".join(["---"] * n) + " |")
                    for r in body:
                        r = r + [""] * (n - len(r))
                        L.append("| " + " | ".join(r) + " |")
                    L.append("")
                else:
                    i -= 1  # 已消费的空行，回退避免死循环
            i += 1

        out = os.path.join(OUT_DIR, slug + ".md")
        with open(out, "w", encoding="utf-8") as f:
            f.write("\n".join(L).rstrip() + "\n")
        produced.append(slug)
        print(f"[OK] {slug}.md")

    print(f"\n完成: {len(produced)} 份")


if __name__ == "__main__":
    main()