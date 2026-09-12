# CHINGBOH.github.io

以 **Marimo + DuckDB Direct-Lake** 构建的静态作品集与交互式商业研报站，部署于 GitHub Pages。

## 架构

```text
DuckDB / 受控底稿 ──> reports-marimo/*.py ──> index.html + monographs/marimo_*.html ──> push main ──> GitHub Pages (legacy 分支直接部署)
```

- `reports-marimo/`：**唯一应用真源**（Marimo app）。文字、布局、控件、图表和链接都在相应的 app 中维护，不拆回 YAML，也不手改导出的 HTML。
- DuckDB Direct-Lake 视图：指标与事实的数据来源；app 只读连接湖仓、查询视图，在运行/导出时计算展示值。
- `index.html`、`monographs/marimo_*.html`：Marimo 导出的静态页面，是发布输入与视觉验收对象，不手工编辑。
- `data/monographs_src/`、`data/monographs_tpl/` 与旧中文文件名研报：迁移前档案，不参与构建或发布。

## 部署链路（legacy 分支直接部署）

Pages 配置为 `source: main`（根目录），**推送 main 即自动上线，不依赖 Actions workflow**。

改动流程：

1. 编辑 `reports-marimo/*.py`。
2. 导出静态页到仓库根：

   ```bash
   python3 scripts/build_and_export_marimo_all.py
   ```

   Marimo 不在默认 venv 时，追加 `--marimo-bin /path/to/marimo`。只导某几页可用 `--only <关键词>`。

3. 提交并推送：

   ```bash
   git add . && git commit -m "..." && git push origin main
   ```

4. GitHub Pages legacy 自动从 main 根目录部署上线（数十秒），无需等待 Actions。

## 发布装配与校验（可选）

`scripts/assemble_marimo_site.py` 生成一次性 `site/` 目录（含旧 URL 跳转页）并做发布前校验；`site/` 已 gitignore，legacy 部署不依赖它：

```bash
python3 scripts/assemble_marimo_site.py --output site
python3 scripts/assemble_marimo_site.py --check
python3 -m http.server 8000 --directory site   # 本地预览
```

## 页面

| 页面 | Marimo 源码 | 发布路径 |
| --- | --- | --- |
| 作品集总舱 | `portfolio_master_app.py` | `/` (index.html) |
| 广田云软装 | `cloud_deco_app.py` | `/monographs/marimo_cloud_deco.html` |
| 董办与总经办 | `board_and_gm_app.py` | `/monographs/marimo_board_and_gm.html` |
| 华科统计学 | `hust_statistics_app.py` | `/monographs/marimo_hust_statistics.html` |
| AI 工程 | `ai_engineering_app.py` | `/monographs/marimo_ai_engineering.html` |
| 红花岗 | `honghuagang_app.py` | `/monographs/marimo_honghuagang.html` |
| 湄潭 | `meitan_app.py` | `/monographs/marimo_meitan.html` |
| 华泰 | `huatai_app.py` | `/monographs/marimo_huatai.html` |
| 九龙山庄 | `jiulong_app.py` | `/monographs/marimo_jiulong.html` |

## 迁移说明

旧 YAML 研报不再是内容或发布的中间层；旧中文 URL 保留跳转页指向对应 Marimo 页面，以维持已有书签，跳转页不含旧研报正文。