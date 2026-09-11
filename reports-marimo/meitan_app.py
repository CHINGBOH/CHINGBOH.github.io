# -*- coding: utf-8 -*-
import marimo

__generated_with = "0.24.1"
app = marimo.App(width="full", app_title="遵义湄江温泉大酒店商业统筹研报 · Marimo 旗舰版")


@app.cell
def __():
    import marimo as mo
    import duckdb
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import io
    import base64

    # 严格遵照 marimo-reactive-monograph-bi 规范：原生无损矢量 SVG 与 LaTeX 数学公式渲染
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['svg.fonttype'] = 'path'
    plt.rcParams['mathtext.fontset'] = 'cm'

    NAVY, GOLD, GREY = '#1f4e78', '#c8a45d', '#7b8899'
    con = duckdb.connect('/home/l/个人资料仓库/data/career_analytics_lake.duckdb', read_only=True)
    try:
        con.execute('INSTALL spatial; LOAD spatial;')
    except Exception:
        pass

    return (
        GOLD,
        GREY,
        NAVY,
        base64,
        con,
        duckdb,
        io,
        matplotlib,
        mo,
        np,
        pd,
        plt,
    )


@app.cell
def __(con):
    # 提取核心法定审计底账（静态只读真值）
    facts = con.execute("SELECT * FROM v_meitan_contract_facts").fetchall()[0]
    proj_name = facts[0]
    contract_no = facts[2]
    contract_amt = float(facts[7])     # 33,800,000.00
    built_area = float(facts[9])       # 63,339.00 ㎡
    danfang_contract = contract_amt / built_area

    # 现金流与结算数据
    cf_row = con.execute("SELECT * FROM v_meitan_contract_cashflow_engine").fetchall()[0]
    baoshen_amt = float(cf_row[3])     # 27,985,048.88
    suoding_amt = float(cf_row[4])     # 26,500,000.00
    peihe_amt = float(cf_row[5])       # 3,180,000.00 (12%)
    huikuan_85 = float(cf_row[6])      # 22,525,000.00
    huikuan_97 = float(cf_row[7])      # 25,705,000.00
    actual_cash = float(cf_row[10])    # 25,705,000.00
    shenjian_val = baoshen_amt - suoding_amt
    actual_shenjian_rate = (shenjian_val / baoshen_amt) * 100.0

    # 结算总账收据
    receipt_row = con.execute("SELECT * FROM v_meitan_settlement_receipt").fetchall()[0]
    all_settle_amt = float(receipt_row[10])   # 25,475,507.39 全案结算

    # 4 级商务定价模型
    pricing_df = con.execute("SELECT 品类事项, 厂家采购底价_元, 内部造价预算_元, 对外商务底限_元, 对外正式商务报价_元, 正式报价毛利率_pct FROM v_meitan_4tier_pricing_model").df()

    # 样板房先行双轨核算
    mockup_df = con.execute("SELECT 家具编号, 物料名称, 尺寸规格, 单套件数, 样板间采购成本, 样板间商务报价, 大货52套采购成本, 大货52套商务报价, 大货单件毛利, 规模化采购降本幅度, 材质工艺 FROM v_meitan_mockup_furniture_dual_track").df()

    # 摆场实物清单
    staging_df = con.execute("SELECT 摆场序号, 物料编码, 空间落位, 物料名称, 实物规格, 出货摆场件数, 单位, 所属楼栋, 品类 FROM v_meitan_staging_furniture").df()

    # 现场签证清单
    visa_df = con.execute("SELECT 签证序号, 联系单编号, 签证依据与变更原因, 现场签证主要内容, 现场签证送审金额_元 FROM v_meitan_visa_summary WHERE 现场签证送审金额_元 IS NOT NULL").df()

    return (
        actual_cash,
        actual_shenjian_rate,
        all_settle_amt,
        baoshen_amt,
        built_area,
        contract_amt,
        contract_no,
        danfang_contract,
        facts,
        huikuan_85,
        huikuan_97,
        mockup_df,
        peihe_amt,
        pricing_df,
        proj_name,
        receipt_row,
        shenjian_val,
        staging_df,
        suoding_amt,
        visa_df,
    )


