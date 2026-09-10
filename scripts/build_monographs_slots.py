#!/usr/bin/env python3
"""研报/作品集文字真源无损抽取器（AGENTS.md 单一真源铁律）

从成品 `monographs/*.html` 与 `作品集.html` 一次性无损抽出：
  1. `data/monographs_tpl/<slug>.tpl.html`  —— 外壳模板：成品原样，仅给"用户可编辑文字节点"打 data-slot 属性
  2. `data/monographs_src/<slug>.yaml`       —— 文字真源（slot 模型，kind/orig/text/parent）

设计原则（方案 C：成品即外壳 + data-slot 原位回填）
- 骨架/图表 JS/样式/布局结构一律不动；只给叶子文字容器注入 `data-slot="sNN"`。
- 因此 tpl 忽略 `data-slot` 后与成品 **byte 级一致**，Step1b 强制校验。
- yaml `slots` 按 DOM 顺序扁平排列；`orig`=容器当前内部原文(精确子串)；
  `text`=可编辑的轻量 markdown 化正文（渲染器：text==linearize(orig) 时保持 orig，否则回填 render(text)）。

用法：
    python3 scripts/build_monographs_slots.py [--only 关键字] [--rebuild]
"""
import html
import html.parser
import os
import re
import sys

import yaml  # PyYAML：与 build_monographs_yaml.py 一致（失败则 pip install pyyaml）

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_FILES = sorted([
    os.path.join(REPO, "monographs", f)
    for f in os.listdir(os.path.join(REPO, "monographs"))
    if f.endswith(".html")
]) + [os.path.join(REPO, "作品集.html")]

TPLDIR = os.path.join(REPO, "data", "monographs_tpl")
YAMLDIR = os.path.join(REPO, "data", "monographs_src")

# 行内元素：不作为 slot 载体；其余视为"结构化容器"
INLINE = {
    "b", "strong", "i", "em", "span", "a", "u", "sup", "sub",
    "code", "br", "small", "mark", "abbr", "wbr", "cite", "q",
    "label", "time",
}
# 跳过：内容不作为文字真源
SKIP = {
    "script", "style", "svg", "canvas", "noscript", "head", "meta",
    "link", "title", "iframe", "video", "audio", "object", "embed",
    "math", "base", "template", "slot",
}


def line_starts(s):
    offs = [0]
    for i, ch in enumerate(s):
        if ch == "\n":
            offs.append(i + 1)
    return offs


def find_tag_end(raw, start):
    """从 '<' 起扫描到该开始标签的 '>' 的索引（引号感知）。"""
    j = start
    q = False
    quote = None
    n = len(raw)
    while j < n:
        c = raw[j]
        if q:
            if c == quote:
                q = False
        else:
            if c in ('"', "'"):
                q = True
                quote = c
            elif c == ">":
                return j
        j += 1
    return -1


class _Tokens:
    """收集带字节偏移的事件序列。"""

    def __init__(self, raw, ls):
        self.raw = raw
        self.ls = ls
        self.ev = []
        self.skip = 0  # 处于 script/style 内的深度

    def off(self):
        ln, col = self.p.getpos()
        return self.ls[ln - 1] + col if ln - 1 < len(self.ls) else -1

    def feed(self):
        class P(html.parser.HTMLParser):
            def __init__(self, owner):
                super().__init__(convert_charrefs=False)
                self.o = owner

            def handle_starttag(self, tag, attrs):
                if self.o.skip:
                    self.o.skip += 1
                    return
                if tag in ("script", "style"):
                    self.o.skip = 1
                self.o.ev.append([self.o.off(), "start", tag, attrs])

            def handle_startendtag(self, tag, attrs):
                if self.o.skip:
                    return
                self.o.ev.append([self.o.off(), "startend", tag, attrs])

            def handle_endtag(self, tag):
                if self.o.skip:
                    self.o.skip -= 1
                self.o.ev.append([self.o.off(), "end", tag, None])

            def handle_data(self, data):
                if self.o.skip:
                    return
                if data:
                    self.o.ev.append([self.o.off(), "data", None, data])

            def handle_entityref(self, name):
                self.o.ev.append([self.o.off(), "ref", None, "&" + name + ";"])

            def handle_charref(self, name):
                self.o.ev.append([self.o.off(), "ref", None, "&#" + name + ";"])

        self.p = P(self)
        self.p.feed(self.raw)
        self.ev.sort(key=lambda e: e[0])
        return self.ev


