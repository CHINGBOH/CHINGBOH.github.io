#!/usr/bin/env python3
"""
Playwright 验证脚本：
1. 检查返回导航条
2. 测试图表在不同宽度下的响应式缩放
3. 检测溢出情况
"""
import subprocess, sys

# 确保安装 playwright
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.sync_api import sync_playwright

import time, json, os

BASE_URL = "http://localhost:8899"
OUT_DIR  = "/home/l/projects/CHINGBOH.github.io/reports-marimo"

TEST_PAGES = [
    ("index", "/"),
    ("cloud_deco", "/monographs/marimo_cloud_deco.html"),
    ("ai_engineering", "/monographs/marimo_ai_engineering.html"),
    ("board_gm", "/monographs/marimo_board_and_gm.html"),
    ("hust", "/monographs/marimo_hust_statistics.html"),
]

WIDTHS = [1300, 1050, 800]

OVERFLOW_CHECK_JS = """
() => {
    const results = [];
    // 检查页面级别的溢出
    const bodyWidth = document.body.scrollWidth;
    const viewportWidth = window.innerWidth;
    const pageOverflow = bodyWidth > viewportWidth + 5;
    
    // 检查所有 SVG
    const svgs = Array.from(document.querySelectorAll("svg[viewBox]"));
    const svgIssues = svgs.map(s => {
        const r = s.getBoundingClientRect();
        const pr = s.parentElement ? s.parentElement.getBoundingClientRect() : null;
        const rightEdge = r.right;
        const overflow = rightEdge > viewportWidth + 5;
        return {
            width: Math.round(r.width),
            right: Math.round(rightEdge),
            parentWidth: pr ? Math.round(pr.width) : null,
            overflow: overflow,
        };
    });
    const hasOverflow = pageOverflow || svgIssues.some(s => s.overflow);
    
    return {
        viewportWidth: viewportWidth,
        bodyScrollWidth: bodyWidth,
        pageOverflow: pageOverflow,
        svgCount: svgs.length,
        svgIssues: svgIssues.filter(s => s.overflow),
        hasAnyOverflow: hasOverflow,
    };
}
"""

NAV_CHECK_JS = """
() => {
    const nav = document.getElementById("back-nav-bar");
    if (!nav) return { hasNav: false };
    const link = nav.querySelector("a[href='/']");
    const rect = nav.getBoundingClientRect();
    return {
        hasNav: true,
        linkText: link ? link.textContent.trim() : null,
        isFixed: getComputedStyle(nav).position === "fixed",
        top: rect.top,
        visible: rect.height > 0,
    };
}
"""

def main():
    report = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for page_name, path in TEST_PAGES:
            url = BASE_URL + path
            report[page_name] = {}
            
            for width in WIDTHS:
                page = browser.new_page(viewport={"width": width, "height": 900})
                try:
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    time.sleep(2)  # 等渲染完成
                    
                    # 检查导航条
                    nav_info = page.evaluate(NAV_CHECK_JS)
                    
                    # 检查溢出
                    overflow_info = page.evaluate(OVERFLOW_CHECK_JS)
                    
                    result = {
                        "nav": nav_info,
                        "overflow": overflow_info,
                    }
                    report[page_name][width] = result
                    
                    # 截图
                    shot_path = os.path.join(OUT_DIR, f"pw_{page_name}_{width}.png")
                    page.screenshot(path=shot_path, full_page=False)
                    
                    status = "✅ OK" if not overflow_info["hasAnyOverflow"] else "❌ OVERFLOW"
                    nav_status = "🔙 NAV" if nav_info.get("hasNav") else "   ---"
                    print(f"  {status} {nav_status} [{width}px] {page_name}: svgs={overflow_info['svgCount']}, body_scroll={overflow_info['bodyScrollWidth']}px, overflows={len(overflow_info['svgIssues'])}")
                    if overflow_info["svgIssues"]:
                        for issue in overflow_info["svgIssues"][:3]:
                            print(f"         ↳ SVG width={issue['width']}px, right={issue['right']}px > viewport {width}px")
                    
                except Exception as e:
                    print(f"  ⚠️  Error on {page_name} {width}px: {e}")
                    report[page_name][width] = {"error": str(e)}
                finally:
                    page.close()
        
        browser.close()
    
    print("\n" + "="*60)
    print("Playwright 测试完成！截图已保存到 reports-marimo/pw_*.png")
    return report

if __name__ == "__main__":
    print("=" * 60)
    print("Playwright 响应式图表验证 + 导航条测试")
    print("=" * 60)
    main()
