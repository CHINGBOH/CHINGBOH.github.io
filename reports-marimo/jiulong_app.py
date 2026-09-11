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
    # 连接 DuckDB 并加载陆川九龙山庄改造提升项目专项湖仓底账
    conn = duckdb.connect()
    with open('/home/l/个人资料仓库/data/views_jiulong_bom_mart.sql') as f:
        conn.execute(f.read())
    with open('/home/l/个人资料仓库/data/views_jiulong_direct_excel.sql') as f:
        conn.execute(f.read())

    # 提取核心历史真值事实
    contract_master_df = conn.execute("SELECT * FROM v_jl_contract_master").df()
    public_breakdown_df = conn.execute("SELECT * FROM v_jl_public_area_breakdown").df()
    payment_terms_df = conn.execute("SELECT * FROM v_jl_payment_milestones").df()
    zone_breakdown_df = conn.execute("SELECT * FROM v_jl_zone_breakdown").df()
    bom_detail_df = conn.execute("SELECT * FROM v_jiulong_bom_detail").df()

    # 核心标尺常量
    initial_quote = 553.455  # 0929 原始清单商务报价合价 (万元)
    discount_val = 3.455     # 签约下浮让利优惠额 (万元，34,550元)
    contract_amt = 550.00    # 最终固定总价包干签约额 (万元)
    public_amt = 236.22      # 公区造价 (万元)
    guest_amt = 317.24       # 客房及汤院造价 (万元)
    total_qty = 2046         # 全案实物件数 (件)
    total_items = 329        # 全案物料清单行数 (行)

    # 估算珠三角工厂源头直采成本基准 (约占报价 53.5%，即约 294.5 万元，毛利空间约 255.5 万元)
    est_direct_cost = 294.50
    direct_cost = 294.50

    return (
        bom_detail_df,
        conn,
        contract_amt,
        contract_master_df,
        direct_cost,
        discount_val,
        est_direct_cost,
        guest_amt,
        initial_quote,
        payment_terms_df,
        public_amt,
        public_breakdown_df,
        total_items,
        total_qty,
        zone_breakdown_df,
    )


@app.cell
def __(bom_detail_df, mo):
    # UIElement 独立单元格：标段与房型空间联动筛选器
    _zones = ["全部空间标段", "公区活动及定制家具", "主楼客房及特色汤院"]
    zone_selector = mo.ui.dropdown(
        options=_zones,
        value="全部空间标段",
        label="🏛️ 空间标段筛选"
    )

    # 高管调参交互模式单选
    input_mode = mo.ui.radio(
        options=["滑轮拖动模式", "具体数值输入模式"],
        value="具体数值输入模式",
        label="🎛️ 调参驱动源"
    )

    # 1. 商务签约优惠让利率调优 (天蓝主题)
    slider_discount = mo.ui.slider(
        start=0.0,
        stop=5.0,
        step=0.1,
        value=0.62,
        label="滑轮调节下浮率 (%)"
    )
    number_discount = mo.ui.number(
        start=0.0,
        stop=5.0,
        step=0.01,
        value=0.62,
        label="输入精确下浮率 (%)"
    )

    # 2. 供应链采购与工艺降本率调优 (薄荷绿主题)
    slider_cost_save = mo.ui.slider(
        start=0.0,
        stop=25.0,
        step=0.5,
        value=12.0,
        label="滑轮调节工艺降本 (%)"
    )
    number_cost_save = mo.ui.number(
        start=0.0,
        stop=25.0,
        step=0.5,
        value=12.0,
        label="输入精确降本率 (%)"
    )

    # 3. 现场货到进度款回款控制率调优 (金黄主题)
    slider_arrival_rate = mo.ui.slider(
        start=50.0,
        stop=95.0,
        step=1.0,
        value=80.0,
        label="滑轮调节货到累计回款 (%)"
    )
    number_arrival_rate = mo.ui.number(
        start=50.0,
        stop=95.0,
        step=1.0,
        value=80.0,
        label="输入货到回款率 (%)"
    )

    # 表格选择器独立初始化
    table_bom = mo.ui.table(
        bom_detail_df[['标段', '房型', '物料编码', '空间落位', '物料名称', '规格尺寸', '合计数量', '单位', '综合单价_元', '直接合价_元']],
        selection="single",
        pagination=True,
        page_size=10,
        label="九龙山庄 2,046 件定制家具与客房资产穿透台账（点击某行穿透工艺与材质）"
    )

    return (
        input_mode,
        number_arrival_rate,
        number_cost_save,
        number_discount,
        slider_arrival_rate,
        slider_cost_save,
        slider_discount,
        table_bom,
        zone_selector,
    )


