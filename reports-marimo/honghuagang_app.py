# -*- coding: utf-8 -*-
import marimo

__generated_with = "0.24.1"
app = marimo.App(width="full", app_title="遵义红花岗南部城市综合体商业统筹研报 · Marimo 旗舰版")


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

    plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['svg.fonttype'] = 'path'
    plt.rcParams['mathtext.fontset'] = 'cm'

    NAVY, GOLD, GREY = '#1f4e78', '#c8a45d', '#7b8899'
    con = duckdb.connect('/home/l/个人资料仓库/data/career_analytics_lake.duckdb', read_only=True)
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
    cl = dict((r[0], r) for r in con.execute('SELECT * FROM v_hhg_settlement_closed_loop').fetchall())
    baoshen  = float(cl['报送金额'][1])
    suoding  = float(cl['现审定金额(税前)'][1])

    aud = dict((r[0], float(r[1])) for r in con.execute('SELECT * FROM v_hhg_settlement_audit_summary').fetchall())
    wuliao, shuijin, gangong = aud['直接软装物品清单合价'], aud['工程增值税金 (3.48%)'], aud['现场赶工配合费 (7.00%)']

    cf = dict((r[0], float(r[1])) for r in con.execute('SELECT * FROM v_hhg_cashflow_reconciliation').fetchall())
    hetong, jiekuan, huisou, jinghui = cf['总承包暂定分包合同额'], cf['业主年前借款 (垫资启动金)'], cf['年后累计回收产值款 (扣借款前)'], cf['扣除总包配合费后实际净回款']
    danfang = baoshen / 20000.0

    bom_df = con.execute('SELECT 序号, 编码, 分区, 空间位置, 类别, 名称, 规格, 数量, 单位, 单价_元, 合价_元 FROM v_hhg_atom_bom_items').df()
    return aud, baoshen, bom_df, cf, cl, danfang, gangong, hetong, huisou, jiekuan, jinghui, shuijin, suoding, wuliao