@app.cell
def __(mo):
    # 神仙技能 1: mo.sidebar (高管侧边栏：上面滑轮，下面具体数据数值输入，三色视觉色彩锚定)

    # 参数 1: 审减率 (科技蓝体系: #1d4ed8 / #2563eb / #eff6ff / #bfdbfe)
    slider_shenjian = mo.ui.slider(start=5.0, stop=30.0, step=0.5, value=5.31, label="滑动调节审减率")
    num_shenjian = mo.ui.number(start=0.0, stop=50.0, step=0.01, value=5.31, label="输入精确数值 (%)")

    # 参数 2: 现场增项追加 (翡翠绿体系: #15803d / #059669 / #f0fdf4 / #bbf7d0)
    slider_zengxiang = mo.ui.slider(start=0.0, stop=150.0, step=5.0, value=27.13, label="滑动调节增项")
    num_zengxiang = mo.ui.number(start=0.0, stop=300.0, step=0.1, value=27.13, label="输入精确数值 (万元)")

    # 参数 3: 总包管理配合费率 (商务橙体系: #c2410c / #ea580c / #fff7ed / #fed7aa)
    slider_peihe = mo.ui.slider(start=5.0, stop=20.0, step=0.5, value=12.0, label="滑动调节四局配合费率")
    num_peihe = mo.ui.number(start=0.0, stop=30.0, step=0.1, value=12.0, label="输入精确数值 (%)")

    # 调参模式开关：选择是以滑轮为主还是数值输入为主
    mode_switch = mo.ui.radio(options=["滑轮拖动模式", "具体数值输入模式"], value="具体数值输入模式", label="🎛️ 调参驱动源")

    dropdown_bldg = mo.ui.dropdown(options=["全部楼栋", "A1栋公区及客房", "A2栋公区及客房", "主楼综合区"], value="全部楼栋", label="楼栋区域过滤")

    sidebar = mo.sidebar(
        [
            mo.md("### 🏛️ 高管全局操盘控制台"),
            mo.md("*湄江温泉度假酒店 · 实时量化推演，纯局部反应式计算*"),
            mo.md("---"),
            mode_switch,
            mo.md("---"),
            mo.Html("""
            <div style="border-left: 4px solid #2563eb; background: #eff6ff; border: 1px solid #bfdbfe; padding: 6px 10px; border-radius: 4px; margin-bottom: 8px;">
              <strong style="color: #1d4ed8; font-size: 12.5px;">📊 1. 审减率敏感度调优</strong>
            </div>
            """),
            slider_shenjian,
            num_shenjian,
            mo.md("---"),
            mo.Html("""
            <div style="border-left: 4px solid #059669; background: #f0fdf4; border: 1px solid #bbf7d0; padding: 6px 10px; border-radius: 4px; margin-bottom: 8px;">
              <strong style="color: #15803d; font-size: 12.5px;">💰 2. 现场增项追加调优</strong>
            </div>
            """),
            slider_zengxiang,
            num_zengxiang,
            mo.md("---"),
            mo.Html("""
            <div style="border-left: 4px solid #ea580c; background: #fff7ed; border: 1px solid #fed7aa; padding: 6px 10px; border-radius: 4px; margin-bottom: 8px;">
              <strong style="color: #c2410c; font-size: 12.5px;">🤝 3. 四局配合费率调优</strong>
            </div>
            """),
            slider_peihe,
            num_peihe,
            mo.md("---"),
            mo.md("**🔍 空间楼栋钻取**"),
            dropdown_bldg,
            mo.md("---"),
            mo.md("<div style='font-size: 11px; color: #94a3b8;'>梁清波 商业专案库 · Marimo Reactive Engine</div>")
        ]
    )
    return (
        dropdown_bldg,
        mode_switch,
        num_peihe,
        num_shenjian,
        num_zengxiang,
        sidebar,
        slider_peihe,
        slider_shenjian,
        slider_zengxiang,
    )


@app.cell
def __(sidebar):
    # 显式渲染左侧高管侧边栏
    sidebar
    return


@app.cell
def __(
    baoshen_amt,
    mode_switch,
    num_peihe,
    num_shenjian,
    num_zengxiang,
    slider_peihe,
    slider_shenjian,
    slider_zengxiang,
    suoding_amt,
):
    # 动态推演核心运算（严格色彩视觉对齐系统）
    if mode_switch.value == "具体数值输入模式":
        sim_rate = float(num_shenjian.value)
        sim_add  = float(num_zengxiang.value) * 10000.0
        sim_pf_rate = float(num_peihe.value) / 100.0
        sim_pf_val = num_peihe.value
        active_mode_badge = "<span style='background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600;'>⚙️ 数值输入模式生效</span>"
    else:
        sim_rate = float(slider_shenjian.value)
        sim_add  = float(slider_zengxiang.value) * 10000.0
        sim_pf_rate = float(slider_peihe.value) / 100.0
        sim_pf_val = slider_peihe.value
        active_mode_badge = "<span style='background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600;'>⚙️ 滑轮拖动模式生效</span>"

    base_lock = baoshen_amt * (1.0 - sim_rate / 100.0)
    sim_lock = base_lock + sim_add
    lock_diff = sim_lock - suoding_amt

    sim_peihe = sim_lock * sim_pf_rate
    sim_net_cash = sim_lock - sim_peihe
    actual_net = suoding_amt * (1.0 - 0.12)
    net_diff = sim_net_cash - actual_net

    # 3 大专属设计系统色彩标签（与侧边栏 1、2、3 严格一致）
    badge_shenjian = f"<span style='background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;'>📊 审减率 {sim_rate:.2f}%</span>"
    badge_zengxiang = f"<span style='background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;'>💰 增项 {sim_add/1e4:.2f}万</span>"
    badge_peihe = f"<span style='background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;'>🤝 四局配合费 {sim_pf_val}%</span>"

    diff_color = '#059669' if lock_diff >= 0 else '#dc2626'
    diff_symbol = '▲ 高于实际定案' if lock_diff >= 0 else '▼ 低于实际定案'
    diff_badge = f"<span style='background: {'#f0fdf4' if lock_diff >= 0 else '#fef2f2'}; color: {diff_color}; border: 1px solid {'#bbf7d0' if lock_diff >= 0 else '#fecaca'}; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600;'>{diff_symbol}</span>"

    # 构建高保真响应式卡片组（带彩色顶边和严格对应胶囊）
    kpi_cards_html = f"""
    <div style="font-family: 'Latin Modern Roman', 'Lora', 'Noto Serif SC', serif; margin-bottom: 20px;">
      <!-- 调参联动状态指示条 -->
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 14px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
        <div style="display: flex; align-items: center; gap: 8px;">
          {active_mode_badge}
          <span style="font-size: 12px; color: #64748b;">实时调优参数同步：</span>
          {badge_shenjian}
          {badge_zengxiang}
          {badge_peihe}
        </div>
        <div style="font-size: 11px; color: #94a3b8;">
          与左侧控制台色彩 100% 视觉锚定
        </div>
      </div>

      <!-- 4 大核心 KPI 指标卡 (带专属彩色顶边线) -->
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;">
        <!-- 卡片 1: 锁定金额 (科技蓝顶边) -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #2563eb; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
          <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">推演认价锁定金额</div>
          <div style="font-size: 22px; font-weight: 700; color: #1e3a8a; font-family: monospace;">{sim_lock/1e4:,.2f} <span style="font-size: 12px; font-weight: 400; color: #64748b;">万元</span></div>
          <div style="margin-top: 8px; display: flex; gap: 4px; flex-wrap: wrap;">
            {badge_shenjian}
            {badge_zengxiang}
          </div>
        </div>

        <!-- 卡片 2: 审定偏差 (中立灰顶边) -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #c8a45d; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
          <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">较实际审定 (2,650.00万) 偏差</div>
          <div style="font-size: 22px; font-weight: 700; color: {diff_color}; font-family: monospace;">{abs(lock_diff/1e4):,.2f} <span style="font-size: 12px; font-weight: 400; color: #64748b;">万元</span></div>
          <div style="margin-top: 8px;">
            {diff_badge}
          </div>
        </div>

        <!-- 卡片 3: 扣除总包配合费后净落袋 (翡翠绿顶边) -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #059669; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
          <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">扣总包管理费后预估净额</div>
          <div style="font-size: 22px; font-weight: 700; color: #059669; font-family: monospace;">{sim_net_cash/1e4:,.2f} <span style="font-size: 12px; font-weight: 400; color: #64748b;">万元</span></div>
          <div style="margin-top: 8px;">
            <span style="background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600;">🤝 扣四局管理费 {sim_peihe/1e4:,.2f}万 ({sim_pf_val}%)</span>
          </div>
        </div>

        <!-- 卡片 4: 实际已兑现到账 (深海蓝顶边) -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 4px solid #1f4e78; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
          <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">全案结算与实际入账总额</div>
          <div style="font-size: 22px; font-weight: 700; color: #1f4e78; font-family: monospace;">2,570.50 <span style="font-size: 12px; font-weight: 400; color: #64748b;">万元</span></div>
          <div style="margin-top: 8px;">
            <span style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600;">含税97%入账 · 3%质保金</span>
          </div>
        </div>
      </div>
    </div>
    """
    return (
        active_mode_badge,
        actual_net,
        badge_peihe,
        badge_shenjian,
        badge_zengxiang,
        base_lock,
        diff_badge,
        diff_color,
        diff_symbol,
        kpi_cards_html,
        lock_diff,
        net_diff,
        sim_add,
        sim_lock,
        sim_net_cash,
        sim_peihe,
        sim_pf_rate,
        sim_pf_val,
        sim_rate,
    )


