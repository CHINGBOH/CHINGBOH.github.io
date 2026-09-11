import marimo

__generated_with = "0.11.0"
app = marimo.App(
    width="full",
    layout_file=None,
)


@app.cell
def __():
    import base64
    import io
    import duckdb
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import marimo as mo

    # 统一 Matplotlib 高清学术与中文/LaTeX 字体配置
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'SimSun', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['svg.fonttype'] = 'path'
    plt.rcParams['mathtext.fontset'] = 'cm'

    return base64, duckdb, io, matplotlib, mo, np, pd, plt


@app.cell
def __(duckdb):
    # 连接 DuckDB 并加载上海华泰中心售楼处专项视图群
    conn = duckdb.connect()
    with open('/home/l/个人资料仓库/data/views_huatai_direct_excel.sql') as f:
        _sql = f.read()
    conn.execute(_sql)

    # 提取核心历史真值事实
    cost_budget_df = conn.execute("SELECT * FROM v_ht_cost_budget_comparison").df()
    evolution_df = conn.execute("SELECT * FROM v_ht_multiround_pricing_evolution").df()
    category_df = conn.execute("SELECT * FROM v_ht_contract_category_summary").df()
    payment_terms_df = conn.execute("SELECT * FROM v_ht_contract_payment_terms").df()
    spatial_summary_df = conn.execute("SELECT * FROM v_ht_spatial_zone_summary").df()
    spatial_detail_df = conn.execute("SELECT * FROM v_ht_spatial_zone_inventory").df()

    # 核心标尺常量
    initial_quote = 176.40  # 初轮测算报价 (万元)
    contract_amt = 156.66   # 最终闭口合同总价 (万元)
    direct_cost = 79.66     # 工厂直采+物流直接成本 (万元)
    area_m2 = 600.0         # 售楼处展示面积 (㎡)
    sqm_price = 2610.92     # 单方造价 (元/㎡)
    duration_days = 35      # 总工期 (天)
    item_count = 281        # 实物件数
    style_count = 78        # 物料款式数

    return (
        area_m2,
        category_df,
        conn,
        contract_amt,
        cost_budget_df,
        direct_cost,
        duration_days,
        evolution_df,
        initial_quote,
        item_count,
        payment_terms_df,
        spatial_detail_df,
        spatial_summary_df,
        sqm_price,
        style_count,
    )


@app.cell
def __(mo):
    # 神仙技能 1: 高管侧边栏驱动源切换 (滑轮 vs 数值输入)
    input_mode = mo.ui.radio(
        options=["滑轮拖动模式", "具体数值输入模式"],
        value="具体数值输入模式",
        label="🎛️ 调参驱动源"
    )

    # 控制器 1: 竞标调价折让率 (%) (默认 11.19% 对应 176.40 万降至 156.66 万)
    slider_discount = mo.ui.slider(
        start=0.0, stop=20.0, step=0.1, value=11.19,
        label="滑轮调节竞标折让率"
    )
    number_discount = mo.ui.number(
        start=0.0, stop=20.0, step=0.01, value=11.19,
        label="输入精确折让率 (%)"
    )

    # 控制器 2: 源头采购与工艺平替降本率 (%) (默认 10.0%)
    slider_cost_save = mo.ui.slider(
        start=0.0, stop=25.0, step=0.5, value=10.0,
        label="滑轮调节工艺降本"
    )
    number_cost_save = mo.ui.number(
        start=0.0, stop=25.0, step=0.1, value=10.0,
        label="输入精确降本率 (%)"
    )

    # 控制器 3: 出货前回款控制比例 (%) (默认 70.0% 刚性覆盖)
    slider_pre_rate = mo.ui.slider(
        start=50.0, stop=90.0, step=1.0, value=70.0,
        label="滑轮调节出货前回款率"
    )
    number_pre_rate = mo.ui.number(
        start=50.0, stop=90.0, step=0.5, value=70.0,
        label="输入出货回款率 (%)"
    )

    # 控制器 4: 空间功能区过滤
    zone_selector = mo.ui.dropdown(
        options=["全部功能区", "营销核心洽谈区", "三层行政贵宾专区", "营销办公与经理室", "公共通道与配套区", "大堂与前台接待区", "环幕影音体验厅", "沙盘模型展示区"],
        value="全部功能区",
        label="楼层空间钻取"
    )

    return (
        input_mode,
        number_cost_save,
        number_discount,
        number_pre_rate,
        slider_cost_save,
        slider_discount,
        slider_pre_rate,
        zone_selector,
    )


