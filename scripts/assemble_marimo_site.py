#!/usr/bin/env python3
"""Assemble the GitHub Pages artifact from reviewed Marimo exports.

This deliberately does not invoke Marimo or access the private Direct-Lake.
The exports are reviewed locally first; CI only copies those static artifacts.
"""

from __future__ import annotations

import argparse
import html
import shutil
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
HOME_EXPORT = Path("index.html")
REPORT_EXPORTS = {
    "marimo_cloud_deco.html": Path("monographs/marimo_cloud_deco.html"),
    "marimo_board_and_gm.html": Path("monographs/marimo_board_and_gm.html"),
    "marimo_hust_statistics.html": Path("monographs/marimo_hust_statistics.html"),
    "marimo_ai_engineering.html": Path("monographs/marimo_ai_engineering.html"),
    "marimo_honghuagang.html": Path("monographs/marimo_honghuagang.html"),
    "marimo_meitan.html": Path("monographs/marimo_meitan.html"),
    "marimo_huatai.html": Path("monographs/marimo_huatai.html"),
    "marimo_jiulong.html": Path("monographs/marimo_jiulong.html"),
}

# Old YAML routes stay alive as redirect-only compatibility URLs.  No legacy
# report HTML is copied to the deployed site.
LEGACY_REDIRECTS = {
    "AI全栈工程与VibeCoding敏捷研发商业研报.html": "marimo_ai_engineering.html",
    "上市公司董办合规资本运作与总经办企业运营商业研报.html": "marimo_board_and_gm.html",
    "上海华泰中心售楼处全生命周期商业操盘研报.html": "marimo_huatai.html",
    "华中科技大学统计学学术奠基与数理底座商业研报.html": "marimo_hust_statistics.html",
    "深圳市广田云软装科技全生命周期商业操盘与供应链大盘商业研报.html": "marimo_cloud_deco.html",
    "湄潭项目全生命周期数据洞察研报.html": "marimo_meitan.html",
    "红花岗项目全生命周期深度商业研报.html": "marimo_honghuagang.html",
    "遵义大酒店五星级软装工程全周期商业操盘研报.html": "marimo_cloud_deco.html",
}
ROOT_REDIRECTS = {"作品集.html": "index.html"}
OPTIONAL_ROOT_FILES = (Path("专案数据与底稿穿透索引.html"),)


def redirect_page(destination: str) -> str:
    escaped = html.escape(destination, quote=True)
    return f"""<!doctype html>
<html lang=\"zh-CN\"><head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <meta http-equiv=\"refresh\" content=\"0; url={escaped}\">
  <link rel=\"canonical\" href=\"{escaped}\">
  <title>页面已迁移</title>
</head><body>
  <p>该研报已迁移至 <a href=\"{escaped}\">Marimo 交互式页面</a>。</p>
  <script>location.replace({destination!r});</script>
</body></html>
"""


def resolve_output(value: str) -> Path:
    output = Path(value).resolve()
    if output == REPO or REPO not in output.parents:
        raise ValueError("--output 必须是仓库内的子目录，不能是仓库根目录")
    return output


def required_sources() -> list[Path]:
    return [REPO / HOME_EXPORT, *(REPO / path for path in REPORT_EXPORTS.values())]


def assert_sources() -> None:
    missing = [path.relative_to(REPO) for path in required_sources() if not path.is_file()]
    if missing:
        formatted = ", ".join(map(str, missing))
        raise FileNotFoundError(f"缺少 Marimo 导出物：{formatted}。请先运行 build_and_export_marimo_all.py")


def assemble(output: Path) -> None:
    assert_sources()
    if output.exists():
        shutil.rmtree(output)
    (output / "monographs").mkdir(parents=True)

    shutil.copy2(REPO / HOME_EXPORT, output / "index.html")
    for published_name, source_relative in REPORT_EXPORTS.items():
        shutil.copy2(REPO / source_relative, output / "monographs" / published_name)

    for old_name, target in LEGACY_REDIRECTS.items():
        (output / "monographs" / old_name).write_text(redirect_page(target), encoding="utf-8")
    for old_name, target in ROOT_REDIRECTS.items():
        (output / old_name).write_text(redirect_page(target), encoding="utf-8")
    for source_relative in OPTIONAL_ROOT_FILES:
        source = REPO / source_relative
        if source.is_file():
            shutil.copy2(source, output / source_relative.name)

    (output / ".nojekyll").touch()
    (output / "404.html").write_text(redirect_page("index.html"), encoding="utf-8")


def check(output: Path) -> None:
    required = [output / "index.html", *(output / "monographs" / name for name in REPORT_EXPORTS)]
    required += [output / "monographs" / name for name in LEGACY_REDIRECTS]
    required += [output / name for name in ROOT_REDIRECTS]
    missing = [path.relative_to(output) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("发布目录缺少文件：" + ", ".join(map(str, missing)))

    marimo_pages = [output / "index.html", *(output / "monographs" / name for name in REPORT_EXPORTS)]
    non_marimo = [
        path.relative_to(output)
        for path in marimo_pages
        if "@marimo-team" not in path.read_text(encoding="utf-8", errors="replace")
    ]
    if non_marimo:
        raise AssertionError("发布输入不是 Marimo 导出物：" + ", ".join(map(str, non_marimo)))

    leaked = []
    for old_name in LEGACY_REDIRECTS:
        contents = (output / "monographs" / old_name).read_text(encoding="utf-8")
        if "location.replace" not in contents or "Marimo" not in contents:
            leaked.append(old_name)
    if leaked:
        raise AssertionError("旧 URL 不是 Marimo 跳转页：" + ", ".join(leaked))
    print(f"[ok] Marimo site ready: {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="site", help="发布目录（默认：site）")
    parser.add_argument("--check", action="store_true", help="只验证现有发布目录，不写文件")
    args = parser.parse_args()

    try:
        output = resolve_output(args.output)
        if args.check:
            check(output)
        else:
            assemble(output)
            check(output)
    except (AssertionError, FileNotFoundError, ValueError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
