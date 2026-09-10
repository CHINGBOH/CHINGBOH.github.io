#!/usr/bin/env python3
"""
研报文字层抽取器（AGENTS.md 单一真源铁律）
==========================================
将 monographs/*.html 的「文字层」抽取为 data/monographs/*.yaml：
章节标题 + 段落 + 表格 + 列表文本，按原文 DOM 顺序组织为扁平 blocks。
图表 script/style/nav 一律剔除 —— 不参与渲染，仅作可读/可编辑字源。

设计原则：
- 扁平 blocks 顺序模型，忠实原文，零嵌套歧义，便于 Agents/脚本读取。
- 不修改、不依赖原 HTML 文件；YAML 仅供内容查阅与编辑。
- yaml_file 字段记录源文件，支持 --rebuild 反复重建。

用法：
    python3 scripts/build_monographs_yaml.py            # 抽全部 monographs/*.html
    python3 scripts/build_monographs_yaml.py --rebuild  # 强制重新抽取全部（覆盖已有）
"""
import html
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO_ROOT, "monographs")
OUT_DIR = os.path.join(REPO_ROOT, "data", "monographs")


def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def extract_blocks(html_text):
    """把 body 中带文本的标题/段落/列表抽为扁平 blocks。

    正文大量承载在 div 的裸文本（非 p/li 标签），故采用 DOM 顺序遍历：
    - h1-h3 记作 "h" 标题块；
    - 其余非空文本节点聚合为 "p" 段落块（剔除导航/品牌/指标碎片）。
    """
    from html.parser import HTMLParser

    body = html_text
    m = re.search(r"<body[^>]*>(.*)</body>", html_text, re.S)
    if m:
        body = m.group(1)

    class _P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.blocks = []  # 输出
            self.cur = []  # 当前裸文本缓存
            self.skip = 0  # 跳过的嵌套深度（script 等）
            self.hlevel = None
            self.in_tr = False  # 是否在表格行内
            self.in_cell = False
            self.row_cells = []
            self.cell = []

        def _flush_cell(self):
            if self.in_cell:
                t = "".join(self.cell)
                t = re.sub(r"\s+", " ", t).strip()
                self.row_cells.append(t)
            self.cell = []
            self.in_cell = False

        def handle_starttag(self, tag, attrs):
            if self.skip:
                self.skip += 1
                return
            if tag in ("script", "style", "nav", "header", "footer"):
                self.skip = 1
                self.flush()
                return
            if tag in ("h1", "h2", "h3", "h4"):
                self.flush()
                self.hlevel = tag
            elif tag == "tr":
                self._flush_cell()
                self.in_tr = True
            elif tag in ("td", "th"):
                if self.in_tr:
                    self._flush_cell()
                    self.in_cell = True
            elif tag in ("li", "br"):
                self.flush()

        def handle_endtag(self, tag):
            if self.skip:
                self.skip -= 1
                return
            if tag == "tr":
                self._flush_cell()
                if self.in_tr and any(self.row_cells):
                    self.blocks.append({"type": "table_row", "cells": self.row_cells})
                self.in_tr = False
                self.in_cell = False
                self.row_cells = []
            elif tag in ("td", "th"):
                if self.in_tr:
                    self._flush_cell()
            elif tag in ("h1", "h2", "h3", "h4"):
                self.flush()
            elif tag in ("li", "p"):
                self.flush()

        def handle_data(self, data):
            if self.skip:
                return
            if data and data.strip():
                if self.in_cell:
                    self.cell.append(data)
                else:
                    self.cur.append(data)
            elif data:
                # 相邻 inline 元素(如两个<span>代码名)间的空白节点保留为分隔，
                # 避免 "probe_sas_dom.py" + "ui_button_registry.md" 粘连
                if self.in_cell:
                    self.cell.append(" ")
                else:
                    self.cur.append(" ")

        def flush(self):
            txt = "".join(self.cur)
            self.cur = []
            t = re.sub(r"\s+", " ", txt).strip()
            if not t:
                return
            hl = getattr(self, "hlevel", None)
            if hl:
                if len(t) > 1:
                    self.blocks.append({"type": "h", "text": t, "level": int(hl[1])})
                self.hlevel = None
            else:
                self.blocks.append({"type": "p", "text": t})

    p = _P()
    p.feed(body)
    blocks = p.blocks

    # 剔除导航/品牌噪声：开头的短英文标识、返回链接、ARCHIVAL 等
    noise = ("ARCHIVAL MONOGRAPH", "返回云软装大盘", "PROFESSIONAL PORTFOLIO")

    def _is_table_caption(t):
        """判定是否为 ECharts 图表 caption（英文标签+数据碎片拼接、无完整中文句）。"""
        # 证据段无条件保留
        if re.search(r"本研报所述|参考标准|归档状态|本专案所述", t):
            return False
        # 含 FIG. 数据标签 → caption
        if re.search(r"FIG\.", t):
            return True
        # 含连续英文大写标签(标签+紧随中文/数字)+数据碎片
        if re.search(r"[A-Z][A-Z ]{4,}(?:[\u4e00-\u9fff]|\d),|NET SPACE|CONTRACT SUM|SUBMITTED SUM",
                     t):
            return True
        # 以英文大写标签(>2词)起始/或含 · 分隔英文标签 → 多为图表分区标记
        if re.match(r"^[A-Z][A-Z& ]{3,}", t) or re.search(r"(?:^| )· [A-Z]{2,}(?: · |$)", t):
            return True
        return False

    def clean_p(bk):
        """返回处理后的文本；若整段应剔除返回 None。"""
        t = bk["text"]
        if t in noise:
            return None
        if _is_table_caption(t):
            return None
        # 剥离嵌在文字中间的 SECTION 分区标签
        t = re.sub(
            r"\s*SECTION\s*(?:\d+|[IVXLC]+)(?:\s*[·.\-]\s*[A-Z0-9A-Za-z ·]+)?\s*",
            " ", t).strip()
        # 剥离段落末尾的图表分区标记：如 "判断B · VALUE ALLOCATION"、"匹配C · ASSET COMPOSITION"
        t = re.sub(
            r"\s*[A-Z] · [A-Z][A-Z ]{2,}$", " ", t).strip()
        # 剥离 SQL 取证命令碎片(ATTACH/.read/SELECT 属 HTML 代码块残留)
        t = re.sub(
            r"(?:📊)?数据查询参考\s*ATTACH.*?(?=本|§|参考|$)", "", t, flags=re.S)
        t = re.sub(r"\s{2,}", " ", t).strip()
        return t or None

    keep = []
    for bk in blocks:
        if bk["type"] == "h":
            keep.append(bk)
            continue
        if bk["type"] != "p":
            keep.append(bk)
            continue
        cleaned = clean_p(bk)
        if cleaned is None:
            continue
        bk["text"] = cleaned
        keep.append(bk)

    # 剔除首个真标题之前的导航菜单垃圾(锚点标签/返回链接/PRJ代号)
    def _is_nav(t):
        if t.startswith("‹") or t.startswith("返回") or "返回总舱" in t or "返回云软装" in t:
            return True
        if re.match(r"^PRJ-[A-Z0-9-]+$", t):
            return True
        # 纯短中文锚点标签(≤6字、无标点)
        if len(t) <= 6 and re.fullmatch(r"[\u4e00-\u9fff]+", t):
            return True
        return False

    final = []
    for bk in keep:
        if bk["type"] == "h":
            break  # 真标题出现后不再过滤
        if bk["type"] == "p" and _is_nav(bk["text"]):
            continue
        final.append(bk)
    # 追加剩余块(首个标题起全部保留)
    idx = next((i for i, b in enumerate(keep) if b["type"] == "h"), len(keep))
    final.extend(keep[idx:])
    return final


