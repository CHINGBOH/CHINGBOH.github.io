# AGENTS.md — 研报文字 YAML 单一真源铁律 (CHINGBOH.github.io)

<!-- monographs_yaml_single_source_rule -->
## 🏛️ 研报/作品集文字单一真源 Iron Rule

1. **研报正文与作品集文字唯一真源 = `data/monographs_src/<slug>.yaml`**（slot 扁平模型）
   - 每个 `slot`：`text` 为可编辑轻量 markdown（`**粗体**` / `` `等宽` `` / `\n` 换行），`orig` 为抽取时的容器原始内部文字，`kind` 白名单：hero-title/section-title/sec-heading/p/li/table-cell/kpi/chart-caption/block/…
   - 首页文字走 `data/profile.yaml`；研报/作品集一律走 `data/monographs_src/`。
   - **版式眉题/FIG·TABLE 编号/筛选 label/卡片标题/导航等"游离文字"已用 `scripts/add_free_float_slots.py` 增补为 slot**，真正做到 100% 文字接管；仅剩「时间轴日期(带年限徽标)」与「图表 JS 内坐标轴/图例/数据标签」豁免（前者属时间轴数据、后者按规则属图表数据，不入 yaml）。

2. **严禁手改 `monographs/*.html` 与 `作品集.html` 的正文**；措辞/逻辑统一只改 `data/monographs_src/*.yaml` 的 `text`，再渲染。

3. **渲染唯一入口 = `scripts/build_monographs_from_yaml.py`**（方案 C：成品即外壳 + data-slot 原位回填）：
   ```bash
   python3 scripts/build_monographs_from_yaml.py --backup --diff          # 逐份独立 diff 门禁后覆盖
   python3 scripts/build_monographs_from_yaml.py --only 遵义大酒店 --dry-run --diff
   python3 scripts/build_monographs_from_yaml.py --force                  # 成品被手改后强制以当前为基线
   ```
   - 门禁：骨架标签序列（shell tpl vs 渲染）必须一致；text 每 slot == 期望；失败写 `data/monographs_diff_report.txt` 退出码 1。
   - `--backup` 备份到 `data/monographs_backup/<ts>/`（已 gitignore，隔离目录）。

4. **外壳模板 `data/monographs_tpl/<slug>.tpl.html` + 抽取器 `scripts/build_monographs_slots.py`**：
   - 仅当 HTML 结构/新增节点确需变化时才重抽取：`python3 scripts/build_monographs_slots.py`（tpl 忽略 data-slot 后须与成品 byte 级一致才通过）。
   - 抽取/渲染/校验共用 `scripts/slotlib.py`（linearize / render_md / slot_regions / skeleton_html / tag_norm）。

5. **图表 JS/样式/布局结构一律不进 yaml**；ECharts 中 JS 渲染的坐标轴/图例/数据标签属图表 JS 数据。渲染后必须跑 Playwright：
   ```bash
   python3 scripts/playwright_verify_monographs.py
   ```
   断言每个 `.chart-container` 有已初始化的 `<canvas>`、抽查 yaml 文字端点到场、全页截图存 `data/monographs_backup/verify_shots/`。

<!-- text_yaml_number_duckdb_boundary -->
## 🧭 数据存储边界（文字 vs 数字）

- **文字/措辞/标题/正文  走 `data/monographs_src/*.yaml`**（外加首页 `data/profile.yaml`）。内容型、低改动频、要给人/agent 读改与 git diff，YAML 是唯一主场。
- **数字指标（产值/工时/LOC/合同额等）走 DuckDB 湖仓**（`v_ai_*` 视图），渲染时注入，不在文案里硬编码；DuckDB 价值在分析查询，不是存文案。
- **禁用 SQLite** 承接这些数据：比 YAML 更难读/难 diff、数值又弱于 DuckDB，纯增复杂度；如确需追加存储生态位，先与本结论对齐。
- 一致性靠"边界"而非"存储"：措辞只许改 yaml、数字只许出自 DuckDB 视图；渲染门禁（structure/text/byte_eq/Playwright）兜底防漂移。