@app.cell
def __(bom_df, con, mo):
    # 神仙技能 1: mo.sidebar (高管侧边栏：上面滑轮，下面具体数据数值输入，配专属视觉色彩锚定)
    
    # 参数 1: 审减率 (科技蓝体系: #1d4ed8 / #2563eb / #eff6ff / #bfdbfe)
    slider_shenjian = mo.ui.slider(start=10.0, stop=60.0, step=0.5, value=34.65, label="滑动调节审减率")
    num_shenjian = mo.ui.number(start=0.0, stop=100.0, step=0.01, value=34.65, label="输入精确数值 (%)")
    
    # 参数 2: 增项追加 (翡翠绿体系: #15803d / #059669 / #f0fdf4 / #bbf7d0)
    slider_zengxiang = mo.ui.slider(start=0.0, stop=300.0, step=10.0, value=120.0, label="滑动调节增项")
    num_zengxiang = mo.ui.number(start=0.0, stop=500.0, step=1.0, value=120.0, label="输入精确数值 (万元)")

    # 参数 3: 总包配合费率 (商务橙体系: #c2410c / #ea580c / #fff7ed / #fed7aa)
    slider_peihe = mo.ui.slider(start=2.0, stop=15.0, step=0.5, value=7.5, label="滑动调节配合费率")
    num_peihe = mo.ui.number(start=0.0, stop=20.0, step=0.1, value=7.5, label="输入精确数值 (%)")

    # 调参模式开关：选择是以滑轮为主还是数值输入为主
    mode_switch = mo.ui.radio(options=["滑轮拖动模式", "具体数值输入模式"], value="具体数值输入模式", label="🎛️ 调参驱动源")

    dropdown_zone = mo.ui.dropdown(options=["全部区域", "公共空间", "D区", "C区"], value="全部区域", label="区域空间过滤")

    cf_df = con.execute("SELECT * FROM v_hhg_cashflow_reconciliation").df()

    sidebar = mo.sidebar(
        [
            mo.md("### 🏛️ 高管全局操盘控制台"),
            mo.md("*实时调参，纯局部动态计算，杜绝全屏白屏卡顿*"),
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
              <strong style="color: #c2410c; font-size: 12.5px;">🤝 3. 总包配合费率调优</strong>
            </div>
            """),
            slider_peihe,
            num_peihe,
            mo.md("---"),
            mo.md("**🔍 空间维度钻取**"),
            dropdown_zone,
            mo.md("---"),
            mo.md("<div style='font-size: 11px; color: #94a3b8;'>梁清波 商业专案库 · Marimo Reactive Engine</div>")
        ]
    )
    return (
        cf_df,
        dropdown_zone,
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
    # 显式渲染左侧侧边栏
    sidebar
    return


@app.cell
def __(
    baoshen,
    huisou,
    jiekuan,
    mo,
    mode_switch,
    num_peihe,
    num_shenjian,
    num_zengxiang,
    slider_peihe,
    slider_shenjian,
    slider_zengxiang,
    suoding,
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

    base_lock = baoshen * (1.0 - sim_rate / 100.0)
    sim_lock = base_lock + sim_add
    lock_diff = sim_lock - suoding

    sim_peihe = (huisou * 10000.0) * sim_pf_rate
    sim_net_cash = (huisou * 10000.0) - sim_peihe
    actual_net = 18500000.0
    net_diff = sim_net_cash - actual_net

    # 3 大专属设计系统色彩标签（与侧边栏 1、2、3 严格一致）
    badge_shenjian = f"<span style='background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;'>📊 审减率 {sim_rate:.2f}%</span>"
    badge_zengxiang = f"<span style='background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;'>💰 增项 {sim_add/1e4:.0f}万</span>"
    badge_peihe = f"<span style='background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;'>🤝 配合费率 {sim_pf_val}%</span>"

    diff_color = '#059669' if lock_diff >= 0 else '#dc2626'
    diff_symbol = '▲ 高于实际定案' if lock_diff >= 0 else '▼ 低于实际定案'
    diff_badge = f"<span style='background: {'#f0fdf4' if lock_diff >= 0 else '#fef2f2'}; color: {diff_color}; border: 1px solid {'#bbf7d0' if lock_diff >= 0 else '#fecaca'}; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600;'>{diff_symbol}</span>"

    # 构建高保真响应式卡片组（带彩色顶边和严格对应胶囊）
    kpi_cards_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin-bottom: 20px;">
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

      <!-- 4 大高管金融 KPI 卡片 -->
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;">
        <!-- 卡片 1: 对应 1.审减率(蓝) + 2.增项(绿) -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 3px solid #2563eb; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
          <div style="font-size: 12px; color: #64748b; font-weight: 500; margin-bottom: 4px;">推演认价锁定金额</div>
          <div style="font-size: 22px; font-weight: 700; color: #1d4ed8; letter-spacing: -0.5px;">
            {sim_lock/1e4:,.2f} <span style="font-size: 13px; font-weight: 500; color: #64748b;">万元</span>
          </div>
          <div style="display: flex; gap: 4px; margin-top: 8px; flex-wrap: wrap;">
            {badge_shenjian}
            {badge_zengxiang}
          </div>
        </div>

        <!-- 卡片 2: 偏差 -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 3px solid #c8a45d; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
          <div style="font-size: 12px; color: #64748b; font-weight: 500; margin-bottom: 4px;">较实际锁定 (2,408.99万) 偏差</div>
          <div style="font-size: 22px; font-weight: 700; color: #b45309; letter-spacing: -0.5px;">
            {abs(lock_diff)/1e4:,.2f} <span style="font-size: 13px; font-weight: 500; color: #64748b;">万元</span>
          </div>
          <div style="margin-top: 8px;">
            {diff_badge}
          </div>
        </div>

        <!-- 卡片 3: 对应 3.配合费率(橙) -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 3px solid #ea580c; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
          <div style="font-size: 12px; color: #64748b; font-weight: 500; margin-bottom: 4px;">推演实际净现金落袋</div>
          <div style="font-size: 22px; font-weight: 700; color: #059669; letter-spacing: -0.5px;">
            {sim_net_cash/1e4:,.2f} <span style="font-size: 13px; font-weight: 500; color: #64748b;">万元</span>
          </div>
          <div style="margin-top: 8px;">
            <span style='background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600;'>
              🤝 扣配合费 {sim_peihe/1e4:,.2f}万 ({sim_pf_val}%)
            </span>
          </div>
        </div>

        <!-- 卡片 4: 借款破局 -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-top: 3px solid #1f4e78; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
          <div style="font-size: 12px; color: #64748b; font-weight: 500; margin-bottom: 4px;">业主年前借款破局</div>
          <div style="font-size: 22px; font-weight: 700; color: #1f4e78; letter-spacing: -0.5px;">
            {float(jiekuan):,.0f} <span style="font-size: 13px; font-weight: 500; color: #64748b;">万元</span>
          </div>
          <div style="margin-top: 8px;">
            <span style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600;">
              0 自有资金挤占
            </span>
          </div>
        </div>
      </div>
    </div>
    """

    stat_banner = mo.Html(kpi_cards_html)
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
        stat_banner,
    )


@app.cell
def __(
    GOLD,
    GREY,
    NAVY,
    baoshen,
    base64,
    con,
    danfang,
    dropdown_zone,
    gangong,
    hetong,
    huisou,
    io,
    jiekuan,
    jinghui,
    mo,
    plt,
    shuijin,
    suoding,
    wuliao,
):
    # 构建 Tab 1: 全景商业研报（纯静态基准数据驱动，不依赖滑块推演变量，绝对不会因调参而重新计算白屏！）

    # 【图表 1 优化】：数字标注在环形外部，空间纯净通透，右侧设清晰图例
    _aud_rows = con.execute("SELECT * FROM v_hhg_settlement_audit_summary WHERE 造价构成项 NOT LIKE '%总额%' AND 造价构成项 NOT LIKE '%总造价%'").fetchall()
    _al = [r[0] for r in _aud_rows]
    _av = [float(r[1]) for r in _aud_rows]
    _fig1, _ax1 = plt.subplots(figsize=(7.5, 3.4), dpi=140)
    _wedges, _texts, _autotexts = _ax1.pie(
        _av,
        autopct='%1.1f%%',
        pctdistance=1.22,
        startangle=90,
        colors=[NAVY, '#607d8b', GOLD],
        wedgeprops=dict(width=0.38, edgecolor='white', linewidth=1.5),
        textprops=dict(fontsize=8.8, color='#1e293b', fontweight='bold')
    )
    # 数字标注精准落位在各扇区外圈，留白舒适
    _autotexts[0].set_position((0, -1.22))      # 90.5% 居于底部外侧
    _autotexts[1].set_position((0.72, 1.05))    # 3.1% 居于右上方外侧
    _autotexts[2].set_position((0.18, 1.25))    # 6.3% 居于正上方外侧

    _ax1.text(0, 0, f"送审合计\n{sum(_av):,.0f} 万", ha='center', va='center', fontsize=10.5, fontweight='bold', color=NAVY)
    _legend_labels = [f'{_l}: {_v:,.2f} 万' for _l, _v in zip(_al, _av)]
    _ax1.legend(_wedges, _legend_labels, title='造价分项构成明细', loc='center left', bbox_to_anchor=(1.12, 0.5), fontsize=8.5, frameon=False)
    _ax1.set_title('送审造价三大构成 · 直接物料占 90.5%', fontsize=11, fontweight='bold', pad=12)
    _fig1.subplots_adjust(left=0.08, right=0.62, top=0.88, bottom=0.1)
    _buf1 = io.BytesIO()
    _fig1.savefig(_buf1, format='svg', bbox_inches='tight')
    plt.close(_fig1)
    _buf1.seek(0)
    _chart1_b64 = base64.b64encode(_buf1.getvalue()).decode('utf-8')

    # 【图表 2 优化】：右侧拓展 xlim 至 2500，留足安全边距，确保“总包配合费 -150 万”绝不被裁剪
    _fig2, _ax2 = plt.subplots(figsize=(8.2, 3.2), dpi=140)
    _labels = ['业主借款', '年后回收产值', '扣总包配合费', '实际净落袋']
    _jk, _hs, _pf, _jh = float(jiekuan), float(huisou), 150.0, float(jinghui)
    _widths = [_jk, _hs, _pf, _jh]
    _bottoms = [0, 0, _jh, 0]
    _colors = [GOLD, NAVY, '#7b8899', '#059669']
    _bars = _ax2.barh(_labels, _widths, left=_bottoms, color=_colors, height=0.45, zorder=3)
    _ax2.text(_jk/2, 0, f'{_jk:,.0f} 万', va='center', ha='center', color='white', fontweight='bold', fontsize=8.5)
    _ax2.text(_hs/2, 1, f'{_hs:,.0f} 万', va='center', ha='center', color='white', fontweight='bold', fontsize=8.5)
    _ax2.text(_jh + _pf/2, 2, f'-{_pf:,.0f}', va='center', ha='center', color='white', fontsize=8)
    _ax2.text(_jh/2, 3, f'{_jh:,.0f} 万', va='center', ha='center', color='white', fontweight='bold', fontsize=8.5)
    _ax2.annotate('总包配合费 -150 万', xy=(_jh, 2), xytext=(_hs + 50, 2), color='#b04040', fontsize=8.5,
                  arrowprops=dict(arrowstyle='->', color='#b04040', lw=0.9))
    _ax2.set_xlim(0, 2550)
    _ax2.spines[['top','right']].set_visible(False)
    _ax2.grid(axis='x', color='#e8ecf0', lw=0.7, zorder=0); _ax2.set_axisbelow(True)
    _ax2.set_title('资金闭环 · 借款 1,000 万撬动整体交付，回收后扣配合费净落袋 1,850 万', fontsize=11, fontweight='bold', pad=10)
    _fig2.subplots_adjust(left=0.16, right=0.92, top=0.88, bottom=0.15)
    _buf2 = io.BytesIO()
    _fig2.savefig(_buf2, format='svg', bbox_inches='tight')
    plt.close(_fig2)
    _buf2.seek(0)
    _chart2_b64 = base64.b64encode(_buf2.getvalue()).decode('utf-8')

    # 【图表 3】: 品类大盘
    _cat = con.execute('SELECT * FROM v_hhg_category_summary').fetchall()
    _cn  = ['家具','灯饰','窗帘','艺术品','布艺','宴会专项','办公']
    _amt = [float(r[1]) for r in _cat]
    _order = sorted(range(len(_amt)), key=lambda idx: _amt[idx])
    _cn_s  = [_cn[idx] for idx in _order]
    _amt_s = [_amt[idx] for idx in _order]
    _tot   = sum(_amt_s)
    _fig3, _ax3 = plt.subplots(figsize=(7.8, 3.0), dpi=140)
    _bar_colors = [GOLD if c in ['家具','艺术品'] else '#7b8899' for c in _cn_s]
    _bars3 = _ax3.barh(_cn_s, _amt_s, color=_bar_colors, height=0.55, zorder=3)
    for _b, _v in zip(_bars3, _amt_s):
        _ax3.text(_v + 15, _b.get_y()+_b.get_height()/2, f'{_v:,.0f} 万 · {_v/_tot*100:.1f}%', va='center', ha='left', fontsize=8, color='#2c3e50')
    _ax3.set_title('七大品类送审贡献 · 家具+艺术品双引擎占 75%', fontsize=11, fontweight='bold', pad=10)
    _ax3.set_xlim(0, max(_amt_s)*1.25)
    _ax3.spines[['top','right']].set_visible(False)
    _ax3.grid(axis='x', color='#e8ecf0', lw=0.7, zorder=0); _ax3.set_axisbelow(True)
    _fig3.subplots_adjust(left=0.14, right=0.92, top=0.88, bottom=0.15)
    _buf3 = io.BytesIO()
    _fig3.savefig(_buf3, format='svg', bbox_inches='tight')
    plt.close(_fig3)
    _buf3.seek(0)
    _chart3_b64 = base64.b64encode(_buf3.getvalue()).decode('utf-8')

    # 【图表 4】: 空间动线 BOM
    _cur_zone = dropdown_zone.value
    _q = "SELECT * FROM v_hhg_zone_summary"
    if _cur_zone != "全部区域":
        _q += f" WHERE 所属分区 = '{_cur_zone}'"
    _zone = con.execute(_q).fetchall()
    _zl = [r[0] for r in _zone]
    _zv = [float(r[3])/10000 for r in _zone]
    _zsum = sum(_zv) if _zv else 1.0
    _fig4, _ax4 = plt.subplots(figsize=(7.8, 2.8), dpi=140)
    _ax4.bar(_zl, _zv, color=[NAVY, GOLD, GREY][:len(_zl)], width=0.45, zorder=3)
    for _i, (_l, _v) in enumerate(zip(_zl, _zv)):
        _ax4.text(_i, _v + (max(_zv)*0.03 if _zv else 10), f'{_v:,.2f} 万\n{_v/_zsum*100:.1f}%', ha='center', va='bottom', fontsize=8)
    if _zv:
        _ax4.set_ylim(0, max(_zv)*1.25)
    _ax4.set_ylabel('万元', fontsize=8.5)
    _ax4.set_title(f'区域 BOM 合价 · 当前过滤: {_cur_zone}', fontsize=11, fontweight='bold', pad=10)
    _ax4.spines[['top','right']].set_visible(False)
    _ax4.grid(axis='y', color='#e8ecf0', lw=0.7, zorder=0); _ax4.set_axisbelow(True)
    _fig4.subplots_adjust(left=0.14, right=0.92, top=0.88, bottom=0.15)
    _buf4 = io.BytesIO()
    _fig4.savefig(_buf4, format='svg', bbox_inches='tight')
    plt.close(_fig4)
    _buf4.seek(0)
    _chart4_b64 = base64.b64encode(_buf4.getvalue()).decode('utf-8')

    # 【图表 5】: 激光实测面积对比
    _ms = con.execute('SELECT * FROM v_hhg_measured_space_areas').fetchall()
    _ml = [r[0] for r in _ms]
    _orig = [float(r[2]) for r in _ms]
    _net = [float(r[4]) for r in _ms]
    _cut = [o-n for o,n in zip(_orig,_net)]
    _fig5, _ax5 = plt.subplots(figsize=(7.8, 3.0), dpi=140)
    _x = range(len(_ml)); _w = 0.36
    _ax5.bar([i-_w/2 for i in _x], _orig, _w, label='原始面积', color='#c9d6e0', zorder=3)
    _ax5.bar([i+_w/2 for i in _x], _net,  _w, label='审减后净面积', color=NAVY, zorder=3)
    for _i in _x:
        _ax5.text(_i-_w/2, _orig[_i]+40, f'{_orig[_i]:,.0f}', ha='center', fontsize=7, color=GREY)
        _ax5.text(_i+_w/2, _net[_i]+40,  f'{_net[_i]:,.0f}', ha='center', fontsize=7, color=NAVY)
        if _cut[_i] > 1:
            _ax5.annotate(f'-{_cut[_i]:,.0f}', xy=(_i+_w/2, _net[_i]), xytext=(_i+_w/2, _net[_i]/2),
                          ha='center', fontsize=7.2, color='#b04040',
                          arrowprops=dict(arrowstyle='->', color='#b04040', lw=0.8))
    _ax5.set_xticks(list(_x)); _ax5.set_xticklabels(_ml, fontsize=8)
    _ax5.set_ylabel('m²', fontsize=8.5); _ax5.set_ylim(0, max(_orig)*1.2)
    _ax5.set_title('各区域实测面积 vs 审减后净面积（m²）', fontsize=11, fontweight='bold', pad=10)
    _ax5.legend(fontsize=7.5, ncol=2); _ax5.spines[['top','right']].set_visible(False)
    _ax5.grid(axis='y', color='#e8ecf0', lw=0.7, zorder=0); _ax5.set_axisbelow(True)
    _fig5.subplots_adjust(left=0.14, right=0.92, top=0.88, bottom=0.15)
    _buf5 = io.BytesIO()
    _fig5.savefig(_buf5, format='svg', bbox_inches='tight')
    plt.close(_fig5)
    _buf5.seek(0)
    _chart5_b64 = base64.b64encode(_buf5.getvalue()).decode('utf-8')

    _kpi_table = f"""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
      <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
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
            <td style="padding: 10px 16px; color: #64748b;">造价报审</td>
            <td style="padding: 10px 16px; font-weight: 600;">报审送审总造价</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 700; color: #1f4e78;">{baoshen/1e4:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">初报敞口</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9; background: #fafafa;">
            <td style="padding: 10px 16px; color: #64748b;">审计定案</td>
            <td style="padding: 10px 16px; font-weight: 600;">最终认价锁定金额 (税前)</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 700; color: #c8a45d;">{suoding/1e4:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">审减率 34.65%</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 16px; color: #64748b;">送审构成</td>
            <td style="padding: 10px 16px; font-weight: 600;">直接软装物品清单合价</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; color: #334155;">{wuliao:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">物料占比 90.5%</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9; background: #fafafa;">
            <td style="padding: 10px 16px; color: #64748b;">专项配合</td>
            <td style="padding: 10px 16px; font-weight: 600;">现场赶工配合费 (7.00%) / 增值税金</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; color: #334155;">{gangong:,.2f} / {shuijin:,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">赶工费核定</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 16px; color: #64748b;">合约基准</td>
            <td style="padding: 10px 16px; font-weight: 600;">总承包暂定分包合同额</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; color: #334155;">{float(hetong):,.0f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#f1f5f9; color:#475569; padding:2px 8px; border-radius:4px; font-size:11px;">包干单方签约</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9; background: #fafafa;">
            <td style="padding: 10px 16px; color: #64748b;">启动杠杆</td>
            <td style="padding: 10px 16px; font-weight: 600;">业主年前无息借款 (垫资启动金)</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 600; color: #0284c7;">{float(jiekuan):,.0f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#e0f2fe; color:#0369a1; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">零沉淀撬动</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 16px; color: #64748b;">资金回收</td>
            <td style="padding: 10px 16px; font-weight: 600;">年后累计回收产值款 (扣借款前)</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 600; color: #1e40af;">{float(huisou):,.0f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#e0e7ff; color:#3730a3; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">产值兑现</span></td>
          </tr>
          <tr style="border-bottom: 1px solid #f1f5f9; background: #fafafa;">
            <td style="padding: 10px 16px; color: #64748b;">净回款落袋</td>
            <td style="padding: 10px 16px; font-weight: 600;">扣除总包配合费后实际净回款</td>
            <td style="padding: 10px 16px; text-align: right; font-family: monospace; font-weight: 700; color: #059669;">{float(jinghui):,.2f} 万元</td>
            <td style="padding: 10px 16px; text-align: center;"><span style="background:#d1fae5; color:#065f46; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600;">最终现金结余</span></td>
          </tr>
        </tbody>
      </table>
    </div>
    """

    _roles = [
     ('承揽与界面界定', '牵头承揽城南综合体五星级公区软装分包；厘清发包/总包/分包三级界面', f'签约暂定 {float(hetong):,.0f} 万元 · 报审单方 {danfang:,.2f} 元/㎡', '《专业分包合同原件》'),
     ('采销定价与增项锁定', '设立多轨阶梯防线留足调价弹性；追加现场增项锁定底盘', f'报审 {baoshen/1e4:,.2f} 万 → 锁定 {suoding/1e4:,.2f} 万（含 120 万增项）', '《送审第一册与认价单》'),
     ('业主借款破局', '直通城投签署千万元无息借款，自有资金零占用全额锁定春节排产', f'2017-01-03 签署无息借款 {float(jiekuan):,.0f} 万元', '《城投借款协议原件》'),
     ('回款闭环', '年后集中交验收回产值冲抵借款，扣除总包配合费实现充沛现金净落袋', f'回收 {float(huisou):,.0f} 万 · 净落袋 {float(jinghui):,.2f} 万元', '《收款统计与配合费单》'),
     ('结算审计核减', '针对扣减意见出具激光测绘底图捍卫计价面积；以 390 行 BOM 支撑平稳过审', '抗辩锁定 16,478 ㎡ 净面积 · 交付 14,950 件', '《激光测绘表与签收台账》'),
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
        mo.md("- **公建国资标杆承揽**：项目紧扣遵义南部城市综合体五星级格兰云天国际大酒店开业刚性节点，承揽公区 C/D 区 1-3 层室内软装专业工程。\n- **法定分包界面清晰**：发包人遵义红花岗城投，总包中建四局，专业分包按暂定 3,000 万元签约，包干面积 20,000 ㎡ 折合单方 **1,751.45 元/㎡** 送审申报。\n- **三大构成**：申报 3,502.90 万元中，直接物料 3,170.62 万元（占 90.5%），抢工赶工配合费 221.94 万元，税金 110.34 万元。"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{_chart1_b64}' alt='造价构成'></div>"),
        mo.md("---"),
        mo.md("## § 2 业主千万元借款破局与净回款闭环"),
        mo.md("- **0 自有资金挤占破局**：直通红花岗城投高层，于 **2017-01-03 签署 1,000 万元无息借款协议**，全额锁定春节前珠三角源头排产，自有运营资金零沉淀。\n- **集中冲抵与净现金结余**：年后收回进度产值款 **2,000 万元** 全额对冲还清借款；扣除总包 **150 万元** 管理配合费后，实现 **1,850.00 万元** 充沛现金净落袋。"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{_chart2_b64}' alt='资金闭环'></div>"),
        mo.md("---"),
        mo.md("## § 3 采销多轨博弈定价与品类资产配置"),
        mo.md("- **阶梯商务防线与利润蓄水池**：预留调价弹性空间，从容应对审计审减（审减率 34.65%）。\n- **增项抵补锁定核心底盘**：在认价底线 2,288.99 万元基础上，追加并锁定 **120.00 万元** 现场增项，将最终认价锁定在 **2,408.99 万元**。\n- **品类双引擎**：**家具（1,206 万元，占 38.0%）** 与 **艺术品（1,185 万元，占 37.4%）** 合计占大盘 75.4%。"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{_chart3_b64}' alt='品类大盘'></div>"),
        mo.md("---"),
        mo.md("## § 4 空间动线与区域 BOM 资产结构"),
        mo.md("- **空间功能价值分布**：\n  1. **公区公共空间（中庭挑空及连廊）**：BOM 合价 **2,739.98 万元（占 62.7%）**，含 96 万黄铜主雕、89 万通高原木浮雕及 83.86 万刺绣等重资产；\n  2. **D区（主大堂与全日餐厅）**：BOM 合价 **979.12 万元（占 22.4%）**；\n  3. **C区（千人宴会中心）**：BOM 合价 **653.85 万元（占 15.0%）**，集中配置 1,500 张高档宴会椅与 3,000 条椅套。"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{_chart4_b64}' alt='空间动线'></div>"),
        mo.md("---"),
        mo.md("## § 5 激光实测面积技术抗辩与量化核减"),
        mo.md("- **激光测绘抗辩**：扣减后厨与机房 4,756 ㎡，坚决抗辩捍卫真实装饰界面，锁定纯软装计价面积 **16,478.00 ㎡**，对应结算净单方 **1,461.95 元/㎡**。\n- **14,950 件(套) 原子级实物证据链**：390 行清单支撑全案平稳过审。"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{_chart5_b64}' alt='实测面积'></div>"),
        mo.md("---"),
        mo.md("## § 6 商业统筹复盘与主导履职核定"),
        mo.Html(_role_table)
    ])
    return tab1_content,


@app.cell
def __(baoshen, base64, io, mo, np, pd, plt, sim_rate):
    # 构建 Tab 2: 敏感度双变量多场景推演矩阵 (热力图 + 交互数据表)
    _rates = [25.0, 30.0, sim_rate, 38.0, 42.0]
    _adds  = [0.0, 60.0, 120.0, 180.0, 240.0]

    _matrix_data = []
    _grid = np.zeros((len(_rates), len(_adds)))
    for _i, _r in enumerate(_rates):
        _row = {'审减率(%)': f'{_r:.2f}%'}
        for _j, _a in enumerate(_adds):
            _lock = baoshen * (1.0 - _r/100.0) + _a * 10000.0
            _val_wan = _lock / 1e4
            _grid[_i, _j] = _val_wan
            _row[f'+{_a:.0f}万增项'] = f"{_val_wan:,.2f} 万"
        _matrix_data.append(_row)
    _matrix_df = pd.DataFrame(_matrix_data)

    _fig_sens, _ax_sens = plt.subplots(figsize=(7.6, 3.8), dpi=140)
    _im = _ax_sens.imshow(_grid, cmap='YlGnBu', aspect='auto')
    _ax_sens.set_xticks(range(len(_adds)))
    _ax_sens.set_yticks(range(len(_rates)))
    _ax_sens.set_xticklabels([f'+{_a:.0f}万增项' for _a in _adds], fontsize=9, fontweight='bold')
    _ax_sens.set_yticklabels([f'审减率 {_r:.2f}%' for _r in _rates], fontsize=9, fontweight='bold')
    _cbar = _fig_sens.colorbar(_im, _ax_sens, fraction=0.035, pad=0.04)
    _cbar.ax.set_ylabel('推演认价锁定 (万元)', fontsize=8.5)

    for _i in range(len(_rates)):
        for _j in range(len(_adds)):
            _val = _grid[_i, _j]
            _is_actual = (abs(_rates[_i] - 34.65) < 0.01 and _adds[_j] == 120.0)
            _txt_color = '#dc2626' if _is_actual else ('#ffffff' if _val > 2400 else '#0f172a')
            _prefix = '★实际: ' if _is_actual else ''
            _ax_sens.text(_j, _i, f'{_prefix}{_val:,.1f}', ha='center', va='center',
                          fontsize=8.5, fontweight='bold' if _is_actual else 'normal', color=_txt_color)

    _ax_sens.set_title('认价锁定敏感度矩阵推演 (当前推演审减率 vs 现场增项追加)', fontsize=11, fontweight='bold', pad=12)
    _fig_sens.subplots_adjust(left=0.15, right=0.92, top=0.88, bottom=0.15)
    _buf_sens = io.BytesIO()
    _fig_sens.savefig(_buf_sens, format='svg', bbox_inches='tight')
    plt.close(_fig_sens)
    _buf_sens.seek(0)
    _sens_b64 = base64.b64encode(_buf_sens.getvalue()).decode('utf-8')

    tab2_content = mo.vstack([
        mo.md("### 🎛️ 商业操盘敏感度双变量多场景推演矩阵"),
        mo.md("通过在不同审减压力（25%~42%）与增项追加能力（0~240万）之间的交叉矩阵推演，清晰证明：**2017年梁清波团队成功锁定的 120 万元现场增项，是冲抵审计重刀、保住 2,408.99 万元核心产值底线的最关键定海神针！**"),
        mo.Html(f"<div class='chart-svg-box'><img src='data:image/svg+xml;base64,{_sens_b64}' alt='敏感度热力图'></div>"),
        mo.md("#### 📊 场景推演量化对账表（万元）"),
        mo.ui.table(_matrix_df)
    ])
    return tab2_content,


@app.cell
def __(bom_df, mo):
    # 构建 Tab 3: 神仙技能 5: mo.ui.table (390 行原子级清单交互式穿透台)
    bom_table = mo.ui.table(
        bom_df,
        selection="single",
        page_size=10,
        label="🔍 390 行实物清单原子级交互数据库（支持全局关键字搜索、列排序、点选行穿透）"
    )
    return bom_table,


@app.cell
def __(bom_table, mo):
    # 选定某一行时，触发详情动态穿透卡片
    _selected = bom_table.value
    if _selected is not None and not _selected.empty:
        _row = _selected.iloc[0]
        _detail_card = f"""
        <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 14px 18px; margin-top: 14px;">
          <div style="font-weight: 700; color: #166534; font-size: 14px; margin-bottom: 6px;">
            📌 选中原子实物资产穿透详情：{_row['名称']} ({_row['编码']})
          </div>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 12.5px; color: #374151;">
            <div><strong>所属分区：</strong>{_row['分区']}</div>
            <div><strong>具体空间：</strong>{_row['空间位置']}</div>
            <div><strong>资产类别：</strong>{_row['类别']}</div>
            <div><strong>采购数量：</strong>{_row['数量']} {_row['单位']}</div>
            <div><strong>单价：</strong>¥{float(_row['单价_元']):,.2f}</div>
            <div><strong>合价：</strong><span style="color:#059669; font-weight:700;">¥{float(_row['合价_元']):,.2f}</span></div>
            <div style="grid-column: span 2;"><strong>工艺材质要求：</strong>{_row['材质要求']}</div>
          </div>
        </div>
        """
    else:
        _detail_card = """
        <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 12px; margin-top: 12px; font-size: 12px; color: #64748b; text-align: center;">
          💡 提示：在上方表格中任意点击选中某一行物料（例如搜索“餐椅”、“沙发”、“茶几”、“地毯”），此处将即时穿透显示该物品的材质工艺、空间落位与造价参数！
        </div>
        """

    tab3_content = mo.vstack([
        mo.md("### 🔍 390 行原子级软装实物资产交互透视台"),
        mo.md("本台账直连 DuckDB 湖仓 `v_hhg_atom_bom_items` 底账，涵盖遵义红花岗公区全部 14,950 件(套) 落地实物。您可在搜索框输入 **“餐椅”**、**“沙发”**、**“茶几”**、**“地毯”** 等快速检索："),
        bom_table,
        mo.Html(_detail_card)
    ])
    return tab3_content,


@app.cell
def __(mo):
    # 构建 Tab 4: 神仙技能 6: mo.accordion (法定审计原件与档案索引手风琴)
    tab4_content = mo.vstack([
        mo.md("### ⚖️ 法定审计原件与原始档案卷宗索引"),
        mo.md("全案事实严格遵照《审计法》与国资工程决算标准，实行完整实物与财务证据链归档："),
        mo.accordion({
            "📑 1. 合同与法律协议原件 (三级法定界面)": mo.md(
                """
                - **《遵义南部城市综合体五星级酒店公区软装专业分包合同》原件**：
                  - 合同编号：`PRJ-HHG-2016-SG-01`
                  - 签约三方：发包人遵义市红花岗区城投、总承包中建四局、专业分包深圳广田
                  - 核心条款：暂定金额 3,000 万元，包干单方计价
                - **《红花岗城市综合体 C/D 区 1-3 层公区年前软装抢工借款协议》**：
                  - 签署日期：**2017-01-03**
                  - 法律效力：遵义市红花岗区城投盖章生效，专款垫资 1,000 万元，无息使用
                """
            ),
            "📊 2. 财务决算与实物验收底账 (390 行 BOM)": mo.md(
                """
                - **《广田云软装结算计算稿》**：
                  - 送审盖章清单第一册原件，核准送审总造价 3,502.90 万元
                  - 390 行原子级清单，逐项核定直接物料合价 3,170.62 万元与认价记录
                - **《红花岗项目收款统计表》与对账凭证**：
                  - 年后累计收回 2,000 万元工程款银行回执
                  - 中建四局 150 万元总包配合费核销凭证，确认净落袋 1,850.00 万元
                """
            ),
            "📐 3. 激光实测测绘技术抗辩底图 (捍卫 16,478 ㎡)": mo.md(
                """
                - **《红花岗各区域激光实测测绘复核表》**：
                  - 原始建筑面积 22,706 ㎡
                  - 扣除后厨、配电房与管道机房 4,756 ㎡
                  - 成功捍卫并认定纯软装装饰净面积 **16,478.00 ㎡**
                - **14,950 件(套) 实物到场签收与移交清单**：
                  - 涵盖中庭挑空 96 万黄铜主雕、89 万原木浮雕、83.86 万刺绣与 1,500 张宴会椅的现场签收签字单
                """
            )
        })
    ])
    return tab4_content,


@app.cell
def __(mo, stat_banner, tab1_content, tab2_content, tab3_content, tab4_content):
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
        "🔍 390 行原子级清单透视": tab3_content,
        "⚖️ 法定审计档案索引": tab4_content,
    })

    main_view = mo.vstack([
        latex_style,
        mo.md(
            """
            # 遵义红花岗南部城市综合体商业统筹研报
            ### 梁清波 商业专案库 · 项目代号 PRJ-HHG-2016 · Marimo 旗舰版
            > **🏛️ 实证与技术架构说明**：
            > 本研报基于 Marimo 纯 Python 反应式 DAG 引擎驱动，所有指标与图表直连 DuckDB 湖仓。
            > **全案图表全面升级为原生无损矢量 SVG 架构**（任意放大无损、无模糊、高分屏视网膜级锐度）；**排版字体全面升级为典雅 LaTeX 学术出版衬线风格**。
            """
        ),
        stat_banner,
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