@app.cell
def __(
    input_mode,
    mo,
    number_arrival_rate,
    number_cost_save,
    number_discount,
    slider_arrival_rate,
    slider_cost_save,
    slider_discount,
    zone_selector,
):
    # 动态参数绑定逻辑 (滑轮 vs 数值双模)
    _is_num_mode = (input_mode.value == "具体数值输入模式")

    if _is_num_mode:
        sim_discount = float(number_discount.value) if number_discount.value is not None else 0.62
        sim_cost_save = float(number_cost_save.value) if number_cost_save.value is not None else 12.0
        sim_arrival_rate = float(number_arrival_rate.value) if number_arrival_rate.value is not None else 80.0
    else:
        sim_discount = float(slider_discount.value) if slider_discount.value is not None else 0.62
        sim_cost_save = float(slider_cost_save.value) if slider_cost_save.value is not None else 12.0
        sim_arrival_rate = float(slider_arrival_rate.value) if slider_arrival_rate.value is not None else 80.0

    # 组装高管全局侧边栏 (三色认知视觉锚定，彻底移除 CSV 下载)
    sidebar = mo.sidebar([
        mo.md("## 🏛️ 高管全局操盘控制台"),
        mo.md("*陆川九龙山庄改造提升项目 · 固定总价与资金节点实时推演*"),
        mo.md("---"),
        input_mode,
        mo.md("---"),
        mo.Html("<div style='background:#f0f9ff; border:1px solid #bae6fd; border-left:4px solid #0284c7; padding:8px 10px; border-radius:4px; font-weight:600; color:#0369a1;'>📊 1. 商务签约下浮让利率调优</div>"),
        slider_discount,
        number_discount,
        mo.md("---"),
        mo.Html("<div style='background:#f0fdf4; border:1px solid #bbf7d0; border-left:4px solid #16a34a; padding:8px 10px; border-radius:4px; font-weight:600; color:#15803d;'>🏭 2. 供应链采购与工艺降本调优</div>"),
        slider_cost_save,
        number_cost_save,
        mo.md("---"),
        mo.Html("<div style='background:#fefce8; border:1px solid #fef08a; border-left:4px solid #ca8a04; padding:8px 10px; border-radius:4px; font-weight:600; color:#854d0e;'>💰 3. 现场货到累计回款控制率调优</div>"),
        slider_arrival_rate,
        number_arrival_rate,
        mo.md("---"),
        mo.md("🔍 **空间资产钻取**"),
        zone_selector,
        mo.md("---"),
        mo.md("<div style='font-size:11px; color:#64748b; line-height:1.5;'>梁清波 商业专案库 · Marimo Reactive Engine<br>项目代号：GY-2021-YW-050</div>")
    ])

    return (
        sidebar,
        sim_arrival_rate,
        sim_cost_save,
        sim_discount,
    )


@app.cell
def __(sidebar):
    # 渲染侧边栏
    sidebar
    return


@app.cell
def __(
    est_direct_cost,
    initial_quote,
    input_mode,
    mo,
    sim_arrival_rate,
    sim_cost_save,
    sim_discount,
):
    # 动态推演核心算法模型
    # 1. 实际签约包干总价推演
    sim_contract_amt = initial_quote * (1.0 - sim_discount / 100.0)
    sim_discount_amt = initial_quote - sim_contract_amt

    # 2. 供应链源头采购与工艺平替降本后直接成本推演
    sim_direct_cost = est_direct_cost * (1.0 - sim_cost_save / 100.0)
    sim_margin_amt = sim_contract_amt - sim_direct_cost
    sim_margin_rate = (sim_margin_amt / sim_contract_amt) * 100.0 if sim_contract_amt > 0 else 0.0

    # 3. 现场货到阶段回款与资金覆盖倍数推演
    sim_arrival_cash = sim_contract_amt * (sim_arrival_rate / 100.0)
    sim_coverage_ratio = (sim_arrival_cash / sim_direct_cost) * 100.0 if sim_direct_cost > 0 else 0.0

    # 4. 单方与单间指标 (30,000 ㎡ / 188 间客房)
    sim_cost_per_sqm = (sim_contract_amt * 10000.0) / 30000.0
    sim_guest_cost_per_room = (317.24 * 10000.0) / 188.0

    _mode_text = f"💡 <strong>{input_mode.value}生效</strong> · 实时调优参数同步："
    _kpi_discount_tag = f"<span style='background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px; font-weight:600;'>📊 下浮 {sim_discount:.2f}%</span>"
    _kpi_cost_tag = f"<span style='background:#dcfce7; color:#15803d; padding:2px 6px; border-radius:4px; font-weight:600;'>🏭 工艺降本 {sim_cost_save:.1f}%</span>"
    _kpi_cash_tag = f"<span style='background:#fef9c3; color:#854d0e; padding:2px 6px; border-radius:4px; font-weight:600;'>💰 货到回款率 {sim_arrival_rate:.1f}%</span>"

    kpi_cards_html = mo.Html(f"""
    <div style="margin: 14px 0 22px 0;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; font-size: 13px; color: #475569; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 14px;">
        <div>{_mode_text} &nbsp;{_kpi_discount_tag} &nbsp;{_kpi_cost_tag} &nbsp;{_kpi_cash_tag}</div>
        <div style="font-size: 11px; color: #94a3b8;">与左侧控制台色彩 100% 视觉锚定</div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #0284c7; border-radius: 8px; padding: 16px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <div style="font-size: 12px; color: #64748b; font-weight: 500;">推演合同签约总额</div>
          <div style="font-size: 26px; font-weight: 700; color: #0f172a; margin: 4px 0; font-family: 'Latin Modern Roman', serif;">
            {sim_contract_amt:.2f} <span style="font-size: 14px; font-weight: normal; color: #64748b;">万元</span>
          </div>
          <div style="font-size: 11px; color: #0284c7;">
            {_kpi_discount_tag} &nbsp;<span style="color:#64748b;">基准 553.46万 (下浮{sim_discount_amt:.2f}万)</span>
          </div>
        </div>

        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #16a34a; border-radius: 8px; padding: 16px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <div style="font-size: 12px; color: #64748b; font-weight: 500;">推演综合毛利率 (空间)</div>
          <div style="font-size: 26px; font-weight: 700; color: #16a34a; margin: 4px 0; font-family: 'Latin Modern Roman', serif;">
            {sim_margin_rate:.1f}% <span style="font-size: 14px; font-weight: normal; color: #64748b;">({sim_margin_amt:.2f}万)</span>
          </div>
          <div style="font-size: 11px; color: #15803d;">
            {_kpi_cost_tag} 护盘 &nbsp;<span style="color:#64748b;">采购成本 {sim_direct_cost:.2f}万</span>
          </div>
        </div>

        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #ca8a04; border-radius: 8px; padding: 16px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <div style="font-size: 12px; color: #64748b; font-weight: 500;">货到现场资金覆盖倍数</div>
          <div style="font-size: 26px; font-weight: 700; color: #0f172a; margin: 4px 0; font-family: 'Latin Modern Roman', serif;">
            {sim_coverage_ratio:.1f}% <span style="font-size: 13px; font-weight: normal; color: #64748b;">(已收{sim_arrival_cash:.2f}万)</span>
          </div>
          <div style="font-size: 11px; color: #ca8a04;">
            <span style="background:#fef9c3; padding:1px 5px; border-radius:3px;">💰 货到初验累计回款 80%</span>
          </div>
        </div>

        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #0d9488; border-radius: 8px; padding: 16px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
          <div style="font-size: 12px; color: #64748b; font-weight: 500;">客房均摊造价定额</div>
          <div style="font-size: 26px; font-weight: 700; color: #0d9488; margin: 4px 0; font-family: 'Latin Modern Roman', serif;">
            {sim_guest_cost_per_room:,.0f} <span style="font-size: 14px; font-weight: normal; color: #64748b;">元/间</span>
          </div>
          <div style="font-size: 11px; color: #0f766e;">
            <span style="background:#ccfbf1; padding:1px 5px; border-radius:3px;">全案 30,000 ㎡ · 2,046 件实物</span>
          </div>
        </div>
      </div>
    </div>
    """)

    return (
        kpi_cards_html,
        sim_arrival_cash,
        sim_contract_amt,
        sim_coverage_ratio,
        sim_direct_cost,
        sim_discount_amt,
        sim_guest_cost_per_room,
        sim_margin_amt,
        sim_margin_rate,
    )


