# AGENTS.md — Marimo 研报站架构 (CHINGBOH.github.io)

## 研报单一真源

1. **对外研报与主页的唯一应用真源是 `reports-marimo/*.py`。**
   - `portfolio_master_app.py` 生成首页；其余 `*_app.py` 各生成一份独立研报。
   - 叙事、布局、控件、图表和链接均在对应 Marimo app 中维护。不要把正文拆回 YAML，也不要手改导出的 HTML。

2. **数值真源是 DuckDB / Direct-Lake 视图与受控底稿。**
   - app 应只读连接湖仓、查询视图并在运行/导出时计算展示指标。
   - YAML 不再是研报的中间层、渲染输入或发布依赖；`data/monographs_src/`、`data/monographs_tpl/` 及旧 `monographs/*.html` 只保留为迁移前档案，禁止作为新内容来源。

3. **导出与发布分两步。**
   - 本地生成：`python3 scripts/build_and_export_marimo_all.py`。它从 Marimo app 输出静态 HTML 到仓库根目录 `index.html` 和 `monographs/marimo_*.html`。
   - 发布装配：`python3 scripts/assemble_marimo_site.py --output site`。它只发布上述 Marimo 导出物、必要的底稿索引，并为旧 YAML URL 生成跳转页；绝不把旧 YAML HTML 拷贝进发布目录。
   - 发布前校验：`python3 scripts/assemble_marimo_site.py --check`。

4. **禁止重新启用旧 YAML 管线。**
   - 不运行 `build_monographs_from_yaml.py`、`build_monographs_slots.py`、`build_monographs_yaml.py`、`build_monographs_md.py` 或 `playwright_verify_monographs.py` 来构建站点。
   - 若要清理迁移前档案，先单独确认删除范围；不要在功能修改中顺手删除历史资料。

## 静态站约定

- `index.html` 与 `monographs/marimo_*.html` 是 **Marimo 导出物**，由导出脚本覆盖；只可作为发布输入和视觉验收对象。
- `site/` 是一次性发布产物，已忽略，不提交。
- 部署走 GitHub Pages **legacy 分支直接部署**（`source: main` 根目录），推送 `main` 即自动上线，不依赖 Actions workflow（仓库内不保留自定义部署 workflow）。
- 历史中文文件名 URL 为兼容旧书签保留跳转页，目标均为对应的 Marimo 页面，不再提供旧页面内容。