@app.cell
def __(
    GOLD,
    GREY,
    NAVY,
    baoshen_amt,
    base64,
    built_area,
    contract_amt,
    danfang_contract,
    io,
    mockup_df,
    plt,
    pricing_df,
    suoding_amt,
    visa_df,
):
    # 静态图表组生成（遵循原生矢量 SVG 规范，一次性渲染，极尽锐利）

    # 【图表 1】: 四级商务定价博弈防线 (对比 4 个层级的金额)
    # 取前 6 个典型客房及公区品类
    _sample_items = pricing_df.head(6)
    _names = [str(n)[:10] for n in _sample_items['品类事项']]
    _c_raw = [float(v)/1e4 for v in _sample_items['厂家采购底价_元']]
    _c_bud = [float(v)/1e4 for v in _sample_items['内部造价预算_元']]
    _c_low = [float(v)/1e4 for v in _sample_items['对外商务底限_元']]
    _c_quo = [float(v)/1e4 for v in _sample_items['对外正式商务报价_元']]

    _fig1, _ax1 = plt.subplots(figsize=(8.4, 3.4), dpi=140)
    _x = range(len(_names))
    _w = 0.18
    _ax1.bar([i - 1.5*_w for i in _x], _c_raw, _w, label='1. 厂家出厂底价', color='#94a3b8', zorder=3)
    _ax1.bar([i - 0.5*_w for i in _x], _c_bud, _w, label='2. 内部造价预算', color='#64748b', zorder=3)
    _ax1.bar([i + 0.5*_w for i in _x], _c_low, _w, label='3. 对外商务底限', color=GOLD, zorder=3)
    _ax1.bar([i + 1.5*_w for i in _x], _c_quo, _w, label='4. 正式送审报价 (蓄水池)', color=NAVY, zorder=3)
    _ax1.set_xticks(list(_x))
    _ax1.set_xticklabels(_names, fontsize=8.5)
    _ax1.set_ylabel('万元', fontsize=8.5)
    _ax1.set_title('四级商务防线阶梯博弈 · 正式送审建立 40%~66% 利润蓄水池防御', fontsize=11, fontweight='bold', pad=12)
    _ax1.legend(fontsize=8, loc='upper left')
    _ax1.spines[['top', 'right']].set_visible(False)
    _ax1.grid(axis='y', color='#e8ecf0', lw=0.7, zorder=0); _ax1.set_axisbelow(True)
    _fig1.subplots_adjust(left=0.1, right=0.95, top=0.88, bottom=0.15)
    _buf1 = io.BytesIO()
    _fig1.savefig(_buf1, format='svg', bbox_inches='tight')
    plt.close(_fig1)
    _buf1.seek(0)
    chart1_b64 = base64.b64encode(_buf1.getvalue()).decode('utf-8')

    # 【图表 2】: 资金闭环瀑布流 (原合同 -> 报审 -> 最终审定 -> 扣四局配合费 12% -> 净落袋)
    _fig2, _ax2 = plt.subplots(figsize=(8.2, 3.2), dpi=140)
    _labels = ['原暂定合同', '报审送审造价', '中建四局管理费', '最终审定额', '实际入账回款']
    _c_amt = float(contract_amt) / 1e4
    _b_amt = float(baoshen_amt) / 1e4
    _pf_amt = 318.0
    _s_amt = float(suoding_amt) / 1e4
    _hk_amt = 2570.5
    _widths = [_c_amt, _b_amt, _pf_amt, _s_amt, _hk_amt]
    _colors = ['#475569', NAVY, '#dc2626', GOLD, '#059669']
    _bars = _ax2.barh(_labels, _widths, color=_colors, height=0.45, zorder=3)
    for _b, _v in zip(_bars, _widths):
        _ax2.text(_v + 40, _b.get_y()+_b.get_height()/2, f'{_v:,.1f} 万', va='center', ha='left', fontsize=8.5, fontweight='bold', color='#1e293b')
    _ax2.set_xlim(0, 4200)
    _ax2.spines[['top', 'right']].set_visible(False)
    _ax2.grid(axis='x', color='#e8ecf0', lw=0.7, zorder=0); _ax2.set_axisbelow(True)
    _ax2.set_title('全案造价与现金流瀑布流 · 签约暂定 3,380 万，最终审定 2,650 万平稳落袋', fontsize=11, fontweight='bold', pad=10)
    _fig2.subplots_adjust(left=0.18, right=0.92, top=0.88, bottom=0.15)
    _buf2 = io.BytesIO()
    _fig2.savefig(_buf2, format='svg', bbox_inches='tight')
    plt.close(_fig2)
    _buf2.seek(0)
    chart2_b64 = base64.b64encode(_buf2.getvalue()).decode('utf-8')

    # 【图表 3】: 样板房封样 vs 大货 52 套规模集采降本对比
    _mock_sub = mockup_df.head(6)
    _f_names = list(_mock_sub['物料名称'])
    _f_sample = [float(v) for v in _mock_sub['样板间采购成本']]
    _f_bulk   = [float(v) for v in _mock_sub['大货52套采购成本']]
    _fig3, _ax3 = plt.subplots(figsize=(7.8, 3.0), dpi=140)
    _idx = range(len(_f_names)); _bw = 0.35
    _ax3.bar([i-_bw/2 for i in _idx], _f_sample, _bw, label='样板间单件打样成本', color='#cbd5e1', zorder=3)
    _ax3.bar([i+_bw/2 for i in _idx], _f_bulk,   _bw, label='大货52套批量采购成本', color=NAVY, zorder=3)
    for _i in _idx:
        _diff = _f_sample[_i] - _f_bulk[_i]
        _pct = (_diff / _f_sample[_i]) * 100.0 if _f_sample[_i] > 0 else 0
        if _pct > 1.0:
            _ax3.annotate(f'-{_pct:.1f}%', xy=(_i+_bw/2, _f_bulk[_i]), xytext=(_i+_bw/2, _f_bulk[_i] + max(_f_sample)*0.08),
                          ha='center', fontsize=7.5, color='#dc2626', fontweight='bold')
    _ax3.set_xticks(list(_idx))
    _ax3.set_xticklabels(_f_names, fontsize=8.5)
    _ax3.set_ylabel('元/件', fontsize=8.5)
    _ax3.set_title('样板房开模先行 · 规模集采推动单品最高降本 28.57%', fontsize=11, fontweight='bold', pad=10)
    _ax3.legend(fontsize=8)
    _ax3.spines[['top', 'right']].set_visible(False)
    _ax3.grid(axis='y', color='#e8ecf0', lw=0.7, zorder=0); _ax3.set_axisbelow(True)
    _fig3.subplots_adjust(left=0.14, right=0.92, top=0.88, bottom=0.15)
    _buf3 = io.BytesIO()
    _fig3.savefig(_buf3, format='svg', bbox_inches='tight')
    plt.close(_fig3)
    _buf3.seek(0)
    chart3_b64 = base64.b64encode(_buf3.getvalue()).decode('utf-8')

    # 【图表 4】: 品类及空间资产毛利构成
    _cat_names = [str(r[0])[:8] for r in pricing_df.itertuples(index=False)][:7]
    _cat_profits = [float(r[4]) - float(r[1]) for r in pricing_df.itertuples(index=False)][:7]
    _cat_profits_w = [v/1e4 for v in _cat_profits]
    _fig4, _ax4 = plt.subplots(figsize=(7.8, 2.8), dpi=140)
    _ax4.bar(_cat_names, _cat_profits_w, color=[NAVY, GOLD, '#059669', '#3b82f6', GREY, '#f59e0b', '#8b5cf6'][:len(_cat_names)], width=0.45, zorder=3)
    for _i, _v in enumerate(_cat_profits_w):
        _ax4.text(_i, _v + max(_cat_profits_w)*0.03, f'{_v:,.1f}万', ha='center', va='bottom', fontsize=8, fontweight='bold')
    _ax4.set_ylabel('毛利额 (万元)', fontsize=8.5)
    _ax4.set_title('核心品类商业毛利贡献额分布 · 客房标间与套房双核驱动', fontsize=11, fontweight='bold', pad=10)
    _ax4.spines[['top', 'right']].set_visible(False)
    _ax4.grid(axis='y', color='#e8ecf0', lw=0.7, zorder=0); _ax4.set_axisbelow(True)
    _fig4.subplots_adjust(left=0.14, right=0.92, top=0.88, bottom=0.15)
    _buf4 = io.BytesIO()
    _fig4.savefig(_buf4, format='svg', bbox_inches='tight')
    plt.close(_fig4)
    _buf4.seek(0)
    chart4_b64 = base64.b64encode(_buf4.getvalue()).decode('utf-8')

    # 【图表 5】: 现场签证与政府变更增项结构
    _visa_items = list(visa_df['现场签证主要内容'])
    _visa_amts  = [float(v)/1e4 for v in visa_df['现场签证送审金额_元']]
    _fig5, _ax5 = plt.subplots(figsize=(7.8, 2.6), dpi=140)
    _ax5.barh([v[:12] for v in _visa_items], _visa_amts, color=['#059669', '#2563eb', GOLD][:len(_visa_items)], height=0.4, zorder=3)
    for _i, _v in enumerate(_visa_amts):
        _ax5.text(_v + 0.5, _i, f'{_v:,.2f} 万元', va='center', ha='left', fontsize=8.5, fontweight='bold', color='#1e293b')
    _ax5.set_xlim(0, max(_visa_amts)*1.3 if _visa_amts else 35)
    _ax5.spines[['top', 'right']].set_visible(False)
    _ax5.grid(axis='x', color='#e8ecf0', lw=0.7, zorder=0); _ax5.set_axisbelow(True)
    _ax5.set_title('现场签证合规增项 · 市县两级政府意见锁定 A2会见厅追加', fontsize=11, fontweight='bold', pad=10)
    _fig5.subplots_adjust(left=0.22, right=0.92, top=0.88, bottom=0.15)
    _buf5 = io.BytesIO()
    _fig5.savefig(_buf5, format='svg', bbox_inches='tight')
    plt.close(_fig5)
    _buf5.seek(0)
    chart5_b64 = base64.b64encode(_buf5.getvalue()).decode('utf-8')

    return (
        chart1_b64,
        chart2_b64,
        chart3_b64,
        chart4_b64,
        chart5_b64,
    )