@app.cell
def __(
    input_mode,
    mo,
    number_cost_save,
    number_discount,
    number_pre_rate,
    slider_cost_save,
    slider_discount,
    slider_pre_rate,
    zone_selector,
):
    # 动静解耦参数提取器 (完全消除白屏)
    if input_mode.value == "具体数值输入模式":
        sim_discount = float(number_discount.value) if number_discount.value is not None else 11.19
        sim_cost_save = float(number_cost_save.value) if number_cost_save.value is not None else 10.0
        sim_pre_rate = float(number_pre_rate.value) if number_pre_rate.value is not None else 70.0
    else:
        sim_discount = float(slider_discount.value) if slider_discount.value is not None else 11.19
        sim_cost_save = float(slider_cost_save.value) if slider_cost_save.value is not None else 10.0
        sim_pre_rate = float(slider_pre_rate.value) if slider_pre_rate.value is not None else 70.0

    # 组装高管全局侧边栏 (彻底移除 CSV 下载链接，强化三色认知锚定)
    sidebar = mo.sidebar([
        mo.md("## 🏛️ 高管全局操盘控制台"),
        mo.md("*上海华泰中心售楼处 · 招投标与闭口合同实时推演*"),
        mo.md("---"),
        input_mode,
        mo.md("---"),
        mo.Html("<div style='background:#f0f9ff; border:1px solid #bae6fd; border-left:4px solid #0284c7; padding:8px 10px; border-radius:4px; font-weight:600; color:#0369a1;'>📊 1. 竞标调价折让率调优</div>"),
        slider_discount,
        number_discount,
        mo.md("---"),
        mo.Html("<div style='background:#f0fdf4; border:1px solid #bbf7d0; border-left:4px solid #16a34a; padding:8px 10px; border-radius:4px; font-weight:600; color:#15803d;'>🏭 2. 源头采购工艺降本调优</div>"),
        slider_cost_save,
        number_cost_save,
        mo.md("---"),
        mo.Html("<div style='background:#fefce8; border:1px solid #fef08a; border-left:4px solid #ca8a04; padding:8px 10px; border-radius:4px; font-weight:600; color:#854d0e;'>💰 3. 出货前回款控制率调优</div>"),
        slider_pre_rate,
        number_pre_rate,
        mo.md("---"),
        mo.md("🔍 **空间资产钻取**"),
        zone_selector,
        mo.md("---"),
        mo.md("<div style='font-size:11px; color:#64748b; line-height:1.5;'>梁清波 商业专案库 · Marimo Reactive Engine<br>项目代号：SH-HT-201508</div>")
    ])

    return (
        sidebar,
        sim_cost_save,
        sim_discount,
        sim_pre_rate,
    )


@app.cell
def __(sidebar):
    sidebar
    return


@app.cell
def __(
    area_m2,
    direct_cost,
    initial_quote,
    input_mode,
    mo,
    sim_cost_save,
    sim_discount,
    sim_pre_rate,
):
    # 动态推演核心算法模型
    # 1. 竞标推演成交价 = 初轮报价 * (1 - 折让率)
    calc_win_price = initial_quote * (1.0 - sim_discount / 100.0)
    # 2. 采购直接成本 = 基准成本 * (1 - 工艺降本率)
    calc_cost = direct_cost * (1.0 - sim_cost_save / 100.0)
    # 3. 经营毛利率
    calc_margin_amt = calc_win_price - calc_cost
    calc_margin_rate = (calc_margin_amt / calc_win_price) * 100.0 if calc_win_price > 0 else 0.0
    # 4. 出货前回收金额与覆盖倍数
    calc_pre_ship_cash = calc_win_price * (sim_pre_rate / 100.0)
    calc_coverage_ratio = (calc_pre_ship_cash / calc_cost) * 100.0 if calc_cost > 0 else 0.0
    # 5. 单方造价定额
    calc_sqm_price = (calc_win_price * 10000.0) / area_m2

    # 模式提示指示条
    _mode_str = f"<span style='color:#0284c7; font-weight:700;'>⚙️ {input_mode.value}生效</span> · 实时调优参数同步："
    _param_badges = f"""
    <span style='background:#f0f9ff; border:1px solid #bae6fd; color:#0369a1; padding:2px 8px; border-radius:4px; font-size:12px; margin-right:6px;'>📊 竞标折让 {sim_discount:.2f}%</span>
    <span style='background:#f0fdf4; border:1px solid #bbf7d0; color:#15803d; padding:2px 8px; border-radius:4px; font-size:12px; margin-right:6px;'>🏭 工艺降本 {sim_cost_save:.1f}%</span>
    <span style='background:#fefce8; border:1px solid #fef08a; color:#854d0e; padding:2px 8px; border-radius:4px; font-size:12px;'>💰 出货回款率 {sim_pre_rate:.1f}%</span>
    """

    kpi_cards_html = mo.Html(f"""
    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:8px 16px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center; font-size:12.5px;">
      <div>{_mode_str} {_param_badges}</div>
      <div style="color:#64748b; font-size:11px;">与左侧控制台色彩 100% 视觉锚定</div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 22px;">
      <!-- 卡片 1: 竞标推演中标闭口金额 (蓝色锚定) -->
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #0284c7; border-radius: 8px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="font-size: 11.5px; color: #64748b; font-weight: 500;">推演中标闭口金额</div>
        <div style="font-size: 24px; font-weight: 700; color: #0f172a; margin: 4px 0;">{calc_win_price:,.2f} <span style="font-size: 13px; font-weight: 400; color: #64748b;">万元</span></div>
        <div style="margin-top: 4px; display: flex; gap: 4px; flex-wrap: wrap;">
          <span style="background: #f0f9ff; border: 1px solid #bae6fd; color: #0369a1; padding: 1px 6px; border-radius: 3px; font-size: 11px;">📊 折让 {sim_discount:.2f}%</span>
          <span style="background: #f8fafc; border: 1px solid #e2e8f0; color: #475569; padding: 1px 6px; border-radius: 3px; font-size: 11px;">基准 176.40万</span>
        </div>
      </div>

      <!-- 卡片 2: 综合经营毛利率 (绿色锚定) -->
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #16a34a; border-radius: 8px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="font-size: 11.5px; color: #64748b; font-weight: 500;">推演综合毛利率 (空间)</div>
        <div style="font-size: 24px; font-weight: 700; color: #15803d; margin: 4px 0;">{calc_margin_rate:.1f}% <span style="font-size: 13px; font-weight: 400; color: #64748b;">({calc_margin_amt:,.2f}万)</span></div>
        <div style="margin-top: 4px;">
          <span style="background: #f0fdf4; border: 1px solid #bbf7d0; color: #15803d; padding: 1px 6px; border-radius: 3px; font-size: 11px;">🏭 工艺降本 {sim_cost_save:.1f}% 护盘</span>
        </div>
      </div>

      <!-- 卡片 3: 出货前回款覆盖倍数 (金色锚定) -->
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #ca8a04; border-radius: 8px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="font-size: 11.5px; color: #64748b; font-weight: 500;">出货前资金覆盖倍数</div>
        <div style="font-size: 24px; font-weight: 700; color: #0f172a; margin: 4px 0;">{calc_coverage_ratio:.1f}% <span style="font-size: 13px; font-weight: 400; color: #64748b;">(已收{calc_pre_ship_cash:,.2f}万)</span></div>
        <div style="margin-top: 4px;">
          <span style="background: #fefce8; border: 1px solid #fef08a; color: #854d0e; padding: 1px 6px; border-radius: 3px; font-size: 11px;">💰 零垫资安全出厂</span>
        </div>
      </div>

      <!-- 卡片 4: 单方精奢造价定额 (海青色) -->
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #0f766e; border-radius: 8px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="font-size: 11.5px; color: #64748b; font-weight: 500;">单方精奢造价定额</div>
        <div style="font-size: 24px; font-weight: 700; color: #0f766e; margin: 4px 0;">{calc_sqm_price:,.2f} <span style="font-size: 13px; font-weight: 400; color: #64748b;">元/㎡</span></div>
        <div style="margin-top: 4px;">
          <span style="background: #f0fdfa; border: 1px solid #99f6e4; color: #0f766e; padding: 1px 6px; border-radius: 3px; font-size: 11px;">600 ㎡ · 281 件实物总控</span>
        </div>
      </div>
    </div>
    """)

    return (
        calc_cost,
        calc_coverage_ratio,
        calc_margin_amt,
        calc_margin_rate,
        calc_pre_ship_cash,
        calc_sqm_price,
        calc_win_price,
        kpi_cards_html,
    )


