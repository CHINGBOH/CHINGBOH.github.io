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
  /* 移动端响应式网格断点：防止 repeat(4, ...) 强行在手机端压成 4 列造成排版文字竖排 */
  @media (max-width: 768px) {
    [style*="grid-template-columns: repeat(4"],
    [style*="grid-template-columns:repeat(4"],
    [style*="grid-template-columns: 1fr 1fr 1fr 1fr"] {
      grid-template-columns: 1fr !important;
      gap: 10px !important;
    }
  }
  @media (min-width: 769px) and (max-width: 1024px) {
    [style*="grid-template-columns: repeat(4"],
    [style*="grid-template-columns:repeat(4"] {
      grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
      gap: 12px !important;
    }
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
            
        content = clean_html_svgs(content)
        
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"    ✓ {'[MONOGRAPH+NAV]' if is_monograph else '[INDEX]'} {dest_path} ({len(content):,} bytes)")

    print("\nAll Marimo reports exported and patched with responsive engine!")

if __name__ == "__main__":
    main()