@app.cell
def __(base64, io, plt, public_breakdown_df, zone_breakdown_df):
    # 动静解耦核心：在独立静态单元格预渲染 4 张原生矢量 SVG 高清学术图表

    # ---------------------------------------------------------
    # 图 1: 公区五大核心空间 vs 188间客房与半山汤院造价架构双轨图
    # ---------------------------------------------------------
    _fig1, _ax1 = plt.subplots(figsize=(9.2, 4.2), dpi=200)
    _spaces = ['客房与特色汤院', '中餐豪华包房', '大堂/西餐厅', '温泉水疗中心', '贵宾首长厅', '行政高区酒廊']
    _amts = [317.24, 83.57, 65.73, 52.19, 24.69, 10.04]
    _colors = ['#1e3a8a', '#0284c7', '#0369a1', '#0ea5e9', '#38bdf8', '#7dd3fc']
    
    _bars1 = _ax1.barh(_spaces[::-1], _amts[::-1], color=_colors[::-1], height=0.55, edgecolor='none')
    _ax1.set_title('陆川九龙山庄 · 全案空间标段造价架构分布 (单位: 万元)', fontsize=12, fontweight='bold', pad=14)
    _ax1.set_xlabel('造价金额 (万元)', fontsize=10)
    _ax1.grid(axis='x', linestyle='--', alpha=0.3)
    _ax1.spines['top'].set_visible(False)
    _ax1.spines['right'].set_visible(False)
    
    for _b in _bars1:
        _w = _b.get_width()
        _ax1.text(_w + 4.0, _b.get_y() + _b.get_height()/2.0, f'{_w:.2f} 万元 ({(_w/553.455*100):.1f}%)',
                  va='center', ha='left', fontsize=9.5, fontweight='bold', color='#1e293b')
    _ax1.set_xlim(0, 370)

    _buf1 = io.BytesIO()
    _fig1.savefig(_buf1, format='svg', bbox_inches='tight')
    plt.close(_fig1)
    _buf1.seek(0)
    chart1_b64 = base64.b64encode(_buf1.getvalue()).decode('utf-8')

    # ---------------------------------------------------------
    # 图 2: 公区五大空间商务报价 vs 地方造价站参考价严密抗辩对比
    # ---------------------------------------------------------
    _fig2, _ax2 = plt.subplots(figsize=(9.2, 4.2), dpi=200)
    _bench_spaces = ['中餐豪华包房', '大堂吧与西餐厅', '温泉中心水疗', '贵宾首长厅', '行政酒廊']
    _my_quote = [83.57, 65.73, 52.19, 24.69, 10.04]
    _station_quote = [74.71, 72.87, 49.50, 22.10, 9.44] # 造价站对比事实
    
    _x = np.arange(len(_bench_spaces))
    _w = 0.35
    _b_my = _ax2.bar(_x - _w/2, _my_quote, _w, label='0929 商务报价 (我方)', color='#0284c7', edgecolor='none')
    _b_st = _ax2.bar(_x + _w/2, _station_quote, _w, label='地方造价站市场参考价', color='#94a3b8', edgecolor='none')
    
    _ax2.set_title('九龙山庄公区 · 商务报价 vs 造价站市场参考价抗辩比对 (万元)', fontsize=12, fontweight='bold', pad=14)
    _ax2.set_xticks(_x)
    _ax2.set_xticklabels(_bench_spaces, fontsize=10)
    _ax2.set_ylabel('金额 (万元)', fontsize=10)
    _ax2.legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=9)
    _ax2.grid(axis='y', linestyle='--', alpha=0.3)
    _ax2.spines['top'].set_visible(False)
    _ax2.spines['right'].set_visible(False)
    
    for _b in _b_my:
        _h = _b.get_height()
        _ax2.text(_b.get_x() + _b.get_width()/2.0, _h + 1.2, f'{_h:.1f}', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0284c7')
    for _b in _b_st:
        _h = _b.get_height()
        _ax2.text(_b.get_x() + _b.get_width()/2.0, _h + 1.2, f'{_h:.1f}', ha='center', va='bottom', fontsize=8.5, color='#64748b')
    _ax2.set_ylim(0, 98)

    _buf2 = io.BytesIO()
    _fig2.savefig(_buf2, format='svg', bbox_inches='tight')
    plt.close(_fig2)
    _buf2.seek(0)
    chart2_b64 = base64.b64encode(_buf2.getvalue()).decode('utf-8')

    # ---------------------------------------------------------
    # 图 3: 真实合同 30/50/15/5 资金付款节点与到场 80% 现金流护城河
    # ---------------------------------------------------------
    _fig3, _ax3 = plt.subplots(figsize=(9.2, 4.0), dpi=200)
    _nodes = ['预付款 (30%)', '货物到场初验 (累计80%)', '出厂采购成本 (安全线)', '竣工安装摆场 (累计95%)', '质保期满 (100%)']
    _cum_cash = [165.00, 440.00, 294.50, 522.50, 550.00]
    _node_colors = ['#38bdf8', '#0284c7', '#dc2626', '#16a34a', '#0f766e']
    
    _bars3 = _ax3.bar(_nodes, _cum_cash, color=_node_colors, width=0.52, edgecolor='none')
    _ax3.axhline(294.50, color='#dc2626', linestyle='--', linewidth=1.5, label='出厂直接成本安全线 (294.50万元)')
    _ax3.set_title('九龙山庄 · 30/50/15/5 阶段付款节点与到场 80% 现金流护城河 (万元)', fontsize=12, fontweight='bold', pad=14)
    _ax3.set_ylabel('累计现金流 (万元)', fontsize=10)
    _ax3.grid(axis='y', linestyle='--', alpha=0.3)
    _ax3.spines['top'].set_visible(False)
    _ax3.spines['right'].set_visible(False)
    _ax3.legend(loc='upper left', frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=9)
    
    for _b in _bars3:
        _h = _b.get_height()
        _ax3.text(_b.get_x() + _b.get_width()/2.0, _h + 8.0, f'{_h:.2f}万', ha='center', va='bottom', fontsize=9, fontweight='bold')
    _ax3.set_ylim(0, 620)

    _buf3 = io.BytesIO()
    _fig3.savefig(_buf3, format='svg', bbox_inches='tight')
    plt.close(_fig3)
    _buf3.seek(0)
    chart3_b64 = base64.b64encode(_buf3.getvalue()).decode('utf-8')

    # ---------------------------------------------------------
    # 图 4: 2,046 件实物资产在公区五大分区与 188 间客房的件数分布
    # ---------------------------------------------------------
    _fig4, _ax4 = plt.subplots(figsize=(9.2, 4.4), dpi=200)
    _sec_names = ['主楼188间客房及汤院', '中餐豪华包房', '大堂与大堂吧西餐厅', '温泉水疗中心', '贵宾接待首长厅', '行政高区酒廊']
    _sec_qtys = [1348, 224, 216, 135, 89, 34]
    _sec_colors = ['#0f766e', '#0d9488', '#14b8a6', '#2dd4bf', '#5eead4', '#99f6e4']

    _bars4 = _ax4.barh(_sec_names[::-1], _sec_qtys[::-1], color=_sec_colors[::-1], height=0.55, edgecolor='none')
    _ax4.set_title('九龙山庄 · 全案 2,046 件实物资产分布 (主楼客房 vs 公区五大空间)', fontsize=12, fontweight='bold', pad=14)
    _ax4.set_xlabel('配置数量 (件/套)', fontsize=10)
    _ax4.grid(axis='x', linestyle='--', alpha=0.3)
    _ax4.spines['top'].set_visible(False)
    _ax4.spines['right'].set_visible(False)

    for _b in _bars4:
        _w = _b.get_width()
        _ax4.text(_w + 15.0, _b.get_y() + _b.get_height()/2.0, f'{_w:.0f} 件 ({(_w/2046*100):.1f}%)',
                  va='center', ha='left', fontsize=9.5, fontweight='bold', color='#134e4a')
    _ax4.set_xlim(0, 1600)

    _buf4 = io.BytesIO()
    _fig4.savefig(_buf4, format='svg', bbox_inches='tight')
    plt.close(_fig4)
    _buf4.seek(0)
    chart4_b64 = base64.b64encode(_buf4.getvalue()).decode('utf-8')

    return (
        chart1_b64,
        chart2_b64,
        chart3_b64,
        chart4_b64,
    )


@app.cell
def __(
    chart1_b64,
    chart2_b64,
    chart3_b64,
    chart4_b64,
    mo,
):
    # Tab 1: 全景深度商业研报总装 (轻量引用预渲染 SVG，杜绝白屏)
    tab1_content = mo.vstack([
        mo.md("### § 0 核心商业基本盘与合同指标全景"),
        mo.Html("""
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px;">
          <thead>
            <tr style="background: #f8fafc; border-bottom: 2px solid #cbd5e1; text-align: left;">
              <th style="padding: 10px 14px;">商业业务维度</th>
              <th style="padding: 10px 14px;">量化指标名称</th>
              <th style="padding: 10px 14px; text-align: right;">审计核定真值</th>
              <th style="padding: 10px 14px; text-align: center;">操盘控制属性</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 9px 14px; font-weight: 600;">项目属性与发包</td>
              <td style="padding: 9px 14px;">广西陆川温泉九龙山庄有限责任公司 (施工I标)</td>
              <td style="padding: 9px 14px; text-align: right; font-weight: 700; color: #0284c7;">GY-2021-YW-050</td>
              <td style="padding: 9px 14px; text-align: center;"><span style="background:#e0f2fe; color:#0369a1; padding:2px 8px; border-radius:4px;">五星温泉度假村</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 9px 14px; font-weight: 600;">原始清单商务合价</td>
              <td style="padding: 9px 14px;">0929 商务报价清单合价 (公区 236.22万 + 客房 317.24万)</td>
              <td style="padding: 9px 14px; text-align: right; font-weight: 700; color: #0f172a;">553.46 万元</td>
              <td style="padding: 9px 14px; text-align: center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px;">报价原始基准</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 9px 14px; font-weight: 600;">商务下浮优惠</td>
              <td style="padding: 9px 14px;">双方友好商务磋商让利下浮款</td>
              <td style="padding: 9px 14px; text-align: right; font-weight: 700; color: #dc2626;">34,550.00 元 (0.62%)</td>
              <td style="padding: 9px 14px; text-align: center;"><span style="background:#fee2e2; color:#991b1b; padding:2px 8px; border-radius:4px;">促成签约锁定</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 9px 14px; font-weight: 600;">最终合同签约价</td>
              <td style="padding: 9px 14px;">固定总价包干签约总额 (零核减、不调价)</td>
              <td style="padding: 9px 14px; text-align: right; font-weight: 700; color: #16a34a;">550.00 万元</td>
              <td style="padding: 9px 14px; text-align: center;"><span style="background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:4px; font-weight:700;">固定总价包干</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 9px 14px; font-weight: 600;">资金回款护城河</td>
              <td style="padding: 9px 14px;">预付款 30% (165万) + 到场初验 50% (275万)</td>
              <td style="padding: 9px 14px; text-align: right; font-weight: 700; color: #0284c7;">累计 80% (440.00 万元)</td>
              <td style="padding: 9px 14px; text-align: center;"><span style="background:#fef9c3; color:#854d0e; padding:2px 8px; border-radius:4px;">超额覆盖成本</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 9px 14px; font-weight: 600;">抢工交付周期</td>
              <td style="padding: 9px 14px;">多工种穿插作业驻场督导交付天数</td>
              <td style="padding: 9px 14px; text-align: right; font-weight: 700; color: #0f172a;">28 个日历天</td>
              <td style="padding: 9px 14px; text-align: center;"><span style="background:#ccfbf1; color:#0f766e; padding:2px 8px; border-radius:4px;">温泉季极限抢工</span></td>
            </tr>
            <tr>
              <td style="padding: 9px 14px; font-weight: 600;">全案实物交付</td>
              <td style="padding: 9px 14px;">公区 698 件 + 188 间客房及半山汤院 1,348 件</td>
              <td style="padding: 9px 14px; text-align: right; font-weight: 700; color: #0f172a;">2,046 件 / 329 款物料</td>
              <td style="padding: 9px 14px; text-align: center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px;">高定实木防潮</span></td>
            </tr>
          </tbody>
        </table>
        """),

        mo.md("### § 1 公区五星级会所 vs 188 间客房汤院双轨构面"),
        mo.md("""
        - **双轨标段大盘划分**：全案划分为「一、公区活动及定制家具（236.22 万元，占比 42.68%）」与「二、主楼客房及特色半山汤院（317.24 万元，占比 57.32%）」。公区涵盖通高大堂、中餐豪华宴会包房、温泉中心水疗、首长接待厅及行政酒廊；
        - **商务下浮促成签约**：原 0929 报价清单合价 553.46 万元，梁清波团队主动给予 34,550 元商务让利下浮，以 550.00 万元整固定总价包干正式签约，迅速锁定项目大盘。
        """),
        mo.Html(f'<div class="chart-svg-box"><img src="data:image/svg+xml;base64,{chart1_b64}" alt="全案空间标段造价架构分布图" /></div>'),

        mo.md("### § 2 商务报价 vs 地方造价站市场参考价严密抗辩"),
        mo.md("""
        - **造价站权威对账事实**：项目清单曾与当地造价站市场参考价逐项对账。公区 128 项 / 698 件物品造价站参考合计 228.62 万元，我方商务报价 236.22 万元，仅高出 3.21%（7.59 万元），处于极为合理的溢价区间；
        - **结构性对冲抗辩策略**：高出部分集中于中餐包房（+8.86 万元，因配置了 10~20 人大包房高定电动实木圆桌与定制配餐柜）与贵宾首长厅（+2.59 万元），而西餐厅则主动优化让利（低于参考价 7.14 万元），以高定工艺价值成功抗辩造价审减！
        """),
        mo.Html(f'<div class="chart-svg-box"><img src="data:image/svg+xml;base64,{chart2_b64}" alt="公区商务报价 vs 造价站参考价对比" /></div>'),

        mo.md("### § 3 30/50/15/5 资金付款节奏与到场 80% 现金流护城河"),
        mo.md("""
        - **30% 预付款（165.00 万元）**：合同生效 5 个工作日内到账，直接锁定珠三角实木木皮、白蜡木基材与五金开料；
        - **50% 到场进度款（275.00 万元，累计 80% / 440.00 万元）**：核心法务节点。约定货物运抵施工现场初验合格后支付，**累计收款 440.00 万元，超额覆盖珠三角采购与长途干线物流直接成本（294.50 万元）的 149.4%**！
        - **15% 安装竣工款（82.50 万元，累计 95% / 522.50 万元）**：全部摆场完毕递交验收报告后支付；
        - **5% 质保金尾款（27.50 万元）**：工程竣工验收满 1 年后无息返还，全案坏账为零。
        """),
        mo.Html(f'<div class="chart-svg-box"><img src="data:image/svg+xml;base64,{chart3_b64}" alt="资金付款节点与到场80%现金流护城河" /></div>'),

        mo.md("### § 4 28 天极限穿插抢工与 2,046 件实物资产分布"),
        mo.md("""
        - **28 天极限交付奇迹**：面对老建筑改造存在的墙体倾斜公差、温泉高热高湿腐蚀环境，梁清波团队驻场督导，攻克单台垂直货梯运力瓶颈，组织泥水、油漆、软装多工种交叉立体作业，28 天内完成全案 2,046 件实物摆场通电与联合验收；
        - **原子级资产清单**：主楼 188 间客房及半山汤院配置 1,348 件家具（占比 65.9%），中餐包房 224 件，大堂与西餐厅 216 件，温泉水疗 135 件，首长厅 89 件，行政酒廊 34 件。
        """),
        mo.Html(f'<div class="chart-svg-box"><img src="data:image/svg+xml;base64,{chart4_b64}" alt="全案2046件实物资产分布" /></div>'),
    ])

    return tab1_content,


@app.cell
def __(base64, est_direct_cost, initial_quote, io, mo, pd, plt):
    # Tab 2: 商务下浮让利 vs 供应链降本推演矩阵 (静态预渲染高清热力图)
    _disc_range = [0.0, 0.62, 1.5, 2.5, 4.0]
    _cost_save_range = [5.0, 8.0, 12.0, 16.0, 20.0]

    _matrix_rates = []
    _matrix_amts = []
    _matrix_data = []

    for _d in _disc_range:
        _c_amt = initial_quote * (1.0 - _d / 100.0)
        _row_rates = []
        _row_amts = []
        _row_dict = {"商务下浮率": f"{_d:.2f}%"}
        for _cs in _cost_save_range:
            _cost = est_direct_cost * (1.0 - _cs / 100.0)
            _margin = _c_amt - _cost
            _rate = (_margin / _c_amt) * 100.0 if _c_amt > 0 else 0.0
            _row_rates.append(_rate)
            _row_amts.append(_margin)
            _row_dict[f"降本 {_cs:.1f}%"] = f"{_rate:.1f}% ({_margin:.1f}万)"
        _matrix_rates.append(_row_rates)
        _matrix_amts.append(_row_amts)
        _matrix_data.append(_row_dict)

    _fig_sens, _ax_sens = plt.subplots(figsize=(8.8, 4.4), dpi=200)
    _cax = _ax_sens.imshow(_matrix_rates, cmap='YlGnBu', aspect='auto')
    _ax_sens.set_xticks(range(len(_cost_save_range)))
    _ax_sens.set_yticks(range(len(_disc_range)))
    _ax_sens.set_xticklabels([f'降本 {c:.1f}%' for c in _cost_save_range], fontsize=9.5)
    _ax_sens.set_yticklabels([f'下浮 {d:.2f}%' for d in _disc_range], fontsize=9.5)
    _ax_sens.set_title('九龙山庄 · 商务下浮让利 vs 供应链采购降本推演矩阵 (推演综合毛利率)', fontsize=11.5, fontweight='bold', pad=12)

    for _i in range(len(_disc_range)):
        for _j in range(len(_cost_save_range)):
            _val = _matrix_rates[_i][_j]
            _color = 'white' if _val > 48.0 else '#0f172a'
            _label = f'{_val:.1f}%'
            if _disc_range[_i] == 0.62 and _cost_save_range[_j] == 12.0:
                _label = f'★实际: {_val:.1f}%'
                _color = '#dc2626'
            _ax_sens.text(_j, _i, _label, ha='center', va='center', color=_color, fontsize=9.5, fontweight='bold')

    _cbar = _fig_sens.colorbar(_cax, ax=_ax_sens, fraction=0.046, pad=0.04)
    _cbar.set_label('推演经营毛利率 (%)', fontsize=9.5)
    _fig_sens.tight_layout()

    _buf_sens = io.BytesIO()
    _fig_sens.savefig(_buf_sens, format='svg', bbox_inches='tight')
    plt.close(_fig_sens)
    _buf_sens.seek(0)
    sens_heatmap_b64 = base64.b64encode(_buf_sens.getvalue()).decode('utf-8')

    table_sens = mo.ui.table(
        pd.DataFrame(_matrix_data),
        selection=None,
        label="场景推演量化对照表（毛利率与毛利额）"
    )

    tab2_content = mo.vstack([
        mo.md("### 🎛️ 商务签约让利与供应链工艺降本双变量推演矩阵"),
        mo.md("""
        通过在不同商务让利下浮（0% 至 4%）与珠三角工厂源头集采降本（5% 至 20%）之间的交叉推演，清晰验证：
        **梁清波团队通过严控 34,550 元微幅让利（仅 0.62%）锁定 550.00 万元固定总价包干合同，配合 12% 供应链采购工艺降本，将全案综合毛利稳固在 46.5%~50.0% 高位！**
        """),
        mo.Html(f'<div class="chart-svg-box"><img src="data:image/svg+xml;base64,{sens_heatmap_b64}" alt="商务让利 vs 供应链降本推演矩阵热力图" /></div>'),
        mo.md("#### 📊 场景推演量化对照表（毛利率与毛利额）"),
        table_sens
    ])

    return (
        sens_heatmap_b64,
        tab2_content,
        table_sens,
    )


@app.cell
def __(bom_detail_df, table_bom, zone_selector):
    # UIElement 独立单元格：筛选与点击穿透逻辑
    _filter_val = zone_selector.value
    if _filter_val == "公区活动及定制家具":
        filtered_bom_df = bom_detail_df[bom_detail_df['标段'] == '公区']
    elif _filter_val == "主楼客房及特色汤院":
        filtered_bom_df = bom_detail_df[bom_detail_df['标段'] == '客房']
    else:
        filtered_bom_df = bom_detail_df

    # 捕获表格单选行，实现原子级物料穿透
    _selected_row = table_bom.value
    if _selected_row is not None and not _selected_row.empty:
        target_row = _selected_row.iloc[0]
        status_hint = "🔎 当前选中穿透物料"
    elif filtered_bom_df is not None and not filtered_bom_df.empty:
        target_row = filtered_bom_df.iloc[0]
        status_hint = "💡 典型物料穿透示例（可点击上方表格任意一行即时切换）"
    else:
        target_row = None
        status_hint = ""

    return (
        filtered_bom_df,
        status_hint,
        target_row,
    )


@app.cell
def __(
    filtered_bom_df,
    mo,
    status_hint,
    table_bom,
    target_row,
    zone_selector,
):
    # 渲染 Tab 3 穿透卡片与明细表格
    if target_row is not None:
        _detail_card = f"""
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; border-radius: 6px; padding: 14px 18px; margin-top: 12px;">
          <h4 style="margin: 0 0 8px 0; color: #14532d; font-size: 14px;">{status_hint}：{target_row['物料名称']}（物料编码：{target_row['物料编码']}）</h4>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 12.5px; color: #374151;">
            <div><strong>空间标段：</strong>{target_row['标段']} - {target_row['房型']}</div>
            <div><strong>详细空间落位：</strong>{target_row['空间落位']}</div>
            <div><strong>配置数量：</strong><span style="color:#15803d; font-weight:700;">{target_row['合计数量']} {target_row['单位']}</span></div>
            <div><strong>综合单价/合价：</strong><span class="mono-num">{target_row['综合单价_元']:,.0f} 元 / {target_row['直接合价_元']:,.0f} 元</span></div>
            <div style="grid-column: span 4;"><strong>规格尺寸参数：</strong><span class="mono-num">{target_row['规格尺寸']}</span></div>
            <div style="grid-column: span 4; margin-top: 4px; padding: 6px 10px; background: #ffffff; border-radius: 4px; border: 1px solid #dcfce7; line-height: 1.6;">
              <strong>详细材质与工艺选型说明：</strong><br>{target_row['材质工艺'].replace(chr(10), '<br>')}
            </div>
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
        mo.md("### 🔍 2,046 件实物资产与 329 款物料原子级穿透台"),
        mo.md(f"当前筛选范围：**{zone_selector.value}**（直连 DuckDB 湖仓 `lake_jiulongshan_bom.parquet`，支持点击表格行穿透材质与选型）："),
        table_bom,
        mo.Html(_detail_card)
    ])

    return tab3_content,


@app.cell
def __(mo):
    # Tab 4: 招投标与法定合同档案索引手风琴
    tab4_content = mo.vstack([
        mo.md("### ⚖️ 陆川九龙山庄法定合同与审计卷宗原件索引"),
        mo.md("全案事实严格遵照《合同法》与五星级温泉生态度假村改造提升工程审计标准归档："),
        mo.accordion({
            "📑 1. 固定总价包干合同原件 (编号: GY-2021-YW-050)": mo.md("""
            - **发包单位**：广西陆川温泉九龙山庄有限责任公司（陆川县乐源温泉开发）；
            - **承包内容**：陆川九龙山庄改造提升项目软装（施工I标）定制类家具采购及安装工程；
            - **合同金额**：**人民币 5,500,000.00 元整（固定总价包干）**；
            - **核心条款**：除发包方提出书面设计变更或工程范围调整外，该总价包干不因市场物价波动、人工费上涨而作任何调整。
            """),
            "📊 2. 0929 商务报价清单与 34,550 元让利核对底账": mo.md("""
            - **原始商务合价**：5,534,550.00 元（公区 2,362,174.00 元 + 客房 3,172,376.00 元）；
            - **商务让利确认书**：梁清波团队签字确认给予 34,550.00 元商务优惠（下浮 0.62%），促成签约 550.00 万元总价包干；
            - **双方逐页盖章**：包含 329 行清单之物料编码、规格、材质、综合单价与直接合价。
            """),
            "🏛️ 3. 地方造价站市场参考价逐项对账抗辩表": mo.md("""
            - **公区对比底账**：公区 128 项造价站参考价合计 228.62 万元，我方报价 236.22 万元（高出 3.21% / 7.59 万元）；
            - **抗辩结论**：经逐项核对，高出部分在中餐豪华宴会包房电动实木圆桌（高出 8.86 万元）与贵宾首长厅（高出 2.59 万元），西餐厅低于参考价 7.14 万元，成功抗辩造价审减！
            - **客房对比底账**：客房 201 项造价站参考 300.39 万元，我方 317.24 万元（含深山现场长途运输与温泉防潮防腐定制溢价）。
            """),
            "💰 4. 进度款申报表、开票申请表与银行结算回执": mo.md("""
            - **第一笔 (2021-10)**：预付款 30%（165.00 万元），进度款申报表与银行回单载明到账；
            - **第二笔 (2021-11-23)**：公区第一批发货前进度款，申报表含税产值 174.13 万元，请款 50%（87.06 万元），累计到账 252.06 万元；
            - **第三笔 (2021-12-14)**：客房与温泉中心发货前请款，申报产值 359.89 万元，请款 50%（179.95 万元），货到阶段累计实现 80% 超额资金回笼！
            """),
            "⏱️ 5. 28 天极限抢工排产表与现场联合验收纪要": mo.md("""
            - **现场难点**：老旧建筑墙体倾斜公差、温泉高热湿气防潮处理、垂直货梯单台运力受限；
            - **施工组织**：梁清波亲临一线，现场放线交底，多工种立体穿插，28 天完成全部 2,046 件实物安装摆场；
            - **联合验收**：业主投资方、设计院、监理单位三方联合签字验收合格，温泉季如期盛大迎宾开业！
            """)
        })
    ])

    return tab4_content,


@app.cell
def __(kpi_cards_html, mo, tab1_content, tab2_content, tab3_content, tab4_content):
    # LaTeX 学术排版全局样式
    latex_style = mo.Html("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Latin+Modern+Roman:ital,wght@0,400;0,700;1,400&family=Noto+Serif+SC:wght@400;600;700&display=swap');

      body, .marimo-app, h1, h2, h3, h4, h5, h6, p, li, blockquote, div {
        font-family: "Latin Modern Roman", "Computer Modern Serif", "Noto Serif SC", "Source Han Serif SC", "SimSun", serif !important;
      }

      h1, h2, h3 {
        color: #0f172a !important;
        letter-spacing: -0.01em;
      }

      blockquote {
        border-left: 3px solid #0284c7 !important;
        background: #f8fafc !important;
        padding: 10px 16px !important;
        border-radius: 0 6px 6px 0 !important;
        color: #334155 !important;
        font-style: italic;
      }

      table {
        font-family: "Latin Modern Roman", "Noto Serif SC", serif !important;
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
        "🎛️ 商务下浮与降本推演矩阵": tab2_content,
        "🔍 2,046 件实物资产穿透": tab3_content,
        "⚖️ 法定合同与审计卷宗索引": tab4_content,
    })

    main_view = mo.vstack([
        latex_style,
        mo.md("# 陆川九龙山庄改造提升项目商业统筹研报"),
        mo.md("**梁清波 商业专案库 · 合同代号 GY-2021-YW-050 · 温泉生态度假村与固定总价包干操盘典藏**"),
        mo.md("""
        > 🏛️ **项目属性与商业架构说明**：本项目系广西陆川温泉生态康养度假胜地（30,000 ㎡）改造提升软装工程。全案涵盖通高大堂、豪华中餐包房、温泉水疗中心等**公区五星级会所（236.22 万元）**与**主楼 188 间客房及半山独栋汤院（317.24 万元）**。商务让利下浮 34,550 元后以 **550.00 万元固定总价包干**签约；设立 **30/50/15/5** 资金付款节奏，在**货物到场初验时即回收累计 80%（440.00 万元）超额覆盖出厂成本**；梁清波团队驻场督导，**28 天极限穿插抢工**实现全案 2,046 件实物如期交付迎宾！
        """),
        kpi_cards_html,
        report_tabs
    ])

    return latex_style, main_view, report_tabs


@app.cell
def __(main_view):
    # 应用入口渲染导出
    main_view
    return


if __name__ == "__main__":
    app.run()
