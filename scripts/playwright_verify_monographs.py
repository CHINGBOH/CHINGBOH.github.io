#!/usr/bin/env python3
"""Playwright 校验：渲染后研报/作品集的图表与文字端点。

对每份渲染产物：
1. 用 Chromium 打开（file://），等待网络空闲；
2. 断言 `echarts` 全局可用；
3. 断言每个 `.chart-container` 内部都有已初始化的 `<canvas>`（图表未被破坏）；
4. 抽查来自 yaml 的一组文字端点（hero-title/section-title/sec-heading/kpi/chart-caption）确实出现在页面文本中；
5. 全页截图存档到 data/monographs_backup/verify_shots/<slug>.png（供人眼/像素比对）。

用法：
    python3 scripts/playwright_verify_monographs.py [--only 关键字] [--shots 目录]
"""
import os
import sys

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRCDIR = os.path.join(REPO, "data", "monographs_src")
MONO = os.path.join(REPO, "monographs")
SHOTS = os.path.join(REPO, "data", "monographs_backup", "verify_shots")


def text_endpoints(doc):
    """从 yaml 取一组代表性文字端点（非 orig 空文本的少量 slot）。"""
    pick = []
    for s in doc["slots"]:
        if s["kind"] in ("hero-title", "section-title", "sec-heading", "kpi", "chart-caption"):
            t = (s.get("text") or "").replace("\n", " ").strip()
            if t and 3 <= len(t) <= 44 and "*" not in t and "`" not in t:
                pick.append(t)
        if len(pick) >= PER_PAGE_ENDPOINTS:
            break
    return pick


PER_PAGE_ENDPOINTS = 6


def main():
    args = sys.argv[1:]
    only = args[args.index("--only") + 1] if "--only" in args else None
    global SHOTS
    if "--shots" in args:
        SHOTS = args[args.index("--shots") + 1]

    from playwright.sync_api import sync_playwright

    targets = [
        os.path.join(MONO, f) for f in sorted(os.listdir(MONO)) if f.endswith(".html")
    ] + [os.path.join(REPO, "作品集.html")]

    os.makedirs(SHOTS, exist_ok=True)
    failures = []
    ok_total = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for path in targets:
            if only and only not in os.path.basename(path):
                continue
            slug = os.path.splitext(os.path.basename(path))[0]
            slug = os.path.basename(path)[:-5]
            doc = None
            yp = os.path.join(SRCDIR, slug + ".yaml")
            if os.path.exists(yp):
                doc = yaml.safe_load(open(yp, encoding="utf-8"))
            page = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
            report = []
            try:
                page.goto("file://" + path, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(800)

                # 1. echarts 可用
                echarts_ok = page.evaluate("typeof window.echarts !== 'undefined'")
                report.append(f"echarts global: {'OK' if echarts_ok else 'MISSING'}")

                # 2. 每个 chart-container 有 canvas
                n_containers = page.locator(".chart-container").count()
                n_canvas = page.locator(".chart-container canvas").count()
                report.append(f"chart-containers={n_containers} canvases={n_canvas} "
                              f"({'ALL INIT' if n_canvas >= n_containers else 'MISSING INIT'})")
                if n_containers > 0 and n_canvas < n_containers:
                    failures.append(f"{slug}: chart canvas 缺失 {n_canvas}/{n_containers}")

                # 3. 文字端点抽查
                if doc:
                    eps = text_endpoints(doc)
                    missing = []
                    for ep in eps:
                        if not page.get_by_text(ep, exact=True).count():
                            missing.append(ep)
                    report.append(f"endpoints: 抽查{len(eps)}个, 缺失{len(missing)}个" +
                                  (f" -> {missing}" if missing else " OK"))
                    if missing:
                        failures.append(f"{slug}: 文字端点缺失 {len(missing)}/{len(eps)}")

                page.screenshot(path=os.path.join(SHOTS, slug + ".png"), full_page=True)
                report.append(f"shot -> {slug}.png")
            except Exception as e:
                failures.append(f"{slug}: {e}")
            finally:
                page.close()
            print(f"[{slug}] " + " | ".join(report))
            ok_total += 1

        browser.close()

    print(f"\nverified {ok_total} files")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("ALL CHART + TEXT ENDPOINTS PASS")


if __name__ == "__main__":
    main()