def build_tree(raw, ev):
    """由事件建立元素栈，计算每个元素 start/open_end/close_start 及各元素内嵌文本。

    返回 (elements, data_buckets)：elements 按 start 字节升序；data_buckets[node_id].
    """
    # 计算每个 start 事件的 open_end（'>' 位置）
    open_end_for_start = {}
    for e in ev:
        if e[1] in ("start", "startend"):
            j = find_tag_end(raw, e[0])
            open_end_for_start[id(e)] = j

    nodes = []          # node dicts
    node_by_start = {}  # start_byte -> node
    stack = []
    text_parts = {}     # id(node) -> list[str]
    live = {}           # id(node) currently open -> node

    for e in ev:
        typ = e[1]
        if typ in ("start", "startend"):
            nd = {
                "tag": e[2],
                "attrs": dict(e[3] or []),
                "start": e[0],
                "open_end": open_end_for_start[id(e)],
                "close_start": None,
                "children": [],
            }
            if stack:
                nid = id(stack[-1])
                stack[-1]["children"].append(nd)
            nodes.append(nd)
            node_by_start[e[0]] = nd
            live[id(nd)] = nd
            text_parts[id(nd)] = []
            if typ == "start":
                stack.append(nd)
        elif typ == "end":
            nd = live.pop(id(stack[-1]), None) if stack else None
            if nd is not None and nd["tag"] == e[2]:
                nd["close_start"] = e[0]
                stack.pop()
            else:
                # 容错：向上找到同名进行匹配
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i]["tag"] == e[2]:
                        stack[i]["close_start"] = e[0]
                        live.pop(id(stack[i]), None)
                        stack = stack[:i]
                        break
        elif typ in ("data", "ref"):
            if stack:
                nid = id(stack[-1])
                text_parts[nid].append(e[3])

    # 仅保留有 close 的 start 且提供 inner 文本身份
    return nodes, text_parts


def combined_text(nd, text_parts):
    """合并节点自身内联文本 + 子节点文本。"""
    out = list(text_parts.get(id(nd), []))
    for c in nd["children"]:
        out.extend(text_parts.get(id(c), []))
    return "".join(out)


def has_block_child(nd):
    return any(c["tag"] not in INLINE for c in nd["children"])


def nearest_parent(node):
    p = node
    while p is not None:
        if p.get("attrs", {}).get("id"):
            return p["attrs"]["id"]
        if p["tag"] in ("section", "article", "main") and p.get("attrs", {}).get("class"):
            return p["attrs"]["class"].split()[0]
        p = None  # 父链不在 nodes 双向；改用 start 字节前缀匹配祖先
        break
    return None


def find_ancestor(node, nodes):
    """由 start 字节找最近带 id/class 的祖先(section/article/div...)。"""
    best = None
    for other in nodes:
        if other is node:
            continue
        if other["start"] < node["start"] and other["close_start"] is not None:
            if other["close_start"] > node["start"]:
                if other["tag"] in ("section", "article", "main", "header", "footer", "div", "nav", "figure"):
                    if other.get("attrs", {}).get("id"):
                        best = other["attrs"]["id"]
                        break
                    elif other.get("attrs", {}).get("class"):
                        best = other["attrs"]["class"].split()[0]
                        break
    return best or "body"


