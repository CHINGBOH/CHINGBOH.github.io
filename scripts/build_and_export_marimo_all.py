#!/usr/bin/env python3
"""
Marimo 导出全量静态 HTML 并注入 100% 图表响应式伸缩引擎与去水印保护
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MARIMO = os.environ.get(
    "MARIMO_BIN", "/home/l/.data-science-venv/bin/marimo"
)

TASKS = [
    # (src, dest, is_monograph)
    ("reports-marimo/portfolio_master_app.py", "index.html", False),
    ("reports-marimo/cloud_deco_app.py", "monographs/marimo_cloud_deco.html", True),
    ("reports-marimo/board_and_gm_app.py", "monographs/marimo_board_and_gm.html", True),
    ("reports-marimo/hust_statistics_app.py", "monographs/marimo_hust_statistics.html", True),
    ("reports-marimo/ai_engineering_app.py", "monographs/marimo_ai_engineering.html", True),
    ("reports-marimo/honghuagang_app.py", "monographs/marimo_honghuagang.html", True),
    ("reports-marimo/meitan_app.py", "monographs/marimo_meitan.html", True),
    ("reports-marimo/huatai_app.py", "monographs/marimo_huatai.html", True),
    ("reports-marimo/jiulong_app.py", "monographs/marimo_jiulong.html", True),
]

# 返回首页导航条 (仅注入到专项研报，不注入主页)
BACK_NAV_BAR = """
<div id="back-nav-bar" style="
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 99999;
  background: rgba(22, 42, 69, 0.96);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  font-family: 'JetBrains Mono', 'Fira Mono', monospace;
  font-size: 12px;
">
  <a href="/" style="
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #e2e8f0;
    text-decoration: none;
    font-weight: 600;
    letter-spacing: 0.03em;
    padding: 4px 12px;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 4px;
    transition: background 0.2s;
  " onmouseover="this.style.background='rgba(255,255,255,0.12)'" onmouseout="this.style.background='transparent'">
    ← 返回主页
  </a>
  <span style="color: rgba(255,255,255,0.5); font-size: 11px;">
    BOONE LIANG · ARCHIVAL MONOGRAPH
  </span>
</div>
<div style="height: 44px;"></div>
"""

RESPONSIVE_STYLE = """
<style id="marimo-responsive-charts-fix">
  /* 全局图表与图片 100% 自适应伸缩引擎 */
  *, *::before, *::after {
    box-sizing: border-box !important;
  }
  svg {
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
    margin: 0 auto !important;
  }
  img {
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
  }
  [style*="display:grid"], [style*="display: grid"], [style*="display:flex"], [style*="display: flex"] {
    box-sizing: border-box !important;
    max-width: 100% !important;
  }
  [style*="display:grid"] > div, [style*="display: grid"] > div, [style*="display:flex"] > div, [style*="display: flex"] > div {
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
  /* 侧边栏及主视图防横向溢出 */
  .marimo-app, main, article, section, [data-marimo-app="true"], #root {
    max-width: 100% !important;
    overflow-x: hidden !important;
    box-sizing: border-box !important;
  }
  /* 彻底屏蔽静态提示条和水印 */
  [data-radix-toast-viewport], ol[tabindex="-1"], li[role="status"],
  a[href*="marimo-team/marimo"], a[href*="marimo.io"],
  [aria-label*="Notification"], [class*="toast"] {
    display: none !important;
    opacity: 0 !important;
    pointer-events: none !important;
    visibility: hidden !important;
  }