@app.cell
def __(
    base64,
    category_df,
    cost_budget_df,
    evolution_df,
    io,
    payment_terms_df,
    plt,
    spatial_summary_df,
):
    # 动静解耦：预先渲染 4 张原生矢量 SVG 商业图表 (format='svg', svg.fonttype='path')

    # -------------------------------------------------------------
    # 图表 1: 五轮竞争性调价瀑布演进图 (万元)
    # -------------------------------------------------------------
    _fig1, _ax1 = plt.subplots(figsize=(7.8, 3.4), dpi=140)
    _stages = ['初轮测算\n(07-28)', '第1轮调价\n(08-07)', '第2轮调价\n(08-09)', '第3轮审定\n(08-10)', '第4轮封板\n(08-11)', '最终签约\n(08-14)']
    _amts = evolution_df['报价金额_万元'].tolist()
    _colors1 = ['#3b82f6', '#60a5fa', '#93c5fd', '#f59e0b', '#10b981', '#1e40af']
    _bars1 = _ax1.bar(_stages, _amts, color=_colors1, width=0.48, edgecolor='#1e293b', linewidth=0.7)
    _ax1.set_ylabel('报价金额 (万元)', fontsize=9, fontweight='bold')
    _ax1.set_ylim(140, 185)
    _ax1.set_title('上海华泰中心售楼处 · 五轮竞争性商务调价博弈轨迹', fontsize=11, fontweight='bold', pad=12)
    _ax1.grid(axis='y', linestyle='--', alpha=0.3)
    _ax1.spines['top'].set_visible(False)
    _ax1.spines['right'].set_visible(False)

    for _bar, _val in zip(_bars1, _amts):
        _h = _bar.get_height()
        _is_final = (_val == 156.66)
        _ax1.annotate(f'{_val:.2f}万',
                     xy=(_bar.get_x() + _bar.get_width() / 2, _h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8.5,
                     fontweight='bold' if _is_final else 'normal',
                     color='#b91c1c' if _is_final else '#0f172a')

    _fig1.subplots_adjust(left=0.10, right=0.95, top=0.88, bottom=0.18)
    _buf1 = io.BytesIO()
    _fig1.savefig(_buf1, format='svg', bbox_inches='tight')
    plt.close(_fig1)
    _buf1.seek(0)
    chart1_b64 = base64.b64encode(_buf1.getvalue()).decode('utf-8')

    # -------------------------------------------------------------
    # 图表 2: 6 大核心品类采销毛利双轨对比图 (万元)
    # -------------------------------------------------------------
    _fig2, _ax2 = plt.subplots(figsize=(7.8, 3.4), dpi=140)
    _cats = [c.replace('、', ' ') for c in cost_budget_df['品类']]
    _costs = (cost_budget_df['直采成本_元'] / 1e4).tolist()
    _quotes = (cost_budget_df['目标报价_元'] / 1e4).tolist()

    _x = range(len(_cats))
    _w = 0.35
    _b_cost = _ax2.bar([i - _w/2 for i in _x], _costs, width=_w, label='厂家直采成本', color='#94a3b8', edgecolor='#334155', linewidth=0.6)
    _b_quote = _ax2.bar([i + _w/2 for i in _x], _quotes, width=_w, label='目标商务报价', color='#0284c7', edgecolor='#0369a1', linewidth=0.6)

    _ax2.set_xticks(list(_x))
    _ax2.set_xticklabels(_cats, fontsize=8.5, fontweight='bold')
    _ax2.set_ylabel('金额 (万元)', fontsize=9, fontweight='bold')
    _ax2.set_title('6 大核心品类源头直采成本 vs 目标商务报价双轨模型', fontsize=11, fontweight='bold', pad=12)
    _ax2.legend(frameon=True, fontsize=8.5)
    _ax2.grid(axis='y', linestyle='--', alpha=0.3)
    _ax2.spines['top'].set_visible(False)
    _ax2.spines['right'].set_visible(False)

    for _bar in _b_quote:
        _h = _bar.get_height()
        _ax2.annotate(f'{_h:.1f}万', xy=(_bar.get_x() + _bar.get_width()/2, _h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

    _fig2.subplots_adjust(left=0.10, right=0.95, top=0.88, bottom=0.18)
    _buf2 = io.BytesIO()
    _fig2.savefig(_buf2, format='svg', bbox_inches='tight')
    plt.close(_fig2)
    _buf2.seek(0)
    chart2_b64 = base64.b64encode(_buf2.getvalue()).decode('utf-8')

    # -------------------------------------------------------------
    # 图表 3: 30/40/25/5 极速回款资金收支瀑布流 (万元)
    # -------------------------------------------------------------
    _fig3, _ax3 = plt.subplots(figsize=(7.8, 3.2), dpi=140)
    _nodes = ['预付备料款\n(30%)', '出货前节点\n(累计70%)', '直接出厂成本\n(采购+物流)', '摆场验收款\n(累计95%)', '质量保证金\n(5%期满)']
    _cash_vals = [47.00, 109.66, 79.66, 148.82, 156.66]
    _colors3 = ['#38bdf8', '#0284c7', '#dc2626', '#10b981', '#059669']

    _bars3 = _ax3.bar(_nodes, _cash_vals, color=_colors3, width=0.45, edgecolor='#1e293b', linewidth=0.7)
    _ax3.set_ylabel('累计现金流 (万元)', fontsize=9, fontweight='bold')
    _ax3.set_ylim(0, 180)
    _ax3.set_title('30/40/25/5 阶段付款节点 · 出货前累计回收 109.66 万全额覆盖出厂成本', fontsize=10.5, fontweight='bold', pad=12)
    _ax3.axhline(79.66, color='#dc2626', linestyle='--', linewidth=1.2, label='出厂直接成本 79.66万 刚性安全线')
    _ax3.legend(frameon=True, fontsize=8.5, loc='upper left')
    _ax3.grid(axis='y', linestyle='--', alpha=0.3)
    _ax3.spines['top'].set_visible(False)
    _ax3.spines['right'].set_visible(False)

    for _bar, _val in zip(_bars3, _cash_vals):
        _h = _bar.get_height()
        _ax3.annotate(f'{_val:.2f}万', xy=(_bar.get_x() + _bar.get_width()/2, _h),
                     xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    _fig3.subplots_adjust(left=0.10, right=0.95, top=0.88, bottom=0.18)
    _buf3 = io.BytesIO()
    _fig3.savefig(_buf3, format='svg', bbox_inches='tight')
    plt.close(_fig3)
    _buf3.seek(0)
    chart3_b64 = base64.b64encode(_buf3.getvalue()).decode('utf-8')

    # -------------------------------------------------------------
    # 图表 4: 7 大功能空间物料件数与款式分布 (横向条形图)
    # -------------------------------------------------------------
    _fig4, _ax4 = plt.subplots(figsize=(7.8, 3.4), dpi=140)
    _zones = spatial_summary_df['主要功能区'].tolist()[::-1]
    _counts = spatial_summary_df['物料总件数'].tolist()[::-1]
    _styles = spatial_summary_df['物料款式数'].tolist()[::-1]

    _y = range(len(_zones))
    _bars4 = _ax4.barh(_y, _counts, color='#0f766e', height=0.55, edgecolor='#134e4a', linewidth=0.6)
    _ax4.set_yticks(list(_y))
    _ax4.set_yticklabels(_zones, fontsize=8.5, fontweight='bold')
    _ax4.set_xlabel('配置物料件数 (件/套)', fontsize=9, fontweight='bold')
    _ax4.set_title('售楼处 7 大功能分区实物资产配置分布 (合计 281 件 / 78 款)', fontsize=11, fontweight='bold', pad=12)
    _ax4.grid(axis='x', linestyle='--', alpha=0.3)
    _ax4.spines['top'].set_visible(False)
    _ax4.spines['right'].set_visible(False)

    for _bar, _cnt, _stl in zip(_bars4, _counts, _styles):
        _w = _bar.get_width()
        _ax4.annotate(f'{_cnt} 件 ({_stl}款)', xy=(_w, _bar.get_y() + _bar.get_height()/2),
                     xytext=(6, 0), textcoords="offset points", ha='left', va='center', fontsize=8.5, fontweight='bold', color='#0f172a')

    _fig4.subplots_adjust(left=0.22, right=0.88, top=0.88, bottom=0.15)
    _buf4 = io.BytesIO()
    _fig4.savefig(_buf4, format='svg', bbox_inches='tight')
    plt.close(_fig4)
    _buf4.seek(0)
    chart4_b64 = base64.b64encode(_buf4.getvalue()).decode('utf-8')

    return chart1_b64, chart2_b64, chart3_b64, chart4_b64


@app.cell
def __(
    area_m2,
    chart1_b64,
    chart2_b64,
    chart3_b64,
    chart4_b64,
    contract_amt,
    direct_cost,
    duration_days,
    initial_quote,
    item_count,
    mo,
    sqm_price,
    style_count,
):
    # Tab 1: 典藏级全景商业研报正文构建 (完全遵循招投标与闭口合同架构)
    tab1_content = mo.vstack([
        mo.md("## § 0 核心商业基本盘与招投标指标全景"),
        mo.Html(f"""
        <table style="width:100%; font-size:13px; line-height:1.7; border-collapse:collapse; margin-bottom:20px;">
          <thead>
            <tr style="background:#f1f5f9; border-bottom:2px solid #cbd5e1; text-align:left;">
              <th style="padding:8px 12px;">商业业务维度</th>
              <th style="padding:8px 12px;">量化指标名称</th>
              <th style="padding:8px 12px; text-align:right;">审计核定真值</th>
              <th style="padding:8px 12px; text-align:center;">操盘控制属性</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #e2e8f0;">
              <td style="padding:8px 12px; color:#64748b;">承揽方式</td>
              <td style="padding:8px 12px; font-weight:600;">开发商正式招投标 · 闭口价竞标</td>
              <td style="padding:8px 12px; text-align:right; font-weight:700; color:#0369a1;">五轮竞争性报价</td>
              <td style="padding:8px 12px; text-align:center;"><span style="background:#e0f2fe; color:#0369a1; padding:2px 8px; border-radius:4px; font-size:11px;">自主总控直签</span></td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0;">
              <td style="padding:8px 12px; color:#64748b;">初轮测算</td>
              <td style="padding:8px 12px; font-weight:600;">预算清单初轮测算报价总额</td>
              <td style="padding:8px 12px; text-align:right; font-weight:700; color:#0f172a;">{initial_quote:,.2f} 万元</td>
              <td style="padding:8px 12px; text-align:center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">预留 11.2% 谈判纵深</span></td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0;">
              <td style="padding:8px 12px; color:#64748b;">中标签约</td>
              <td style="padding:8px 12px; font-weight:600;">最终签署固定总价包干合同总额</td>
              <td style="padding:8px 12px; text-align:right; font-weight:700; color:#b91c1c;">{contract_amt:,.2f} 万元</td>
              <td style="padding:8px 12px; text-align:center;"><span style="background:#fee2e2; color:#b91c1c; padding:2px 8px; border-radius:4px; font-size:11px;">固定闭口 · 零核减</span></td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0;">
              <td style="padding:8px 12px; color:#64748b;">单方定额</td>
              <td style="padding:8px 12px; font-weight:600;">实测展示面积折合单方造价</td>
              <td style="padding:8px 12px; text-align:right; font-weight:700; color:#0f766e;">{sqm_price:,.2f} 元/㎡</td>
              <td style="padding:8px 12px; text-align:center;"><span style="background:#ccfbf1; color:#0f766e; padding:2px 8px; border-radius:4px; font-size:11px;">600 ㎡ 精奢展厅</span></td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0;">
              <td style="padding:8px 12px; color:#64748b;">源头采购</td>
              <td style="padding:8px 12px; font-weight:600;">珠三角工厂直接采购与物流成本</td>
              <td style="padding:8px 12px; text-align:right; font-weight:700; color:#475569;">{direct_cost:,.2f} 万元</td>
              <td style="padding:8px 12px; text-align:center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">直连顺德/中山工坊</span></td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0;">
              <td style="padding:8px 12px; color:#64748b;">回款阀门</td>
              <td style="padding:8px 12px; font-weight:600;">出货前提货款累计回收金额 (70%)</td>
              <td style="padding:8px 12px; text-align:right; font-weight:700; color:#15803d;">109.66 万元</td>
              <td style="padding:8px 12px; text-align:center;"><span style="background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:4px; font-size:11px;">覆盖成本 137.7% (零垫资)</span></td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0;">
              <td style="padding:8px 12px; color:#64748b;">履约总工期</td>
              <td style="padding:8px 12px; font-weight:600;">自开工至售楼处盛大开盘总天数</td>
              <td style="padding:8px 12px; text-align:right; font-weight:700; color:#0f172a;">{duration_days} 个日历天</td>
              <td style="padding:8px 12px; text-align:center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">现场集中 3 天开盘摆场</span></td>
            </tr>
            <tr>
              <td style="padding:8px 12px; color:#64748b;">实物交付</td>
              <td style="padding:8px 12px; font-weight:600;">7 大功能分区实物资产清单总数</td>
              <td style="padding:8px 12px; text-align:right; font-weight:700; color:#0f172a;">{item_count} 件 / {style_count} 款物料</td>
              <td style="padding:8px 12px; text-align:center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">大堂挑空吊灯拼装点亮</span></td>
            </tr>
          </tbody>
        </table>
        """),

        mo.md("## § 1 商业承揽与正式招投标竞争性博弈"),
        mo.md("""
        * **开发商闭口招标架构**：上海华泰中心售楼处（华邦·上海江桥销售中心，约 600 ㎡）是梁清波独立主导拓展、直签业主投资方上海华泰置业有限公司的标杆性商办营销工程。与政府暂定总价项目不同，本项目采用**开发商正式招投标 / 闭口总价竞标**模式；
        * **五轮调价博弈全记录**：
          1. `2015-07-28 初轮测算版 (176.40 万元)`：编制内部采销测算底账，单方 2,940 元/㎡，主动预留 11.2%（19.74 万元）商务谈判纵深；
          2. `2015-08-07 第一轮商务调价 (168.39 万元)`：针对大堂挑空水晶大吊灯工艺进行参数强化（灯具由 40.0 万上调至 52.3 万），饰品花艺主动让利至 38.1 万；
          3. `2015-08-09 第二轮商务调价 (169.75 万元)`：响应营销总现场动线优化，增加洽谈区 2 人位沙发与家具单项，报价微调 1.36 万元；
          4. `2015-08-10 第三轮甲方审定确定版 (156.22 万元)`：竞争进入白热化，梁清波团队启动工艺平替策略（优化水晶挂件与地毯克重），将合同基准锁定在 156.0 万元防线；
          5. `2015-08-11 第四轮封板报价清单 (156.33 万元)`：各方逐页签字盖章确认，清单核定价为 1,563,277.00 元；
          6. `2015-08-14 最终签署合同清稿版 (156.66 万元)`：根据上海华洽合同第 7 条，以 **1,566,550.00 元固定总价包干**签约锁定，此后按图供货、不再调价！
        """),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{chart1_b64}' alt='五轮竞争性调价瀑布演进图'></div>"),

        mo.md("## § 2 采销双轨源头穿透与工艺平替降本"),
        mo.md("""
        * **穿透珠三角产业集群源头白胚**：跳过中间流通层级，直连东莞大岭山实木家具厂与中山古镇高定灯具厂，获取源头工坊白胚裸价。家具直采成本 23.64 万元，灯具直采成本 16.01 万元，前置锁定直接采购底盘；
        * **家具与定制灯具双核驱动**：封板合同中定制灯具（46.12 万元，占 29.5%）与定制家具（45.16 万元，占 28.9%）合计占比 **58.4%**，牢牢掌控了售楼处的核心视觉高溢价主材；
        * **出厂前飞检与零瑕疵装配**：梁清波亲自飞赴东莞与中山工厂，现场对 3 米直径、4.5 米挑空水晶大吊灯的受力骨架与五金件进行预拼装试挂与通电飞检，确保一次性拼装点亮。
        """),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{chart2_b64}' alt='6大核心品类采销毛利双轨对比图'></div>"),

        mo.md("## § 3 30/40/25/5 极速回款防线与零垫资闭环"),
        mo.md("""
        * **30% 预付备料款（47.00 万元）**：合同签订 7 个工作日内即刻到账，直接用于支付工厂定金与原材料锁定，项目从第 1 天起即处于正向现金流状态；
        * **40% 出货前节点款（累计 70%，109.66 万元）**：严格执行“工厂验货合格打款后发货”的刚性法务阀门。出货前回收的 109.66 万元，全额覆盖珠三角采购及干线物流直接成本（79.66 万元）的 **137.7%**，实现真正的**零垫资出厂**！
        * **25% 摆场验收款（累计 95%，148.82 万元）**：现场集中 3 天摆场完毕并协助开盘，验收合格后 10 个工作日内兑现，全案利润完全落袋；
        * **5% 质量保证金（7.83 万元）**：质保期 1 年届满后 10 个工作日内全额无息返还，零核减零坏账。
        """),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{chart3_b64}' alt='30/40/25/5资金收支瀑布流'></div>"),

        mo.md("## § 4 35 天极限工期倒排与 7 大功能空间实物配置"),
        mo.md("""
        * **35 天极限总工期严密倒排**：
          - 阶段一（8-15）：备料与首件封样，3 日内确定面料色板，5 日内提交灯具挂画清单；
          - 阶段二（8-16 至 9-07）：车间集中加工生产，组织甲方赴顺德/东莞验货；
          - 阶段三（9-08 至 9-14）：珠三角至上海长途干线物流运输，提前通知甲方场地保洁；
          - 阶段四（9-15 至 9-18）：现场集中 3 天完成大吊灯高空悬吊与 281 件物料摆场；
          - 阶段五（9-20）：甲方与设计方联合验收，售楼处如期盛大开盘！
        * **7 大功能空间 281 件实物配置**：营销核心洽谈区（178 件 / 36 款物料，占比 63.3%）与三层行政贵宾专区（29 件 / 14 款物料）为核心落位重心。
        """),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{chart4_b64}' alt='7大功能空间物料分布图'></div>")
    ])

    return tab1_content,


@app.cell
def __(
    base64,
    direct_cost,
    initial_quote,
    io,
    mo,
    np,
    pd,
    plt,
    sim_cost_save,
    sim_discount,
):
    # Tab 2: 竞标报价与供应链毛利动态推演矩阵 (热力图 + 场景推演量化对账表)
    _discounts = [5.0, 8.0, sim_discount, 14.0, 18.0]
    _cost_saves = [0.0, 5.0, sim_cost_save, 15.0, 20.0]

    _grid_margin_rate = np.zeros((len(_discounts), len(_cost_saves)))
    _matrix_data = []

    for _i, _disc in enumerate(_discounts):
        _row = {"竞标折让率": f"{_disc:.2f}%"}
        _win_p = initial_quote * (1.0 - _disc / 100.0)
        for _j, _cs in enumerate(_cost_saves):
            _c = direct_cost * (1.0 - _cs / 100.0)
            _m_amt = _win_p - _c
            _m_rate = (_m_amt / _win_p) * 100.0 if _win_p > 0 else 0.0
            _grid_margin_rate[_i, _j] = _m_rate
            _row[f"降本 {_cs:.1f}%"] = f"{_m_rate:.1f}% ({_m_amt:.1f}万)"
        _matrix_data.append(_row)

    _matrix_df = pd.DataFrame(_matrix_data)

    # 绘制推演热力图 (注意 ax=_ax_sens 传参避免轴冲突)
    _fig_sens, _ax_sens = plt.subplots(figsize=(7.6, 3.8), dpi=140)
    _im = _ax_sens.imshow(_grid_margin_rate, cmap='YlGnBu', aspect='auto')
    _ax_sens.set_xticks(range(len(_cost_saves)))
    _ax_sens.set_yticks(range(len(_discounts)))
    _ax_sens.set_xticklabels([f'降本 {_cs:.1f}%' for _cs in _cost_saves], fontsize=8.5, fontweight='bold')
    _ax_sens.set_yticklabels([f'折让 {_disc:.2f}%' for _disc in _discounts], fontsize=8.5, fontweight='bold')
    _cbar = _fig_sens.colorbar(_im, ax=_ax_sens, fraction=0.035, pad=0.04)
    _cbar.ax.set_ylabel('推演经营毛利率 (%)', fontsize=8.5)

    for _i in range(len(_discounts)):
        for _j in range(len(_cost_saves)):
            _val = _grid_margin_rate[_i, _j]
            _is_actual = (abs(_discounts[_i] - 11.19) < 0.05 and abs(_cost_saves[_j] - 10.0) < 0.05)
            _txt_color = '#dc2626' if _is_actual else ('#ffffff' if _val > 45 else '#0f172a')
            _prefix = '★实际: ' if _is_actual else ''
            _ax_sens.text(_j, _i, f'{_prefix}{_val:.1f}%', ha='center', va='center',
                          fontsize=8.5, fontweight='bold' if _is_actual else 'normal', color=_txt_color)

    _ax_sens.set_title('华泰售楼处 · 竞标让利 vs 供应链降本推演矩阵 (推演毛利率)', fontsize=11, fontweight='bold', pad=12)
    _fig_sens.subplots_adjust(left=0.15, right=0.92, top=0.88, bottom=0.15)
    _buf_sens = io.BytesIO()
    _fig_sens.savefig(_buf_sens, format='svg', bbox_inches='tight')
    plt.close(_fig_sens)
    _buf_sens.seek(0)
    _sens_b64 = base64.b64encode(_buf_sens.getvalue()).decode('utf-8')

    tab2_content = mo.vstack([
        mo.md("### 🎛️ 竞标报价让利与供应链降本双变量推演矩阵"),
        mo.md("通过在不同竞标折让压力（5% 至 18%）与源头工艺平替降本（0% 至 20%）之间的交叉推演，清晰验证：**梁清波团队通过前置预留 11.2% 调价弹性和工厂源头工艺优化，成功在 156.66 万元闭口中标的同时，死守 33.5%~34.8% 的健康经营毛利率！**"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{_sens_b64}' alt='敏感度热力图'></div>"),
        mo.md("#### 📊 场景推演量化对账表（毛利率与毛利额）"),
        mo.ui.table(_matrix_df)
    ])

    return tab2_content,


@app.cell
def __(mo, spatial_detail_df, zone_selector):
    # Tab 3: 7 大空间 281 件实物资产与 78 款物料原子级穿透台 - 声明表格组件
    # 支持空间下拉筛选联动
    if zone_selector.value != "全部功能区":
        _filtered_df = spatial_detail_df[spatial_detail_df['主要功能区'] == zone_selector.value]
    else:
        _filtered_df = spatial_detail_df

    table_spatial = mo.ui.table(
        _filtered_df,
        selection="single",
        label="📦 华泰售楼处 281 件实物资产穿透台账（点击某行穿透）"
    )

    return table_spatial,


@app.cell
def __(mo, spatial_detail_df, table_spatial, zone_selector):
    # Tab 3: 读取选中行状态并组装 Tab 3 视图 (解耦隔离防 RuntimeError)
    _selected_row = table_spatial.value
    if _selected_row is not None and not _selected_row.empty:
        _row = _selected_row.iloc[0]
        _status_hint = "🔎 当前选中穿透项"
    elif spatial_detail_df is not None and not spatial_detail_df.empty:
        _row = spatial_detail_df.iloc[0]
        _status_hint = "💡 典型物料穿透示例（可点击上方表格任意一行切换）"
    else:
        _row = None
        _status_hint = ""

    if _row is not None:
        _detail_card = f"""
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; border-radius: 6px; padding: 12px 16px; margin-top: 12px;">
          <h4 style="margin: 0 0 6px 0; color: #14532d; font-size: 14px;">{_status_hint}：{_row['产品名称']}（物料编号：{_row['物料编号']}）</h4>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 12.5px; color: #374151;">
            <div><strong>主要功能区：</strong>{_row['主要功能区']}</div>
            <div><strong>详细位置：</strong>{_row['详细空间位置']}</div>
            <div><strong>品类分类：</strong>{_row['品类']}</div>
            <div><strong>配置数量：</strong><span style="color:#15803d; font-weight:700;">{_row['数量']} {_row['单位']}</span></div>
            <div style="grid-column: span 4;"><strong>规格与造型参数：</strong><span class="mono-num">{_row['规格参数']}</span></div>
          </div>
        </div>
        """
    else:
        _detail_card = """
        <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 12px; margin-top: 12px; font-size: 12px; color: #64748b; text-align: center;">
          💡 提示：在上方表格中点击选中任意一行，此处将即时穿透显示该物品的材质工艺与空间配置！
        </div>
        """

    tab3_content = mo.vstack([
        mo.md("### 🔍 7 大空间 281 件实物资产与 78 款物料原子级穿透台"),
        mo.md(f"当前筛选空间范围：**{zone_selector.value}**（直连 DuckDB 湖仓 `v_ht_spatial_zone_inventory` 底账，支持点击表格单行穿透材质与选型）："),
        table_spatial,
        mo.Html(_detail_card)
    ])

    return tab3_content,


@app.cell
def __(contract_amt, mo):
    # Tab 4: 招投标档案卷宗与法定闭口合同原件索引 (mo.accordion)
    tab4_content = mo.vstack([
        mo.md("### ⚖️ 招投标档案卷宗与法定闭口合同原件索引"),
        mo.md("全案事实严格遵照《合同法》与正规开发商商业地产采购招投标标准归档："),
        mo.accordion({
            "📑 1. 开发商招标文件与正式招投标邀请函": mo.md(
                """
                - **《上海华泰中心售楼处软装工程招标文件》原件**：
                  - 招标人：上海华泰置业有限公司
                  - 工程地点：上海市嘉定区江桥核心商办地块
                  - 招标范围：销售中心约 600 ㎡ 室内软装全案（家具、灯具、窗帘、地毯、挂画、饰品花艺）
                  - 竞标模式：严格闭口总价竞标，中标后不调价
                """
            ),
            "📊 2. 五轮调价商务磋商与封板报价清单原件": mo.md(
                """
                - **《上海华泰中心售楼处报价清单 8-11》封面盖章核定价**：
                  - 核定总价：**1,563,277.00 元**
                  - 涵盖 6 大核心品类、78 款物料、281 件实物
                  - 完整记录初轮 176.40 万至最终封板的 5 轮调价与工艺平替抗辩底账
                """
            ),
            "📜 3. 正式签署的固定总价包干合同 (清稿版原件)": mo.md(
                f"""
                - **《上海华泰中心售楼处软装供货安装合同（8.14清稿版）》**：
                  - 合同编号：`SH-HT-201508`（档案编号 GR-2015-YW-031）
                  - 签约总价：**固定总价包干 ¥{contract_amt:,.2f} 万元（1,566,550.00 元）**
                  - 合同性质：图纸范围内总价固定包干，无现场签证增加，零核减闭环
                """
            ),
            "💰 4. 30/40/25/5 极速付款水单与发票结算凭证": mo.md(
                """
                - **银行收款水单与财务核销凭证**：
                  - 第一期：预付 30% 备料款 **47.00 万元**（开工即付）
                  - 第二期：出货前付至 70% **62.66 万元**（累计 109.66 万元，超额覆盖出厂直接成本）
                  - 第三期：摆场验收付至 95% **39.16 万元**（累计 148.82 万元，开盘交付）
                  - 第四期：质保金 5% **7.83 万元**（1年期满全额无息返还）
                """
            ),
            "⏱️ 5. 35 天极限工期排产表与现场联合验收纪要": mo.md(
                """
                - **现场开盘验收合格确认单**：
                  - 35 天总工期无一日延误
                  - 现场集中 3 天高空水晶大吊灯安全悬吊与 281 件物料精准摆场
                  - 获得业主营销团队与投资方一致好评，如期盛大开盘
                """
            )
        })
    ])

    return tab4_content,


@app.cell
def __(kpi_cards_html, mo, tab1_content, tab2_content, tab3_content, tab4_content):
    # 注入全栈学术级 LaTeX 衬线排版体系与 SVG 容器规范
    latex_style = mo.Html("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Noto+Serif+SC:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

      html, body, .marimo, .marimo-ui-element, .markdown, [data-marimo-app] {
        font-family: "Latin Modern Roman", "Computer Modern", "TeX Gyre Termes", "Lora", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif !important;
        background-color: #fcfbf9;
        color: #1a1a1a;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
      }

      h1, h2, h3, h4, h5, h6 {
        font-family: "Latin Modern Roman", "Computer Modern", "Lora", "Noto Serif SC", serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
      }

      h1 {
        font-size: 26px !important;
        border-bottom: 2px solid #0369a1 !important;
        padding-bottom: 8px !important;
        margin-bottom: 16px !important;
      }

      h2 {
        font-size: 20px !important;
        border-left: 4px solid #0284c7 !important;
        padding-left: 10px !important;
        margin-top: 28px !important;
        margin-bottom: 14px !important;
        color: #0369a1 !important;
      }

      h3 {
        font-size: 17px !important;
        margin-top: 20px !important;
        color: #1f2937 !important;
      }

      p, li {
        text-align: justify !important;
        text-justify: inter-ideograph !important;
      }

      blockquote {
        border-left: 3px solid #0284c7 !important;
        background: #f0f9ff !important;
        padding: 12px 20px !important;
        margin: 16px 0 !important;
        border-radius: 0 6px 6px 0 !important;
        color: #0c4a6e !important;
      }

      table {
        font-family: "Latin Modern Roman", "Lora", "Noto Serif SC", serif !important;
        border-collapse: collapse !important;
      }

      code, pre, .mono-num {
        font-family: "Latin Modern Mono", "Computer Modern Typewriter", "JetBrains Mono", monospace !important;
      }

      .chart-svg-box {
        text-align: center;
        margin: 16px 0;
        padding: 10px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
      }
      .chart-svg-box img {
        width: 100%;
        max-width: 820px;
        height: auto;
        display: block;
        margin: 0 auto;
      }
    </style>
    """)

    # 4 大 Tabs 视界无缝切换总装
    report_tabs = mo.ui.tabs({
        "🏛️ 全景深度商业研报": tab1_content,
        "🎛️ 竞标调价与降本推演矩阵": tab2_content,
        "🔍 7 大空间 281 件实物穿透": tab3_content,
        "⚖️ 招投标卷宗与闭口合同索引": tab4_content,
    })

    main_view = mo.vstack([
        latex_style,
        mo.md("# 上海华泰中心售楼处商业统筹研报"),
        mo.md("**梁清波 商业专案库 · 项目代号 SH-HT-201508 · 正式招投标与闭口合同操盘旗帜**"),
        mo.md("""
        > 🏛️ **招投标实操与商业架构说明**：本项目系正规商业地产开发商（上海华泰置业）**正式招投标、闭口总价竞标**标杆项目。全案经 5 轮竞争性调价博弈，以 156.66 万元闭口中标签约，坚决守住 33.5% 经营毛利；设立 30/40/25/5 付款节点，在出厂前回收 70%（109.66 万元）超额覆盖出厂直接成本，达成**零垫资出厂**极速商业周转。
        """),
        kpi_cards_html,
        report_tabs
    ])

    return latex_style, main_view, report_tabs


@app.cell
def __(main_view):
    main_view
    return


if __name__ == "__main__":
    app.run()
