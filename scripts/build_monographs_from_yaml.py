#!/usr/bin/env python3
"""研报/作品集渲染器：YAML 文字真源 -> 回填外壳模板 -> monographs/*.html

方案 C（成品即外壳 + data-slot 原位回填）：
- 外壳模板 `data/monographs_tpl/<slug>.tpl.html` 由 build_monographs_slots.py 无损生成；
  其每个文字容器已打 `data-slot="sNN"`，内部为抽取时的原始文字（orig）。
- 渲染器对每个 slot：
    - 若 `text == linearize(orig)`（未编辑）→ 保持 orig，不写；
    - 否则 → 用 `render_md(text)` 原位替换该 slot 内部。
- 其余部分（head/style/nav/图表容器与内联 script/交错顺序/footer）一律不动。
- 由此"图文交错"问题从根上消失（骨架不动只换字），图表保真度最高。

门禁：
- 默认严格：`yaml.meta.hash` 与当前 `monographs/<slug>.html` 指纹不符 → 拒绝
  （保护手工打磨过的成品不被意外覆盖；`--force` 跳过）。
- `--orig-check`：每个 slot 的 `orig` 必须仍等于 tpl 当前内部文字（防 tpl 漂移）。
- `--diff`：渲染到内存，与当前成品做结构 diff + 文字 diff，任何不符 → 不覆盖并退出 1。

用法：
    python3 scripts/build_monographs_from_yaml.py --backup --diff --force
    python3 scripts/build_monographs_from_yaml.py --only 遵义大酒店 --dry-run
"""
import datetime
import json
import hashlib
import os
import re
import shutil
import sys

import yaml

import slotlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRCDIR = os.path.join(REPO, "data", "monographs_src")
TPLDIR = os.path.join(REPO, "data", "monographs_tpl")
BKUP = os.path.join(REPO, "data", "monographs_backup")
REPORT = os.path.join(REPO, "data", "monographs_diff_report.txt")

# <slug> -> 输出文件绝对路径
OUTPUTS = {}
_mono = os.path.join(REPO, "monographs")
for f in os.listdir(_mono):
    if f.endswith(".html"):
        OUTPUTS[f[:-5]] = os.path.join(_mono, f)
_outputs_tpl = {os.path.splitext(f)[0]: f for f in os.listdir(TPLDIR) if f.endswith(".tpl.html")}


def find_output(tpl_slug):
    """由 tpl slug 找输出 html 路径：tpl slug 与 monographs 文件同名。"""
    if tpl_slug in OUTPUTS:
        return OUTPUTS[tpl_slug]
    # 作品集特殊情况：tpl slug 可能是"作品集"，输出 作品集.html
    p = os.path.join(REPO, tpl_slug + ".html")
    return p if os.path.exists(p) else None


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def render_slots(slug, doc, tpl_str, orig_check=True, force=False, errors=None):
    """按 doc 的 slots 对 tpl_str 做原位回填。errors 收集问题。返回渲染后字符串。"""
    errors = errors if errors is not None else []
    regions = slotlib.slot_regions(tpl_str)
    out = tpl_str
    keys = [s["key"] for s in doc["slots"]]
    if len(set(keys)) != len(keys):
        errors.append(f"[{slug}] slot key 重复")
    pending = set(keys)
    edits = []
    for s in doc["slots"]:
        key = s["key"]
        pending.discard(key)
        if key not in regions:
            errors.append(f"[{slug}] data-slot {key} 不在外壳中")
            continue
        tag, inner_start, close_start, current_inner = regions[key]
        orig = s.get("orig")
        lin = slotlib.linearize(orig) if orig is not None else ""
        if orig_check:
            if current_inner != orig:
                errors.append(
                    f"[{slug}] slot {key} 外壳内部文字 vs yaml.orig 不符（外壳疑似被手改/漂移）")
        text = s.get("text")
        if text == lin or (text is None and current_inner == orig):
            continue  # 未编辑：保留 orig
        edits.append((inner_start, close_start, slotlib.render_md(text)))
    # 按偏移降序应用替换：先改尾部，保证前部偏移在字符串中仍有效
    for inner_start, close_start, new_inner in sorted(edits, key=lambda e: e[0], reverse=True):
        out = out[:inner_start] + new_inner + out[close_start:]

    if pending:
        for key in sorted(pending):
            errors.append(f"[{slug}] yaml slot {key} 未在外壳中找到 data-slot")
    return out


