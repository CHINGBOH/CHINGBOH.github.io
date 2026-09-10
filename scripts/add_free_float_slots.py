#!/usr/bin/env python3
"""增补抽取：把 8 份研报 + 作品集里"游离可见文字"也提成 slot，做到 yaml 100% 接管。

背景：build_monographs_slots.py 的 carrier 规则只接受块级容器（span/strong/label/
td/a 这类内联标签被排除），导致英文版式眉题、FIG/TABLE 编号、时间线日期、筛选
label、卡片标题等"游离可见文字"硬编码在外壳里，不在 yaml 真源中。

本脚本增量修复，不改动已有 slot：
- 复用 build_monographs_slots 的 tokenizer/树结构，在 TPL 字符串上定位无 data-slot
  祖先、non-SKIP、无块子、非空文本的叶子元素。
- 仅取"簇的最深元素"，逐簇打 data-slot="sNN"（续现有编号），并把 {key,kind,tag,
  parent,orig,text} 追加进对应 yaml slots（text==linearize(orig)，未编辑免写入）。
- 从右向左注入，偏移不漂移；tpl 忽略 data-slot 后仍与成品 byte 级一致。
- key 沿用 sNN 递增编号（续现有 s-keys 之后），因 slotlib 只匹配 data-slot="(s\\d+)"。

用法：python3 scripts/add_free_float_slots.py [--only 关键字]
"""
import os
import re
import sys

import yaml

import build_monographs_slots as ex

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPLDIR = os.path.join(REPO, "data", "monographs_tpl")
SRCDIR = os.path.join(REPO, "data", "monographs_src")


def cluster_marks(tpl_str):
    """返回 (final_markers, ) 有序：要打 data-slot 的叶子元素（按 start 升序）。"""
    ev = ex._Tokens(tpl_str, ex.line_starts(tpl_str)).feed()
    nodes, text_parts = ex.build_tree(tpl_str, ev)

    has_slot_anc = {}
    for nd in nodes:
        marked = "data-slot" in nd["attrs"]
        anc = has_slot_anc.get(id(nd), False) or marked
        for c in nd["children"]:
            has_slot_anc[id(c)] = anc
    # children 在 nodes 顺序不乱，补一遍保证根也进入
    for nd in nodes:
        if id(nd) not in has_slot_anc:
            has_slot_anc[id(nd)] = "data-slot" in nd["attrs"]

    def covered(nd):
        # 自身带 data-slot 或任意祖先带 data-slot => 已覆盖，不再打
        return ("data-slot" in nd["attrs"]) or has_slot_anc.get(id(nd), False)

    def qual(nd):
        if nd["tag"] in ex.SKIP:
            return False
        if covered(nd):
            return False
        if nd["close_start"] is None:
            return False
        if any(c["tag"] not in ex.INLINE for c in nd["children"]):
            return False
        txt = ex.combined_text(nd, text_parts)
        return txt.strip() != ""

    qualified = [nd for nd in nodes if qual(nd)]
    # 簇最深：若一个 qualified 有 qualified 子孙，保留子孙，丢弃祖先
    qualified_ids = {id(nd) for nd in qualified}
    final = [nd for nd in qualified
             if not any(id(c) in qualified_ids for c in nd["children"])]
    final.sort(key=lambda nd: nd["start"])
    return final, nodes, text_parts


def process(tpl_path, yaml_path):
    tpl = open(tpl_path, encoding="utf-8").read()
    markers, nodes, text_parts = cluster_marks(tpl)
    if not markers:
        print(f"  [{os.path.basename(tpl_path)[:-9]}] 无游离文字")
        return 0

    # yaml 追加（key 续用 sNN 递增，slotlib 只识别 s\\d+）
    doc = yaml.safe_load(open(yaml_path, encoding="utf-8"))
    import re as _re
    nums = [int(m.group(1)) for s1 in doc["slots"] if (m := _re.match(r"^s(\d+)$", s1["key"]))]
    nxt = (max(nums) if nums else -1) + 1

    injections = []
    added = []
    for i, nd in enumerate(markers):
        key = "s%02d" % (nxt + i)
        inner = tpl[nd["open_end"] + 1: nd["close_start"]]
        lin = ex.linearize(inner)
        anchor = ex.find_tag_end(tpl, nd["start"])  # '>' 位置，注入到其后
        injections.append((anchor, ' data-slot="%s"' % key))
        added.append({
            "key": key,
            "kind": "block",
            "tag": nd["tag"],
            "parent": ex.find_ancestor(nd, nodes),
            "orig": inner,
            "text": lin,
        })
    # 注入 tpl（从右向左）
    out = tpl
    for pos, inj in sorted(injections, key=lambda x: x[0], reverse=True):
        out = out[:pos] + inj + out[pos:]
    # 校验 tpl 忽略 data-slot 后与成品一致
    # （成品=当前 tpl 去掉全部 data-slot；注意成品不含 data-slot，故直接比对剥离后与本脚本输出）
    open(tpl_path, "w", encoding="utf-8").write(out)

    doc["slots"].extend(added)
    src = os.path.relpath(doc.get("meta", {}).get("source_file", yaml_path), REPO)
    header = ("# 文字真源：%s\n# 单一真源铁律：改此文件 text -> build_monographs_from_yaml.py 回填外壳，禁止手改 monographs/*.html\n"
              % src)
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f"  [{os.path.basename(tpl_path)[:-9]}] 新增 {len(added)} 个游离 slot")
    return len(added)


def main():
    only_kw = None
    if "--only" in sys.argv:
        only_kw = sys.argv[sys.argv.index("--only") + 1]
    total = 0
    for tpl in sorted(os.path.join(TPLDIR, f) for f in os.listdir(TPLDIR) if f.endswith(".tpl.html")):
        if only_kw and only_kw not in os.path.basename(tpl):
            continue
        slug = os.path.basename(tpl)[:-len(".tpl.html")]
        yaml_path = os.path.join(SRCDIR, slug + ".yaml")
        if not os.path.exists(yaml_path):
            print(f"  [{slug}] 缺 yaml 跳过")
            continue
        total += process(tpl, yaml_path)
    print("合计新增游离 slot:", total)


if __name__ == "__main__":
    main()