</style>
"""

# 首页「生涯阶段直达」切换引擎：document 层 JS，穿透 shadow DOM 找到原生 stage 面板，
# 依据 location.hash 显示对应阶段并滚动顶部。纯 DOM 操作，与 React/Marimo 状态完全解耦。
STAGE_JS = """
<style data-stage-style="true">
  .career-nav { display: flex; flex-direction: column; gap: 3px; font-size: 12.5px; line-height: 1.5; }
  .career-nav a { display: block; padding: 7px 10px; border-left: 3px solid transparent; color: #334155; text-decoration: none; border-radius: 3px; background: transparent; transition: background .12s, border-color .12s; }
  .career-nav a[data-stage="overview"] { border-left-color: #8a6839; color: #162a45; font-weight: 600; }
  .career-nav a:hover { background: rgba(22,42,69,0.05); border-left-color: #8a6839; }
  .career-nav a.is-active { background: rgba(22,42,69,0.08); border-left-color: #8a6839; color: #162a45; font-weight: 700; }
</style>
<script data-stage-switch="true">
(function () {
  function roots() {
    var r = [document], i = 0;
    while (i < r.length) {
      var d = r[i];
      try { if (d.shadowRoot && r.indexOf(d.shadowRoot) < 0) r.push(d.shadowRoot); } catch (e) {}
      try {
        d.querySelectorAll('*').forEach(function (el) {
          if (el.shadowRoot && r.indexOf(el.shadowRoot) < 0) r.push(el.shadowRoot);
        });
      } catch (e) {}
      i++;
    }
    return r;
  }
  function qa(sel) {
    var o = [];
    roots().forEach(function (rt) {
      try { o = o.concat([].slice.call(rt.querySelectorAll(sel))); } catch (e) {}
    });
    return o;
  }
  function panels() { return qa('.stage-panel'); }
  function links() { return qa('a[data-stage]'); }
  function keyOf() {
    var keys = ['overview', 'hust', 'board', 'cloud', 'ai'];
    var raw = (location.hash || '').replace('#', '');
    // hash 存的是 #stage-ai，面板 data-stage 存 ai，需剥离 stage- 前缀以对齐
    var key = raw.indexOf('stage-') === 0 ? raw.slice(6) : raw;
    return keys.indexOf(key) >= 0 ? key : 'hust';
  }
  function apply() {
    var key = keyOf();
    panels().forEach(function (p) {
      var k = (p.getAttribute('data-stage') || '');
      p.style.display = (k && k === key && key !== 'overview') ? 'block' : 'none';
    });
    links().forEach(function (a) {
      if (a.getAttribute('data-stage') === key) { a.classList.add('is-active'); }
      else { a.classList.remove('is-active'); }
    });
    try { window.scrollTo(0, 0); } catch (e) {}
  }
  window.addEventListener('hashchange', apply);
  var tries = 0;
  function boot() {
    if (panels().length > 0) { apply(); }
    else if (tries++ < 80) { setTimeout(boot, 150); }
  }
  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', boot);
  } else {
    setTimeout(boot, 300);
  }
})();
</script>
"""

def clean_html_svgs(content):
    """
    清洗 HTML 内部的 SVG 标签，确保没有任何死锁的 pt/px 宽高阻碍响应式缩放
    """
    def repl_svg(m):
        tag = m.group(0)
        # 移除固定的 width="...pt" 或 width="...px"
        tag = re.sub(r'\s+width="[^"]*\"', '', tag)
        tag = re.sub(r'\s+height="[^"]*\"', '', tag)
        tag = re.sub(r'\s+style="[^"]*\"', '', tag)
        return tag.replace('<svg', '<svg style="width:100%; max-width:100%; height:auto; display:block; margin:0 auto;" preserveAspectRatio="xMidYMid meet"')
    
    # 仅针对 matplotlib 生成的带有 viewBox 的 svg 进行替换
    content = re.sub(r'<svg[^>]+viewBox=[^>]+>', repl_svg, content)
    return content

def main():
    parser = argparse.ArgumentParser(
        description="Export the Marimo source apps used by the public static site."
    )
    parser.add_argument(
        "--output-dir",
        default=str(BASE_DIR),
        help="Directory that receives index.html and monographs/ (default: repository root)",
    )
    parser.add_argument(
        "--marimo-bin",
        default=DEFAULT_MARIMO,
        help="marimo executable (or set MARIMO_BIN)",
    )
    parser.add_argument(
        "--only",
        help="Export only a matching app/output name (for example: huatai)",
    )
    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()
    os.chdir(BASE_DIR)
    for src_rel, dest_rel, is_monograph in TASKS:
        if args.only and args.only.lower() not in f"{src_rel} {dest_rel}".lower():
            continue
        src_path = BASE_DIR / src_rel
        dest_path = output_dir / dest_rel
        
        if not os.path.exists(src_path):
            print(f"Skipping {src_rel}, not found")
            continue
            
        print(f"--> Exporting {src_rel} -> {dest_rel}...")
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [args.marimo_bin, "export", "html", str(src_path), "-o", str(dest_path), "--no-include-code", "-f"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error exporting {src_rel}: {res.stderr}")
            sys.exit(1)
            
        # 读取导出的 HTML 并注入响应式样式与清洗
        with open(dest_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 注入 style 到 </head> 前
        if "</head>" in content:
            content = content.replace("</head>", f"{RESPONSIVE_STYLE}\n</head>")
        else:
            content = f"{RESPONSIVE_STYLE}\n{content}"
            
        # 专项研报：注入返回导航条到 <body> 后
        if is_monograph:
            if "<body>" in content:
                content = content.replace("<body>", f"<body>\n{BACK_NAV_BAR}", 1)
            else:
                # 如果没有 <body>，注入到 HTML 最开头
                content = f"{BACK_NAV_BAR}\n{content}"
        else:
            # 首页：注入「生涯阶段直达」切换引擎到 </body> 前
            if "</body>" in content:
                content = content.replace("</body>", f"{STAGE_JS}\n</body>")
            else:
                content = f"{STAGE_JS}\n{content}"
            
        content = clean_html_svgs(content)
        
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"    ✓ {'[MONOGRAPH+NAV]' if is_monograph else '[INDEX]'} {dest_path} ({len(content):,} bytes)")

    print("\nAll Marimo reports exported and patched with responsive engine!")

if __name__ == "__main__":
    main()