def diff_report(slug, tpl_str, baseline_html, rendered_html, doc):
    """结构与文字 diff。返回 (ok, lines)。

    结构门禁：外壳模板只改动 slot 内部，故"外壳骨架"与"渲染骨架"必须标签一致；
    任何 slot 之外的骨架漂移即 FAIL。基线文件仅作文字一致性软校验。
    """
    lines = []
    ok = True
    sk_t = slotlib.tag_norm(slotlib.skeleton_html(tpl_str))
    sk_r = slotlib.tag_norm(slotlib.skeleton_html(rendered_html))
    if sk_t == sk_r:
        lines.append(f"structure: PASS（外骨架与外壳一致）")
    else:
        ok = False
        lines.append(f"structure: FAIL（外骨架漂移）")
        for i, (a, b) in enumerate(zip(sk_t, sk_r)):
            if a != b:
                lines.append(f"        首个骨架差异 @#{i}: 外壳={a} 渲染={b}")
                break
    # 文字门禁：渲染结果每个 slot 应等于 yaml 期望（orig 或 render_md(text)）
    regions = slotlib.slot_regions(rendered_html)
    unexpected = 0
    for s in doc["slots"]:
        key = s["key"]
        if key not in regions:
            unexpected += 1
            lines.append(f"        slot {key} 缺失 data-slot")
            continue
        cur = regions[key][3]
        text = s.get("text")
        lin = slotlib.linearize(s.get("orig") or "")
        # 未编辑( text==linearize(orig) ) => 渲染保留 orig；已编辑 => render_md(text)
        expected = (s.get("orig") or "") if (text == lin) else slotlib.render_md(text)
        if cur != expected:
            unexpected += 1
            lines.append(f"        slot {key} 渲染文字与 yaml 期望不符")
    if unexpected == 0:
        lines.append(f"text: PASS（{len(doc['slots'])} slots 与 yaml 一致）")
    else:
        ok = False
        lines.append(f"text: FAIL（{unexpected} 个 slot 不符）")
    # 软校验：与基线文件做标签序列对比（首次未编辑渲染应一致；编辑后仅 slot 内差异属预期）
    if baseline_html is not None:
        sb = slotlib.tag_norm(baseline_html)
        sr = slotlib.tag_norm(rendered_html)
        if sb == sr:
            lines.append(f"baseline: 与基线标签序列 byte 级一致")
        else:
            lines.append(f"baseline: 与基线存在差异（编辑过 slot 则属预期）")
    return ok, lines


def main():
    argv = sys.argv[1:]
    do_backup = "--backup" in argv
    do_diff = "--diff" in argv
    force = "--force" in argv
    dry = "--dry-run" in argv
    soonly = None
    if "--only" in argv:
        soonly = argv[argv.index("--only") + 1]

    tpl_files = sorted(os.path.join(TPLDIR, f) for f in os.listdir(TPLDIR) if f.endswith(".tpl.html"))
    if soonly:
        tpl_files = [f for f in tpl_files if soonly in os.path.basename(f)]

    if not tpl_files:
        print("[WARN] 无外壳模板，先跑 build_monographs_slots.py")
        return

    all_ok = True
    full_report = []

    # 备份
    if do_backup and not dry:
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        bdir = os.path.join(BKUP, ts)
        os.makedirs(bdir, exist_ok=True)
        manifest = []
        for tpl_file in tpl_files:
            slug = os.path.splitext(os.path.basename(tpl_file))[0].replace(".tpl", "")
            dest = find_output(slug)
            if dest and os.path.exists(dest):
                shutil.copy2(dest, os.path.join(bdir, os.path.basename(dest)))
                manifest.append(f"{sha256_bytes(open(dest,'rb').read())}  {os.path.basename(dest)}")
        with open(os.path.join(bdir, "MANIFEST.txt"), "w", encoding="utf-8") as f:
            f.write("UTC backup %s\n" % ts + "\n".join(sorted(manifest)) + "\n")
        full_report.append(f"[backup] -> {bdir}")

    for tpl_file in tpl_files:
        slug = os.path.basename(tpl_file)[:-len(".tpl.html")]
        yaml_path = os.path.join(SRCDIR, slug + ".yaml")
        dest = find_output(slug)
        if not os.path.exists(yaml_path):
            full_report.append(f"[{slug}] 缺 yaml，跳过")
            continue
        doc = yaml.safe_load(open(yaml_path, encoding="utf-8"))
        if not doc:
            continue
        tpl_str = open(tpl_file, encoding="utf-8").read()

        file_ok = True
        errors = []
        ref_hash = doc.get("meta", {}).get("hash")
        if not force and dest and os.path.exists(dest) and ref_hash:
            cur_hash = sha256_bytes(open(dest, "rb").read())
            if cur_hash != ref_hash:
                errors.append(
                    f"[{slug}] 当前成品指纹与 yaml.meta.hash 不符（成品被手改？）。"
                    "用 --force 以当前成品为基线强制渲染，或先重新 build_monographs_slots.py 抽取。")

        rendered = render_slots(slug, doc, tpl_str, orig_check=not force,
                                force=force, errors=errors)

        # 结构/文字 diff（与当前成品比对，逐份独立）
        if dest and os.path.exists(dest):
            baseline = open(dest, encoding="utf-8").read()
            ok, lines = diff_report(slug, tpl_str, baseline, rendered, doc)
            if not ok:
                file_ok = False
            full_report.append(f"[{slug}] diff: {'PASS' if ok else 'FAIL'}")
            full_report.extend("    " + l for l in lines)
            # 无损强校验：剥离 data-slot 后的产物应与基线 byte 级一致（有编辑则为预期差异）
            ship = slotlib.strip_slots(rendered)
            if ship == baseline:
                full_report.append("    byte_eq: 产物与基线 byte 级一致")
            else:
                full_report.append("    byte_eq: 与基线有差异（编辑过 slot 则属预期）")

        if errors:
            file_ok = False
            for e in errors:
                full_report.append("  ERR " + e)

        if dry:
            full_report.append(f"[{slug}] (dry-run) 未写入")
            if not file_ok:
                all_ok = False
            continue

        if not file_ok:
            all_ok = False
            full_report.append(f"[{slug}] 未写入（存在失败门禁）")
            continue

        if dest is None:
            full_report.append(f"[{slug}] 找不到输出路径，未写")
            all_ok = False
            continue
        ship = slotlib.strip_slots(rendered)  # 剥离 data-slot 构建标记
        with open(dest, "w", encoding="utf-8") as f:
            f.write(ship)
        full_report.append(f"[{slug}] -> 已写入 {os.path.relpath(dest, REPO)}")

    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(full_report) + "\n")

    for l in full_report:
        print(l)
    print("\nRESULT:", "ALL PASS" if all_ok else "HAS FAILURE")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()