def linearize(inner_html):
    """把叶子容器内部 html 压成轻量 markdown：**粗体** / `等宽` / \\n 换行，其余去标签、解实体。"""
    t = inner_html
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"</?(?:strong|b)>", "**", t, flags=re.I)
    t = re.sub(r"</?code>", "`", t, flags=re.I)
    t = re.sub(r"</?(?:a|span|i|em|u|sup|sub|small|mark|abbr|cite|q|label|time)[^>]*>", "", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    return t


def render_md(text):
    """渲染器用：markdown -> html（** → <strong>、` → <code>、\\n → <br>，其余转义）。"""
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = t.replace("\n", "<br>")
    return t


def kind_for(nd, nodes):
    tag = nd["tag"]
    anc = find_ancestor(nd, nodes)
    if tag == "h1":
        return "hero-title" if anc in ("hero",) else "section-title"
    if tag in ("h2", "h3", "h4", "h5", "h6"):
        return "sec-heading"
    if tag == "p":
        return "p"
    if tag in ("li",):
        return "li"
    if tag in ("td", "th"):
        return "table-cell"
    if tag == "a":
        return "link"
    if tag in ("div",):
        if "spec-value" in (nd.get("attrs", {}).get("class", "") or ""):
            return "kpi"
        if "chart-" in (nd.get("attrs", {}).get("class", "") or ""):
            return "chart-caption"
        return "block"
    return "block"


def process(path, out_tpl, out_yaml, only_kw=None):
    from hashlib import sha256

    raw = open(path, encoding="utf-8").read()
    digest = sha256(raw.encode("utf-8")).hexdigest()

    ev = _Tokens(raw, line_starts(raw)).feed()
    nodes, text_parts = build_tree(raw, ev)

    # 候选 carrier：非内联、非跳过、无块子元素、有文字、有 close_start
    carriers = []
    for nd in nodes:
        if nd["tag"] in INLINE or nd["tag"] in SKIP:
            continue
        if nd["close_start"] is None:
            continue
        if has_block_child(nd):
            continue
        txt = combined_text(nd, text_parts)
        if txt.strip() == "":
            continue
        carriers.append((nd, txt))

    carriers.sort(key=lambda x: x[0]["start"])

    # 分配 key（按 DOM 顺序 s00, s01, ...）
    slots = []
    injections = []  # (open_end_index_of_>, " data-slot=\"sNN\"")
    for idx, (nd, txt) in enumerate(carriers):
        key = "s%02d" % idx
        inner_orig = raw[nd["open_end"] + 1: nd["close_start"]]
        lin = linearize(inner_orig)
        slots.append({
            "key": key,
            "kind": kind_for(nd, nodes),
            "tag": nd["tag"],
            "parent": find_ancestor(nd, nodes),
            "orig": inner_orig,
            "text": lin,
        })
        injections.append((nd["open_end"], ' data-slot="%s"' % key))

    injections.sort(key=lambda x: x[0])
    # 从后往前插入，避免偏移错位
    tpl = raw
    for pos, inject in sorted(injections, key=lambda x: x[0], reverse=True):
        tpl = tpl[:pos] + inject + tpl[pos:]

    slug = os.path.splitext(os.path.basename(path))[0]
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S)
    if m:
        title = linearize(m.group(1))

    doc = {
        "meta": {
            "source_file": os.path.relpath(path, REPO),
            "slug": slug,
            "title": title,
            "hash": digest,
        },
        "slots": slots,
    }

    os.makedirs(out_tpl, exist_ok=True)
    with open(os.path.join(out_tpl, slug + ".tpl.html"), "w", encoding="utf-8") as f:
        f.write(tpl)
    with open(os.path.join(out_yaml, slug + ".yaml"), "w", encoding="utf-8") as f:
        f.write("# 文字真源：%s\n# 单一真源铁律：改此文件 text -> build_monographs_from_yaml.py 回填外壳，禁止手改 monographs/*.html\n"
                % os.path.relpath(path, REPO))
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=1000)

    return {
        "slug": slug,
        "carriers": len(carriers),
        "tpl_eq": tpl.replace(' data-slot="', "").replace('" data-slot', "") or True,
        "hash": digest,
    }


def verify_tpl_byte_eq(orig_path, tpl_path):
    """tpl 去除注入的 data-slot 属性后应与成品字节一致。"""
    raw = open(orig_path, encoding="utf-8").read()
    tpl = open(tpl_path, encoding="utf-8").read()
    stripped = re.sub(r"[ \t]data-slot=\"s\d+\"", "", tpl)
    return raw == stripped


def main():
    argv = sys.argv[1:]
    only_kw = None
    if "--only" in argv:
        only_kw = argv[argv.index("--only") + 1]

    os.makedirs(TPLDIR, exist_ok=True)
    os.makedirs(YAMLDIR, exist_ok=True)

    summary = []
    for path in SRC_FILES:
        if only_kw and only_kw not in os.path.basename(path):
            continue
        r = process(path, TPLDIR, YAMLDIR)
        tpl_path = os.path.join(TPLDIR, r["slug"] + ".tpl.html")
        eq = verify_tpl_byte_eq(path, tpl_path)
        r["byte_eq"] = eq
        summary.append(r)
        print("[%s] carriers=%d byte_eq=%s slug=%s"
              % ("OK" if eq else "BYTE_DIFF", r["carriers"], eq, r["slug"]))

    bad = [r for r in summary if not r["byte_eq"]]
    if bad:
        print("\n[FAIL] %d 份 tpl 与成品字节不一致！" % len(bad))
        for r in bad:
            print("   -", r["slug"])
        sys.exit(1)
    print("\n[OK] 全部 %d 份抽取完成，tpl 忽略 data-slot 后与成品 byte 级一致。"
          % len(summary))


if __name__ == "__main__":
    main()