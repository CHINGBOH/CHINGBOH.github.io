#!/usr/bin/env python3
"""slot 共享工具库（build_monographs_from_yaml.py / verify_monographs_diff.py 共用）

提供：
- linearize(inner)：叶子容器内部 html -> 轻量 markdown（** / ` / \\n）
- render_md(text)：markdown -> html（与 linearize 互逆的转义规则）
- slot_regions(html)：扫描 data-slot 属性 -> {key:(tag, inner_start, close_start, inner)}
- skeleton_html(html)：把每个 slot 内部替换为 __SLOT__（用于"骨架不动"结构门禁）
- tag_norm(html)：归一化标签序列（忽略文字/属性，仅 tag 名 + 开闭）
"""
import html
import re

INLINE = {
    "b", "strong", "i", "em", "span", "a", "u", "sup", "sub",
    "code", "br", "small", "mark", "abbr", "wbr", "cite", "q", "label", "time",
}


def linearize(inner_html):
    t = inner_html
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"</?(?:strong|b)>", "**", t, flags=re.I)
    t = re.sub(r"</?code>", "`", t, flags=re.I)
    t = re.sub(r"</?(?:a|span|i|em|u|sup|sub|small|mark|abbr|cite|q|label|time)[^>]*>", "", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    return t


def render_md(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = t.replace("\n", "<br>")
    return t


def find_tag_end(raw, start):
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


def slot_regions(html_str):
    """返回 {key: (tag, inner_start, close_start, inner)}"""
    out = {}
    pat = re.compile(r'data-slot="(s\d+)"')
    for m in pat.finditer(html_str):
        key = m.group(1)
        tagstart = html_str.rfind("<", 0, m.start())
        tm = re.match(r"<([A-Za-z][\w-]*)", html_str[tagstart:])
        if not tm:
            continue
        tag = tm.group(1)
        open_end = find_tag_end(html_str, tagstart)
        if open_end < 0:
            continue
        inner_start = open_end + 1
        open_pat = re.compile(r"<" + re.escape(tag) + r"(\s|>)")
        close_pat = re.compile(r"</" + re.escape(tag) + r">")
        depth = 1
        i = open_end
        close_start = None
        while True:
            om = open_pat.search(html_str, i)
            cm = close_pat.search(html_str, i)
            if cm is not None and (om is None or cm.start() < om.start()):
                depth -= 1
                if depth == 0:
                    close_start = cm.start()
                    break
                i = cm.end()
            elif om is not None:
                depth += 1
                i = om.end()
            else:
                break
        if close_start is None:
            continue
        out[key] = (tag, inner_start, close_start, html_str[inner_start:close_start])
    return out


def strip_slots(html_str):
    """剥离 data-slot 构建标记属性（产物 html 不应携带）。"""
    return re.sub(r"[ \t]data-slot=\"s\d+\"", "", html_str)


def skeleton_html(html_str):
    """把每个 slot 内部替换为 __SLOT__，得到"骨架"（忽略 slot 内变化）。"""
    regions = slot_regions(html_str)
    ops = sorted(((v[1], v[2], k) for k, v in regions.items()), key=lambda x: -x[1])
    out = html_str
    for inner_start, close_start, key in ops:
        out = out[:inner_start] + "__SLOT__" + out[close_start:]
    return out


def tag_norm(html_str, script_ok=True):
    """归一化标签序列：[(name, open|close|selfclose), ...]，忽略文字/属性/script 内容整体。"""
    import html.parser

    res = []
    skip = 0
    p = None

    class P(html.parser.HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)

        def handle_starttag(self, tag, attrs):
            nonlocal skip
            if skip:
                return
            if tag in ("script", "style", "svg", "canvas"):
                skip = 1
            res.append((tag, "open"))

        def handle_startendtag(self, tag, attrs):
            if skip:
                return
            res.append((tag, "selfclose"))

        def handle_endtag(self, tag):
            nonlocal skip
            if skip:
                skip = 0
                return
            res.append((tag, "close"))

    p = P()
    p.feed(html_str)
    return res