def slug_of(title):
    s = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]+", "-", title)
    return s.strip("-")[:40] or "monograph"


def main():
    rebuild = "--rebuild" in sys.argv
    if not os.path.isdir(SRC_DIR):
        print(f"[ERR] 源目录不存在: {SRC_DIR}")
        sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)

    files = sorted(
        f for f in os.listdir(SRC_DIR) if f.endswith(".html")
    )
    if not files:
        print("[WARN] monographs/ 下无 HTML")
        return

    import yaml  # 用于解析校验（读取用）

    produced = []
    for fn in files:
        path = os.path.join(SRC_DIR, fn)
        src = open(path, encoding="utf-8").read()
        # 文档标题
        t = re.search(r"<title[^>]*>(.*?)</title>", src, re.S)
        raw_title = strip_tags(t.group(1)) if t else fn
        # 去掉站点尾缀
        title = re.sub(r"\s*\|\s*梁清波.*$", "", raw_title).strip()
        slug = slug_of(re.sub(r"\.html$", "", fn))
        blocks = extract_blocks(src)
        doc = {
            "meta": {
                "source_file": fn,
                "slug": slug,
                "title": title,
            },
            "blocks": blocks,
        }
        out_path = os.path.join(OUT_DIR, slug + ".yaml")
        if os.path.exists(out_path) and not rebuild:
            print(f"[SKIP] {out_path} 已存在（--rebuild 覆盖）")
            continue
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(doc, f, allow_unicode=True, sort_keys=False, default_flow_style=False,
                      width=999, indent=2)
        produced.append((slug, len(blocks)))
        print(f"[OK] {slug}.yaml  blocks={len(blocks)}")

    for slug, _n in produced:
        # 校验可解析
        with open(os.path.join(OUT_DIR, slug + ".yaml"), encoding="utf-8") as f:
            yaml.safe_load(f)
    print(f"\n完成: 生成 {len(produced)} 份, 校验均通过")


if __name__ == "__main__":
    main()