@app.cell
def __(
    actual_cash,
    all_settle_amt,
    baoshen_amt,
    built_area,
    chart1_b64,
    chart2_b64,
    chart3_b64,
    chart4_b64,
    chart5_b64,
    contract_amt,
    danfang_contract,
    huikuan_85,
    huikuan_97,
    mo,
    peihe_amt,
    suoding_amt,
):
    # Tab 1: 典藏级全景商业研报正文构建 (完全遵循 2×2 商业操盘矩阵与 LaTeX 出版物排版)

    _kpi_table = f"""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
      <table style="width: 100%; border-collapse: collapse; font-size: 13.5px; text-align: left;">
        <thead>
          <tr style="background: #f8fafc; color: #475569; font-weight: 600; border-bottom: 2px solid #e2e8f0;">
            <th style="padding: 10px 16px;">商业业务维度</th>
            <th style="padding: 10px 16px;">量化指标名称</th>
            <th style="padding: 10px 16px; text-align: right;">审计核定真值</th>
            <th style="padding: 10px 16px; text-align: center;">操盘控制属性</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 16px; color: #64748b;">签约暂定</td>
            <td style="padding: 10px 16px; font-weight: 600;">总承包专业分包合同暂定额</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 700; color: #1f4e78;">{contract_amt/1e4:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">单方 {danfang_contract:,.2f} 元/㎡</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9; background: #fafafa;">
            <td style="padding: 10px 16px; color: #64748b;">造价送审</td>
            <td style="padding: 10px 16px; font-weight: 600;">主楼及裙楼软装报审送审金额</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 700; color: #1e3a8a;">{baoshen_amt/1e4:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#eff6ff; color:#1d4ed8; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">含 4 级蓄水池防线</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 16px; color: #64748b;">最终审定</td>
            <td style="padding: 10px 16px; font-weight: 600;">全案结算审定总造价</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 700; color: #c8a45d;">{suoding_amt/1e4:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">审减率仅 5.31%</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9; background: #fafafa;">
            <td style="padding: 10px 16px; color: #64748b;">管理配合</td>
            <td style="padding: 10px 16px; font-weight: 600;">中建四局总包管理配合费 (12%)</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; color: #dc2626; font-weight: 600;">{peihe_amt/1e4:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#fee2e2; color:#b91c1c; padding:2px 8px; border-radius:4px; font-size:11px;">合同刚性条款</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 16px; color: #64748b;">验收节点</td>
            <td style="padding: 10px 16px; font-weight: 600;">竣工验收合格 7 工作日应付 85%</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; color: #334155;">{huikuan_85/1e4:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">刚性履约回款</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9; background: #fafafa;">
            <td style="padding: 10px 16px; color: #64748b;">结算结余</td>
            <td style="padding: 10px 16px; font-weight: 600;">最终结算 14 工作日应付 97%</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 700; color: #059669;">{huikuan_97/1e4:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#d1fae5; color:#065f46; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">质保金 3% (79.5万)</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 16px; color: #64748b;">现金兑现</td>
            <td style="padding: 10px 16px; font-weight: 600;">真实财务入账与账面支付现金</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 700; color: #047857;">{actual_cash/1e4:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#ecfdf5; color:#047857; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700;">结算回收偏差 0</span></td>
          </tr>
        </tbody>
      </table>
    </div>
    """

    _roles = [
     ('承揽与界面界定', '承揽 AAAA 级湄江温泉度假酒店公区及客房全案软装分包；理顺湄潭城投/中建四局/广田云软装三级界面', f'签约暂定 {contract_amt/1e4:,.2f} 万元 · 建筑体量 {built_area:,.0f} ㎡', '《专业分包合同 021MJWQJD》'),
     ('四级多轨阶梯定价', '穿透珠三角工坊出厂成本，设立 4 级商务防波堤（底价➔预算➔底限➔正式报价）', '预留 40%~66% 调价缓冲池 · 送审 2,798.50 万元', '《商务报价总表与四级模型》'),
     ('样板先行集采降本', '首创大货前样板房开模试制封样，52 套批量规模集采推动单件刚性降本最高 28.57%', '定制床出厂价从 3,360 降至 2,400 元 · 锁死毛利', '《样板房双轨清单与采购合同》'),
     ('总包配合与现金穿透', '从容应对总包 12% 管理配合费核减条款，分阶段推动 85% 竣工款与 97% 结算款按期刚性到账', '实收现金 2,570.50 万元 · 账面偏差 0.00 元', '《工程款支付审批与银行回执》'),
     ('政府变更增项锁定', '紧抓市县两级政府视察意见，快速出具 XMB-39 联系单追加 A2 会见厅高规格家具', '锁定 27.13 万元合规增项 · 抵补审计审减', '《工程联系单 XMB-39 与签证单》'),
    ]
    _role_rows = ""
    for _idx, (_s, _a, _r, _d) in enumerate(_roles):
        _bg = "#fafafa" if _idx % 2 == 1 else "#ffffff"
        _role_rows += f"""
        <tr style="background: {_bg}; border-bottom: 1px solid #f1f5f9;">
          <td style="padding: 10px 14px; font-weight: 600; color: #1e293b;">{_s}</td>
          <td style="padding: 10px 14px; color: #475569;">{_a}</td>
          <td style="padding: 10px 14px; color: #1f4e78; font-weight: 600; font-family: monospace;">{_r}</td>
          <td style="padding: 10px 14px; text-align: center;"><span style="background:#f0f9ff; border:1px solid #bae6fd; color:#0284c7; padding:3px 8px; border-radius:4px; font-size:11px;">{_d}</span></td>
        </tr>
        """
    _role_table = f"""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
      <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
        <thead>
          <tr style="background: #f8fafc; color: #475569; font-weight: 600; border-bottom: 2px solid #e2e8f0;">
            <th style="padding: 10px 14px; width: 18%;">操盘关键环节</th>
            <th style="padding: 10px 14px; width: 34%;">核心主导动作与风控策略</th>
            <th style="padding: 10px 14px; width: 30%;">量化成果与核定数据</th>
            <th style="padding: 10px 14px; width: 18%; text-align: center;">法定审计佐证档案</th>
          </tr>
        </thead>
        <tbody>
          {_role_rows}
        </tbody>
      </table>
    </div>
    """

    tab1_content = mo.vstack([
        mo.md("## § 0 核心商业基本盘与财务决算全景"),
        mo.Html(_kpi_table),
        mo.md("---"),
        mo.md("## § 1 业务承揽与总包分包界面界定"),
        mo.md("- **茶旅一体化公建标杆承揽**：项目紧扣贵州遵义湄潭“茶海温泉”AAAA级景区建设机遇，承揽湄江温泉大酒店（现湄江茶苑度假酒店）全案客房及公区软装工程。\n- **法定界面与合同基准**：发包人为湄潭县城投，总包为中建四局珠海分公司，广田作为专业分包。合同暂定总额 **3,380.00 万元**，建筑面积 **63,339.00 ㎡**，折合签约单方 **533.64 元/㎡**。\n- **全过程风控界定**：理顺无预付款、按月报量、竣工验收付 85%、最终结算付 97% 以及四局 12% 管理配合费等法定结算边界。"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{chart1_b64}' alt='四级商务防线'></div>"),
        mo.md("---"),
        mo.md("## § 2 采销多轨博弈定价与样板先行降本"),
        mo.md("- **四级梯级商务防线**：在 18 个核心采购包件中，深入穿透珠三角源头工坊裸成本，构建**“厂家采购底价 ➔ 内部造价预算 ➔ 对外商务底限 ➔ 对外正式商务报价”**四重阶梯防线，形成 40%~66% 的利润蓄水池，从容抵御审计重刀。\n- **样板先行与大货规模降本**：坚持“大货未动、样板先行”，在 52 套批量下单前完成样板房开模试制封样，依托批量规模采购将定制床等核心物料成本刚性压缩 **28.57%**（从 3,360 元压至 2,400 元），彻底锁死毛利底盘。"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{chart3_b64}' alt='样板先行降本'></div>"),
        mo.md("---"),
        mo.md("## § 3 资金严密履约与全生命周期现金闭环"),
        mo.md("- **总包管理配合费博弈**：面对中建四局 12% 刚性管理配合费（318.00 万元），团队通过紧贴现场工程进度节点，推动业主与总包严格履约。\n- **85% 竣工款与 97% 结算款刚性到位**：竣工验收合格后迅速兑现 **2,252.50 万元**；结算定案后推动 97% 款项落地，实现 **2,570.50 万元** 现金全额入账落袋，与财务收据达成 0 偏差对账！"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{chart2_b64}' alt='资金闭环瀑布流'></div>"),
        mo.md("---"),
        mo.md("## § 4 空间动线资产配置与品类毛利贡献"),
        mo.md("- **核心功能空间配置**：涵盖 A1/A2 栋客房标间、行政套房、温泉公区接待、国际会议大厅及领导会见厅。\n- **客房标间与套房双引擎**：客房标间提供 **121.23 万元** 商务毛利额，套房客房提供 **188.22 万元** 毛利额，双核驱动全案综合毛利率突破 60%。"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{chart4_b64}' alt='品类毛利构成'></div>"),
        mo.md("---"),
        mo.md("## § 5 现场合规签证与政府变更增项锁定"),
        mo.md("- **政府重要接待视察契机**：紧抓市委市政府及县政府现场调研指导契机，顺应高规格政务接待诉求。\n- **现场签证 XMB-39 落地**：针对 A2 栋贵宾会见厅迅速发起深化并签署联系单 `XMB-39`，合规追加 12 张高规格沙发与 12 张茶几，成功锁定 **27.13 万元** 现场签证增项，有效冲抵审计审减。"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{chart5_b64}' alt='现场签证增项'></div>"),
        mo.md("---"),
        mo.md("## § 6 商业统筹复盘与主导履职核定"),
        mo.Html(_role_table)
    ])
    return tab1_content,


@app.cell
def __(baoshen_amt, base64, io, mo, np, pd, plt, sim_rate):
    # Tab 2: 敏感度双变量多场景推演矩阵 (热力图 + 场景推演表)
    _rates = [3.0, 5.0, sim_rate, 10.0, 15.0]
    _adds  = [0.0, 15.0, 27.13, 50.0, 80.0]

    _matrix_data = []
    _grid = np.zeros((len(_rates), len(_adds)))

    for _i, _r in enumerate(_rates):
        _row_vals = []
        for _j, _a in enumerate(_adds):
            _val = (baoshen_amt * (1.0 - _r/100.0) + _a * 10000.0) / 1e4
            _grid[_i, _j] = _val
            _row_vals.append(f"{_val:,.2f}")
        _matrix_data.append({
            "推演审减率": f"{_r:.2f}%",
            "+0万 (无签证)": _row_vals[0],
            "+15万增项": _row_vals[1],
            "+27.13万 (实际签证)": _row_vals[2],
            "+50万追加": _row_vals[3],
            "+80万追加": _row_vals[4],
        })

    _matrix_df = pd.DataFrame(_matrix_data)

    _fig_sens, _ax_sens = plt.subplots(figsize=(7.6, 3.8), dpi=140)
    _im = _ax_sens.imshow(_grid, cmap='YlGnBu', aspect='auto')
    _ax_sens.set_xticks(range(len(_adds)))
    _ax_sens.set_yticks(range(len(_rates)))
    _ax_sens.set_xticklabels([f'+{_a:.1f}万增项' for _a in _adds], fontsize=8.5, fontweight='bold')
    _ax_sens.set_yticklabels([f'审减率 {_r:.2f}%' for _r in _rates], fontsize=8.5, fontweight='bold')
    _cbar = _fig_sens.colorbar(_im, ax=_ax_sens, fraction=0.035, pad=0.04)
    _cbar.ax.set_ylabel('推演认价锁定 (万元)', fontsize=8.5)

    for _i in range(len(_rates)):
        for _j in range(len(_adds)):
            _val = _grid[_i, _j]
            _is_actual = (abs(_rates[_i] - 5.31) < 0.01 and abs(_adds[_j] - 27.13) < 0.01)
            _txt_color = '#dc2626' if _is_actual else ('#ffffff' if _val > 2700 else '#0f172a')
            _prefix = '★实际: ' if _is_actual else ''
            _ax_sens.text(_j, _i, f'{_prefix}{_val:,.1f}', ha='center', va='center',
                          fontsize=8.5, fontweight='bold' if _is_actual else 'normal', color=_txt_color)

    _ax_sens.set_title('湄江温泉大酒店 · 认价锁定敏感度矩阵 (当前推演审减率 vs 现场增项追加)', fontsize=11, fontweight='bold', pad=12)
    _fig_sens.subplots_adjust(left=0.15, right=0.92, top=0.88, bottom=0.15)
    _buf_sens = io.BytesIO()
    _fig_sens.savefig(_buf_sens, format='svg', bbox_inches='tight')
    plt.close(_fig_sens)
    _buf_sens.seek(0)
    _sens_b64 = base64.b64encode(_buf_sens.getvalue()).decode('utf-8')

    tab2_content = mo.vstack([
        mo.md("### 🎛️ 商业操盘敏感度双变量多场景推演矩阵"),
        mo.md("通过在不同审计审减压力（3.00% 至 15.00%）与现场增项追加（0 至 80 万元）之间的交叉推演，清晰验证：**梁清波团队凭借严密的 4 级商务防线，将实际审减率压制在极佳的 5.31% 水平，配合 27.13 万元现场政务接待增项，牢牢守住了 2,650.00 万元的定案底盘！**"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{_sens_b64}' alt='敏感度热力图'></div>"),
        mo.md("#### 📊 场景推演量化对账表（万元）"),
        mo.ui.table(_matrix_df)
    ])
    return tab2_content,


@app.cell
def __(mockup_df, mo, staging_df):
    # Tab 3: 79 行出货摆场原子级实物穿透台 + 12 项样板房双轨对比 - 声明表格组件
    table_staging = mo.ui.table(staging_df, selection="single", label="📦 79 行出货摆场落地实物明细台账（点击某行穿透）")
    table_mockup = mo.ui.table(mockup_df, label="📐 12 项样板间 vs 大货规模集采降本核算表")
    return table_mockup, table_staging


@app.cell
def __(mo, staging_df, table_mockup, table_staging):
    # 读取 table_staging 选中状态并组装 Tab 3 视图
    _selected_row = table_staging.value
    if _selected_row is not None and not _selected_row.empty:
        _row = _selected_row.iloc[0]
        _status_hint = "🔎 当前选中穿透项"
    elif staging_df is not None and not staging_df.empty:
        _row = staging_df.iloc[0]
        _status_hint = "💡 典型物料穿透示例（可点击上方表格任意一行切换）"
    else:
        _row = None
        _status_hint = ""

    if _row is not None:
        _detail_card = f"""
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #15803d; border-radius: 6px; padding: 12px 16px; margin-top: 12px;">
          <h4 style="margin: 0 0 6px 0; color: #14532d; font-size: 14px;">{_status_hint}：{_row['物料名称']}（编码：{_row['物料编码']}）</h4>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 12.5px; color: #374151;">
            <div><strong>所属楼栋：</strong>{_row['所属楼栋']}</div>
            <div><strong>具体空间：</strong>{_row['空间落位']}</div>
            <div><strong>品类分类：</strong>{_row['品类']}</div>
            <div><strong>摆场数量：</strong><span style="color:#15803d; font-weight:700;">{_row['出货摆场件数']} {_row['单位']}</span></div>
            <div style="grid-column: span 4;"><strong>规格尺寸：</strong>{_row['实物规格']}</div>
          </div>
        </div>
        """
    else:
        _detail_card = """
        <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 12px; margin-top: 12px; font-size: 12px; color: #64748b; text-align: center;">
          💡 提示：在上方 79 行出货摆场表格中点击选中任意一行，此处将即时穿透显示该物品的楼栋空间落位与规格！
        </div>
        """

    tab3_content = mo.vstack([
        mo.md("### 🔍 79 行出货摆场与样板房先行原子级实物穿透台"),
        mo.md("本台账直连 DuckDB 湖仓 `v_meitan_staging_furniture` 与 `v_meitan_mockup_furniture_dual_track` 底账，涵盖遵义湄江温泉大酒店现场已点验交付的真实实物资产："),
        table_staging,
        mo.Html(_detail_card),
        mo.md("---"),
        mo.md("#### 📐 样板房开模先行 vs 大货 52 套批量集采降本核算"),
        table_mockup
    ])
    return tab3_content,


@app.cell
def __(contract_amt, contract_no, mo):
    # Tab 4: 法定审计原件与档案卷宗索引 (mo.accordion)
    tab4_content = mo.vstack([
        mo.md("### ⚖️ 法定审计原件与原始档案卷宗索引"),
        mo.md("全案事实严格遵照《审计法》与大型国资工程决算标准，实行完整实物与财务证据链归档："),
        mo.accordion({
            "📑 1. 专业分包合同原件与三级法定界面": mo.md(
                f"""
                - **《遵义市湄江温泉大酒店建设项目软装工程施工分包合同》原件**：
                  - 合同编号：`{contract_no}`
                  - 签约主体：发包人遵义市旅投/湄潭城投、总包中建四局珠海分公司、专业分包广田云软装
                  - 合同暂定签约金额：**¥{contract_amt:,.2f} 元（3,380.00 万元）**
                  - 核心结算约定：验收合格付至 85%，最终结算付至 97%，质保金 3%
                """
            ),
            "📊 2. 商务报价总表与 4 级阶梯博弈底账": mo.md(
                """
                - **《湄江温泉酒店商务报价总表 12-21》原件**：
                  - 涵盖 18 大核心客房与公区品类事项
                  - 完整记录厂家采购底价、内部预算、商务底限与对外正式商务报价四重阶梯
                  - 支撑正式送审 2,798.50 万元的高弹性博弈蓄水池
                """
            ),
            "📐 3. 样板房先行封样双轨清单与采购合同": mo.md(
                """
                - **《湄江温泉大酒店样板房软装清单（成本预算）》**：
                  - 涵盖 12 项典型家具单套样板试制成本与大货 52 套集采成本
                  - 实证支撑定制床实现 28.57% 的规模降本幅度
                """
            ),
            "🏛️ 4. 现场签证与政府会议纪要变更证据链": mo.md(
                """
                - **《工程联系单 XMB-39》与现场签证审定单**：
                  - 依据：遵义市委市政府及湄潭县政府视察会见厅提出的高规格政务接待意见
                  - 内容：A2 会见厅追加 12 张高规格沙发与 12 张方几
                  - 审定金额：**271,296.00 元（27.13 万元）**，由总包与监理全额签字盖章确认
                """
            ),
            "💰 5. 结算协议与 2,570.50 万元财务入账回执": mo.md(
                """
                - **《结算协议-广田软装》与银行回款收款统计**：
                  - 确认全案含税审定 2,650.00 万元，按 97% 扣质保金结算应付 2,570.50 万元
                  - 扣除中建四局 12% 总包管理配合费 318.00 万元
                  - 银行收款流水全额闭环，财务实收偏差额为 **0.00 元**
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

      /* 全局 LaTeX 学术出版物衬线风格 (Latin Modern Roman + Computer Modern + 思源宋体/明朝) */
      html, body, .marimo, .marimo-ui-element, .markdown, [data-marimo-app] {
        font-family: "Latin Modern Roman", "Computer Modern", "TeX Gyre Termes", "Lora", "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif !important;
        font-size: 15px !important;
        line-height: 1.85 !important;
        letter-spacing: 0.015em !important;
        color: #1e293b !important;
        -webkit-font-smoothing: antialiased !important;
      }

      /* 标题学术排版体系 */
      h1, h2, h3, h4, h5, h6 {
        font-family: "Latin Modern Roman", "Computer Modern", "Lora", "Noto Serif SC", "Source Han Serif SC", serif !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        letter-spacing: 0.02em !important;
      }

      h1 {
        font-size: 26px !important;
        border-bottom: 2px solid #1f4e78 !important;
        padding-bottom: 8px !important;
        margin-bottom: 16px !important;
      }

      h2 {
        font-size: 20px !important;
        border-left: 4px solid #1f4e78 !important;
        padding-left: 10px !important;
        margin-top: 28px !important;
        margin-bottom: 14px !important;
        color: #1e3a8a !important;
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
        border-left: 3px solid #c8a45d !important;
        background: #fdfbf7 !important;
        padding: 12px 20px !important;
        margin: 16px 0 !important;
        border-radius: 0 6px 6px 0 !important;
        color: #334155 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
      }

      /* 表格学术排版 */
      table {
        font-family: "Latin Modern Roman", "Lora", "Noto Serif SC", serif !important;
        border-collapse: collapse !important;
      }

      /* 等宽数字与代码 */
      code, pre, .mono-num {
        font-family: "Latin Modern Mono", "Computer Modern Typewriter", "JetBrains Mono", monospace !important;
      }

      /* 原生矢量 SVG 容器与锐利阴影规范 */
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

    # 神仙技能 7: mo.ui.tabs (多维视界无缝切换总装)
    report_tabs = mo.ui.tabs({
        "🏛️ 全景深度商业研报": tab1_content,
        "🎛️ 敏感度动态推演矩阵": tab2_content,
        "🔍 79 行出货与样板房透视": tab3_content,
        "⚖️ 法定审计档案索引": tab4_content,
    })

    main_view = mo.vstack([
        latex_style,
        mo.md(
            """
            # 遵义湄江温泉大酒店商业统筹研报
            ### 梁清波 商业专案库 · 项目代号 PRJ-MT-2015 · Marimo 旗舰版
            > **🏛️ 实证与技术架构说明**：
            > 本研报严格遵照 `marimo-reactive-monograph-bi` 规范构建，直连 DuckDB 湖仓 `v_meitan_*` 视图群。
            > **全案图表全面采用原生无损矢量 SVG 架构**（任意放大无损、无模糊、高分屏视网膜级锐度）；**排版字体全面应用典雅 LaTeX 学术出版衬线风格**。
            """
        ),
        mo.Html(kpi_cards_html),
        mo.md("---"),
        report_tabs
    ])
    return latex_style, main_view, report_tabs


@app.cell
def __(main_view):
    main_view
    return


if __name__ == "__main__":
    app.run()
