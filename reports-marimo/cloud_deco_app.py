import marimo

__generated_with = "0.11.12"
app = marimo.App(width="full", app_title="广田云软装 · 全资子公司十年商业操盘与供应链大盘研报")


@app.cell
def load_libraries_and_init_db():
    import marimo as mo
    import io
    import json
    import duckdb
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 设置 Matplotlib 中文字体与矢量出版级样式 (转为 path 杜绝缺字)
    plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei", "Noto Sans CJK SC", "SimSun", "sans-serif"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.size"] = 10.5
    plt.rcParams["svg.fonttype"] = "path"
    plt.rcParams["mathtext.fontset"] = "cm"

    # 在内存中启动 DuckDB 并执行云软装官方视图群
    con = duckdb.connect(":memory:")
    sql_path = "/home/l/个人资料仓库/data/views_guangtian_cloud_master.sql"
    with open(sql_path, "r", encoding="utf-8") as f:
        con.execute(f.read())

    # 提取 24 大核心标杆工程
    contracts_df = con.execute("SELECT * FROM v_gt_contracts_master ORDER BY 序号 ASC").df()
    
    # 提取业态分布
    types_df = con.execute("SELECT * FROM v_gt_contracts_by_type").df()

    # 提取初创制度与组织编制
    hr_df = con.execute("SELECT * FROM v_gt_cloud_founding_hr").df()
    team_df = con.execute("SELECT * FROM v_gt_cloud_team_structure").df()

    # 提取 135 份全盘汇总
    portfolio_135_df = con.execute("SELECT * FROM v_gt_portfolio_all_135").df()

    # 提取四大回款模式与专班矩阵
    cashflow_df = con.execute("SELECT * FROM v_gt_cashflow_models").df()
    taskforce_df = con.execute("SELECT * FROM v_gt_taskforce_matrix").df()

    return (
        mo,
        io,
        json,
        duckdb,
        pd,
        np,
        plt,
        con,
        contracts_df,
        types_df,
        hr_df,
        team_df,
        portfolio_135_df,
        cashflow_df,
        taskforce_df,
    )


@app.cell
def build_executive_sidebar(mo):
    sidebar_content = mo.vstack([
        mo.md("""
### 🏛️ 高管档案与业务总览
*广田云软装 · 全资子公司十年专案典藏*

---

#### 🏢 实体法人背景
- **企业名称**：深圳市广田云软装科技有限公司
- **法定资质**：广田集团（SZ.002482）全资子公司
- **注册资本**：**3,000.00 万元**（超募资金实缴）
- **成立时间**：2014 年 2 月
- **总部基地**：深圳盛华大厦 / 罗湖艺展中心

---

#### 👤 梁清波 核心任职履历
- **全资子公司初创核心筹办人 (2014-2015)**：
  * 主持起草八大模块 **730 条** 刚性管理制度；
  * 从 0 到 1 组建 **45 人** 跨职系精干编制；
  * 打造罗湖艺展中心 **1,491 ㎡** 沉浸式美学展厅；
  * 实现劳动合同 100% 前置签署与十年跨度**零劳动仲裁**。
- **标杆工程敏捷专班牵头人 (2015-2024)**：
  * 亲自主操遵义大酒店 1.25 亿母盘、遵义湄江温泉 3,380 万、红花岗城市综合体 3,112.5 万、上海华泰售楼处 156.66 万、陆川九龙山庄 550 万等核心项目。

---

#### 📑 研报卷宗四大板块
1. 🏛️ 全景深度商业研报
2. 👥 初创架构与 730 条制度底细
3. 📑 24 大标杆工程与公司 135 份底账
4. ⚖️ 法定初创资质与审计卷宗索引
        """)
    ])

    sidebar_layout = mo.sidebar(sidebar_content)
    return (sidebar_layout,)


@app.cell
def render_sidebar(sidebar_layout):
    sidebar_layout
    return


@app.cell
def render_status_banner(mo):
    status_msg = (
        "<div style='background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #162a45; padding:10px 16px; border-radius:4px; font-size:13px; color:#1e293b; line-height:1.6;'>"
        "🏛️ <strong>深圳广田云软装科技有限公司 · 商业操盘与供应链大盘研报</strong> &nbsp;|&nbsp; "
        "<span style='color:#059669; font-weight:700;'>初创组织基石：45 人精干编制 · 八大模块 730 条管理制度</span> &nbsp;|&nbsp; "
        "<span style='color:#2563eb; font-weight:700;'>公司全盘工程底账：135 份合同 6.83 亿元（审定 5.92 亿元）</span>"
        "</div>"
    )
    status_banner = mo.Html(status_msg)
    return (status_banner,)


@app.cell
def compute_kpi_cards(mo):
    card_capital = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #162a45; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">全资子公司法定实缴注册资本</div>
        <div style="font-size:28px; font-weight:700; color:#0f172a; margin:8px 0 4px 0; font-family:'monospace',monospace;">3,000 <span style="font-size:15px; font-weight:500;">万元</span></div>
        <div style="font-size:12px; color:#162a45; font-weight:600;">深交所上市公司（SZ.002482）超募出资设立</div>
    </div>
    """

    card_governance = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #0f766e; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">初创组织编制与风控制度底座</div>
        <div style="font-size:28px; font-weight:700; color:#0f172a; margin:8px 0 4px 0; font-family:'monospace',monospace;">45 <span style="font-size:15px; font-weight:500;">人</span> / 730 <span style="font-size:15px; font-weight:500;">条</span></div>
        <div style="font-size:12px; color:#0f766e; font-weight:600;">八大模块管理制度 · 十年跨度零劳动仲裁</div>
    </div>
    """

    card_showroom = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #b45309; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">罗湖艺展中心美学展厅矩阵</div>
        <div style="font-size:28px; font-weight:700; color:#0f172a; margin:8px 0 4px 0; font-family:'monospace',monospace;">1,491 <span style="font-size:15px; font-weight:500;">㎡</span></div>
        <div style="font-size:12px; color:#b45309; font-weight:600;">8 大实景风格样板间 · 320+ 批次高端考察封样</div>
    </div>
    """

    card_platform_total = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #2563eb; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">企业平台十年全量盖章合同大盘</div>
        <div style="font-size:28px; font-weight:700; color:#0f172a; margin:8px 0 4px 0; font-family:'monospace',monospace;">135 <span style="font-size:15px; font-weight:500;">份</span> / 6.83 <span style="font-size:15px; font-weight:500;">亿</span></div>
        <div style="font-size:12px; color:#2563eb; font-weight:600;">审计锁定审定产值 5.92 亿元（企业平台底册）</div>
    </div>
    """

    cards_html = f"""
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:16px; margin:16px 0;">
        {card_capital}
        {card_governance}
        {card_showroom}
        {card_platform_total}
    </div>
    """
    kpi_cards_view = mo.Html(cards_html)
    return (kpi_cards_view,)


@app.cell
def render_static_svg_charts(
    plt,
    io,
    mo,
    contracts_df,
    types_df,
    hr_df,
    portfolio_135_df,
):
    palette_navy = "#162a45"
    palette_forest = "#3a6351"
    palette_gold = "#b38600"
    palette_slate = "#4a5568"
    palette_blue = "#2563eb"
    palette_amber = "#d97706"

    # -------------------------------------------------------------
    # 图 1：广田云软装 135 份合同全盘四大集群业态结构透视
    # -------------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(6.5, 3.8), dpi=200)
    clusters = portfolio_135_df["合同集群板块"].tolist()
    signed_vals = (portfolio_135_df["签约合同额_万元"] / 10000.0).tolist()
    audited_vals = (portfolio_135_df["审定产值_万元"] / 10000.0).tolist()
    c_counts = portfolio_135_df["合同份数"].tolist()

    x = range(len(clusters))
    width = 0.35
    b1 = ax1.bar([i - width/2 for i in x], signed_vals, width, label="签约金额 (亿元)", color=palette_navy, edgecolor="none")
    b2 = ax1.bar([i + width/2 for i in x], audited_vals, width, label="审定确权 (亿元)", color=palette_gold, edgecolor="none")

    for i, (val, cnt) in enumerate(zip(signed_vals, c_counts)):
        ax1.text(i - width/2, val + 0.08, f"{val:.2f}亿\n({cnt}份)", ha="center", va="bottom", fontsize=8.5, color=palette_navy, fontweight="bold")
    for i, val in enumerate(audited_vals):
        ax1.text(i + width/2, val + 0.08, f"{val:.2f}亿", ha="center", va="bottom", fontsize=8.5, color=palette_gold, fontweight="bold")

    ax1.set_title("广田云软装 135 份合同四大集群大盘结构透视 (企业平台底册)", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
    ax1.set_xticks(x)
    ax1.set_xticklabels(clusters, fontsize=8.5)
    ax1.set_ylabel("金额 (亿元)", fontsize=9.5)
    ax1.set_ylim(0, max(signed_vals) * 1.35)
    ax1.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    fig1.tight_layout()

    def clean_svg(svg_raw):
        import re
        s = re.sub(r"<\?xml[^>]*\?>", "", svg_raw)
        s = re.sub(r"<!DOCTYPE[^>]*>", "", s)
        def repl_svg(m):
            tag = m.group(0)
            tag = re.sub(r"""\s+width="[^"]*\"""", "", tag)
            tag = re.sub(r"""\s+height="[^"]*\"""", "", tag)
            tag = re.sub(r"""\s+style="[^"]*\"""", "", tag)
            return tag.replace("<svg", '<svg style="width:100%; max-width:100%; height:auto; display:block; margin:0 auto;" preserveAspectRatio="xMidYMid meet"')
        s = re.sub(r"<svg[^>]*>", repl_svg, s, count=1)
        return s.strip()

    buf1 = io.StringIO()
    fig1.savefig(buf1, format="svg", bbox_inches="tight")
    plt.close(fig1)
    svg_chart1 = clean_svg(buf1.getvalue())

    # -------------------------------------------------------------
    # 图 2：敏捷专班核心攻坚项目 vs 平台标杆工程签约与确权对比
    # -------------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(6.5, 3.8), dpi=200)
    top_projects = contracts_df.head(6).copy()
    proj_names = [p[:7] + "..." if len(p) > 7 else p for p in top_projects["项目名称"]]
    proj_signed = top_projects["合同金额_万元"].tolist()
    proj_audited = top_projects["审定金额_万元"].tolist()

    y = range(len(proj_names))
    height = 0.35
    ax2.barh([i + height/2 for i in y], proj_signed, height, label="签约金额 (万元)", color=palette_forest, edgecolor="none")
    ax2.barh([i - height/2 for i in y], proj_audited, height, label="审定确权 (万元)", color=palette_blue, edgecolor="none")

    for i, val in enumerate(proj_signed):
        ax2.text(val + 150, i + height/2, f"{val:,.0f}", ha="left", va="center", fontsize=8.5, color=palette_forest, fontweight="bold")
    for i, val in enumerate(proj_audited):
        ax2.text(val + 150, i - height/2, f"{val:,.0f}", ha="left", va="center", fontsize=8.5, color=palette_blue, fontweight="bold")

    ax2.set_title("核心标杆项目签约与审定金额对比 (Top 6)", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
    ax2.set_yticks(y)
    ax2.set_yticklabels(proj_names, fontsize=8.5)
    ax2.set_xlabel("金额 (万元)", fontsize=9.5)
    ax2.set_xlim(0, max(proj_signed) * 1.25)
    ax2.legend(loc="lower right", frameon=False, fontsize=8.5)
    ax2.grid(axis="x", linestyle="--", alpha=0.3)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.invert_yaxis()
    fig2.tight_layout()

    buf2 = io.StringIO()
    fig2.savefig(buf2, format="svg", bbox_inches="tight")
    plt.close(fig2)
    svg_chart2 = clean_svg(buf2.getvalue())

    # -------------------------------------------------------------
    # 图 3：初创 45 人跨职系团队编制与人效分布
    # -------------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(6.5, 3.8), dpi=200)
    departments = ["方案设计研发中心", "工程实施交付中心", "商务采销成本中心", "行政人事综合中心"]
    dept_counts = [18, 12, 8, 7]
    dept_pcts = [40.0, 26.7, 17.8, 15.5]
    colors_team = ["#1e3a8a", "#0d9488", "#b45309", "#475569"]

    wedges, texts = ax3.pie(
        dept_counts,
        labels=None,
        colors=colors_team,
        startangle=140,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    )

    for i, w in enumerate(wedges):
        ang = (w.theta2 - w.theta1) / 2.0 + w.theta1
        x_pos = 0.78 * np.cos(np.deg2rad(ang))
        y_pos = 0.78 * np.sin(np.deg2rad(ang))
        ax3.text(
            x_pos,
            y_pos,
            f"{dept_counts[i]}人\n({dept_pcts[i]:.1f}%)",
            ha="center",
            va="center",
            fontsize=8.5,
            color="#ffffff",
            fontweight="bold",
        )

    legend_labels = [f"{d}: {c}人 ({p}%)" for d, c, p in zip(departments, dept_counts, dept_pcts)]
    ax3.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(0.95, 0.5), frameon=False, fontsize=8.5)
    ax3.set_title("初创组织 45 人跨职系精干编制结构", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
    fig3.tight_layout()

    buf3 = io.StringIO()
    fig3.savefig(buf3, format="svg", bbox_inches="tight")
    plt.close(fig3)
    svg_chart3 = clean_svg(buf3.getvalue())

    # -------------------------------------------------------------
    # 图 4：八大管理制度 730 条刚性条款分布
    # -------------------------------------------------------------
    fig4, ax4 = plt.subplots(figsize=(6.5, 3.8), dpi=200)
    modules = hr_df["管理制度模块"].tolist()
    mod_clauses = hr_df["刚性条款数"].tolist()

    y_pos = range(len(modules))
    bars = ax4.barh(y_pos, mod_clauses, color="#334155", height=0.6, edgecolor="none")
    bars[0].set_color("#dc2626")  # 奖惩第一刚性模块红色高亮
    bars[1].set_color("#0d9488")

    for i, v in enumerate(mod_clauses):
        pct = (v / 730.0) * 100.0
        ax4.text(v + 4, i, f"{v}条 ({pct:.1f}%)", ha="left", va="center", fontsize=8.5, color="#1e293b", fontweight="bold")

    ax4.set_title("《广田云软装管理制度》八大模块 730 条刚性条款分布", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(modules, fontsize=8.5)
    ax4.set_xlabel("条款数量 (条)", fontsize=9.5)
    ax4.set_xlim(0, max(mod_clauses) * 1.25)
    ax4.grid(axis="x", linestyle="--", alpha=0.3)
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    ax4.invert_yaxis()
    fig4.tight_layout()

    buf4 = io.StringIO()
    fig4.savefig(buf4, format="svg", bbox_inches="tight")
    plt.close(fig4)
    svg_chart4 = clean_svg(buf4.getvalue())

    return (
        svg_chart1,
        svg_chart2,
        svg_chart3,
        svg_chart4,
    )


@app.cell
def render_main_monograph_tab(
    mo,
    svg_chart1,
    svg_chart2,
    svg_chart3,
    svg_chart4,
):
    monograph_text = f"""
### § 1 全资子公司从 0 到 1 初创奠基与组织架构 (2014.02 - 2015.02)

- **3,000 万超募落地与初创挂帅**：2014 年 2 月，深圳广田装饰集团（SZ.002482）董事会决议使用部分超募资金投资 3,000 万元设立深圳市广田云软装艺术科技有限公司。梁清波受命作为初创筹办核心负责人，从零搭建子公司组织架构；
- **45 人跨职系精干编制**：历时 6 个月组建起涵盖设计研发（18人）、工程驻场（12人）、商务采销（8人）、行政人事（7人）的 45 人专业团队，建立起全生命周期的专业梯队；
- **主笔《广田云软装制度》730 条刚性条款**：亲自主持编制八大模块 730 条制度条款，配套 28 类电子审批流与底薪提成双轨制；实现劳动合同 100% 前置签署，创造了**十年跨度零劳动争议、零劳动仲裁**的治理典范；
- **打造艺展中心 1,491 ㎡ 美学展厅**：主导罗湖艺展中心 1,491 ㎡ 高端软装美学展厅设计、装修与软装陈设，成为集团承接大宗工程与地产战采的核心封样基地。

<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(360px, 1fr)); gap:16px; margin:20px 0;">
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:6px; padding:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center; min-width:0; overflow:hidden;">
        {svg_chart3}
    </div>
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:6px; padding:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center; min-width:0; overflow:hidden;">
        {svg_chart4}
    </div>
</div>

---

### § 2 定制软装商务全流程实战与企业十年 135 份盖章合同大盘 (2015 - 2024)

- **广田云软装全周期业务大盘（企业平台底册）**：
  * 广田云软装科技作为集团全资子公司，十年间累计经办并沉淀 **135 份盖章合同**，累计签约额达 **6.83 亿元（68,348 万元）**，最终审计锁定审定产值 **5.92 亿元（59,215.5 万元）**；
  * 全盘涵盖**遵义三大破亿工程（3.37亿元）**、**全国五星级酒店及国宾馆群（2.35亿元）**、**海外重大公建与知名文旅胜地（6,472万元）**、**头部房企全国战采与高端商业（4,676万元）** 四大核心业务集群；
- **梁清波个人操盘角色与职责边界厘定**：
  * 梁清波历任全资子公司**初创核心筹办人 (2014-2015)** 与**重大标杆工程敏捷专班牵头人 (Task Force Lead, 2015-2024)**；
  * 亲自主操攻坚包括：**遵义大酒店（1.25亿母盘，中建四局专业分包）**、**遵义湄江温泉大酒店（3,380万，出厂回款覆盖率 144%）**、**红花岗南部城市综合体（3,112.5万，实测签证据实结算）**、**上海华泰售楼处（156.66万，一次性闭口竞标与零垫资风控）**、**广西陆川九龙山庄（550万，28天极限抢工）** 等核心标杆工程；
- **全流程业务能力贯通**：涵盖业务承接、清单核算、报价竞标、物料白皮书深化、佛山东莞工厂源头验厂验胚、现场放线交底、大宗货品成品保护至竣工验收审计确权全流程。

<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(360px, 1fr)); gap:16px; margin:20px 0;">
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:6px; padding:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center; min-width:0; overflow:hidden;">
        {svg_chart1}
    </div>
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:6px; padding:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center; min-width:0; overflow:hidden;">
        {svg_chart2}
    </div>
</div>

---

### § 3 四大资金回款模式与现金流护城河

- **1. 比例联动回款型（遵义大酒店 1.25 亿母盘）**：
  * 设立联动公式：`分包应收款 = 母公司实际收款 × [1500 ÷ 6000]`，将软装回款与母体土建回款刚性捆绑 25%，贴现利息共担，防范地方城投支付拖延；
- **2. 阶段节点进度型（湄江温泉 3,380 万 / 海南生态园 2,664 万）**：
  * 采用 `30%预付 + 50%到货进度（累计80%） + 15%竣工验收 + 5%质保金`，出货或到场即收回 80% 现金流，**超额覆盖出厂直接成本 140%~150%**，筑牢资金安全线；
- **3. 极速覆盖风控型（上海华泰售楼处 156.66 万 / 宾阳华美达 108.28 万）**：
  * 实行 `30%定金 + 40%排产出货前付清（累计70%~90%）`，产品离开珠三角工厂前即实现资金回正，真正实现零垫资交付；
- **4. 战采统筹协同型（恒大全国战采 3,250 万 / 中国奥园三大战采 225.65 万）**：
  * 集团总部框架协议锁定基准毛利率与阶梯让利，属地化项目分批供货、分段确权、流水式结算回款。

---

### § 4 大项目敏捷专班 (Task Force) 与端到端下沉实操

- **组织协同机制**：打破科层壁垒，抽调设计、造价、工程、采购精干人员组建敏捷专班，梁清波亲任专班牵头人；
- **设计深化与源头品控**：下沉一线解读硬装空间图纸，编制物料白皮书，亲赴东莞、顺德、佛山定制工厂进行白胚结构与面漆封样飞检；
- **现场交付穿插**：亲临施工一线放线交底，克服既有建筑结构倾斜公差、消防阻燃等级与垂直货梯运输瓶颈；
- **竣工审计确权答辩**：挂帅造价审计答辩，重构签证单与实测底账，在遵义大酒店成功实现 9,300 万元审定确权，守住项目核心利润底线！
"""
    tab1_content = mo.md(monograph_text)
    return (tab1_content,)


@app.cell
def render_hr_foundation_tab(
    mo,
    team_df,
    hr_df,
):
    # 组织编制表格
    team_table = mo.ui.table(
        team_df,
        page_size=5,
        label="👥 初创 45 人跨职系精干编制明细表"
    )

    # 制度条款表格
    hr_table = mo.ui.table(
        hr_df,
        page_size=8,
        label="📑 《广田云软装管理制度》八大模块 730 条刚性条款汇编"
    )

    tab2_content = mo.vstack([
        mo.md("""
### 👥 初创组织架构与八大制度 730 条刚性底细

梁清波作为广田云软装全资子公司初创核心筹办人，主持起草了八大模块共计 **730 条** 刚性管理制度，并搭建了涵盖 **45 人** 精干专业编制的跨职系组织架构。
该制度体系不仅确立了“底薪+项目提成”双轨激励机制，更在劳动合同签订、考勤工时、差旅报销与材料合规红线上建立了审计级防线，创造了**十年跨度零劳动争议、零劳动仲裁、零行政处罚**的卓越治理记录。
        """),
        mo.md("#### 1. 初创组织架构 45 人精干编制明细"),
        team_table,
        mo.md("---"),
        mo.md("#### 2. 《广田云软装管理制度》八大模块 730 条刚性风控条款"),
        hr_table,
    ])

    return (
        team_table,
        hr_table,
        tab2_content,
    )


@app.cell
def create_contracts_ui(
    mo,
    contracts_df,
):
    categories = ["全部业态", "遵义三大破亿超级工程", "全国五星级酒店及国宾馆群", "海外重大公建与知名文旅胜地", "头部房企全国战采与高端商业"]
    category_filter = mo.ui.dropdown(
        options=categories,
        value="全部业态",
        label="业态分类筛选"
    )

    contracts_table = mo.ui.table(
        contracts_df,
        page_size=10,
        selection="single",
        pagination=True,
        label="广田云软装 24 大核心标杆工程台账（支持点击单行穿透工程履约详情）"
    )

    return (
        categories,
        category_filter,
        contracts_table,
    )


@app.cell
def display_contracts_mart(
    mo,
    category_filter,
    contracts_table,
    contracts_df,
    portfolio_135_df,
):
    cat_val = category_filter.value
    if cat_val == "全部业态":
        filtered_contracts_df = contracts_df
    elif cat_val == "遵义三大破亿超级工程":
        filtered_contracts_df = contracts_df[contracts_df["序号"].isin([1, 2, 3])]
    elif cat_val == "全国五星级酒店及国宾馆群":
        filtered_contracts_df = contracts_df[contracts_df["序号"].isin([4, 5, 6, 8, 9, 12, 13, 14, 16, 17, 18, 20, 24])]
    elif cat_val == "海外重大公建与知名文旅胜地":
        filtered_contracts_df = contracts_df[contracts_df["序号"].isin([10, 11, 19])]
    else:
        filtered_contracts_df = contracts_df[contracts_df["序号"].isin([7, 15, 21, 22, 23])]

    # 捕获选中行
    selected_df = contracts_table.value
    if selected_df is not None and len(selected_df) > 0:
        target_row = selected_df.iloc[0]
    elif filtered_contracts_df is not None and len(filtered_contracts_df) > 0:
        target_row = filtered_contracts_df.iloc[0]
    else:
        target_row = contracts_df.iloc[0]

    # 判断是否为梁清波敏捷专班操盘项目
    liang_taskforce_projects = [
        "遵义大酒店软装工程",
        "贵州遵义市红花岗南部城市综合体软装工程",
        "遵义湄江温泉城大酒店软装工程",
        "上海华泰售楼处及样板房软装工程",
        "广西玉林陆川九龙山庄二期软装工程"
    ]
    is_taskforce = target_row['项目名称'] in liang_taskforce_projects
    role_badge = (
        "<span style='background:#dc2626; color:#fff; font-size:11px; padding:2px 8px; border-radius:4px; font-weight:700;'>★ 梁清波敏捷专班操盘工程</span>"
        if is_taskforce else
        "<span style='background:#2563eb; color:#fff; font-size:11px; padding:2px 8px; border-radius:4px; font-weight:600;'>🏢 广田云软装平台重大标杆</span>"
    )

    detail_card = f"""
    <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #162a45; border-radius:6px; padding:18px; margin-top:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:16px; font-weight:700; color:#0f172a;">📍 标杆工程穿透：{target_row['项目名称']}</span>
            <div>
                {role_badge}
                <span style="background:#e2e8f0; color:#475569; font-size:11px; padding:3px 8px; border-radius:4px; font-family:'monospace',monospace; margin-left:6px;">合同代号: {target_row['合同编号']}</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; font-size:13px; margin:12px 0;">
            <div><strong style="color:#64748b;">发包方/业主:</strong> {target_row['发包业主']}</div>
            <div><strong style="color:#64748b;">业态分类:</strong> {target_row['业态分类']}</div>
            <div><strong style="color:#64748b;">签约年份:</strong> {target_row['签约年份']} 年</div>
            <div><strong style="color:#64748b;">签约金额:</strong> <span style="color:#2563eb; font-weight:700; font-family:'monospace';">{target_row['合同金额_万元']:,.2f} 万元</span></div>
            <div><strong style="color:#64748b;">审定确权:</strong> <span style="color:#059669; font-weight:700; font-family:'monospace';">{target_row['审定金额_万元']:,.2f} 万元</span></div>
            <div><strong style="color:#64748b;">地理空间:</strong> {target_row['地理区域']}</div>
        </div>
        <div style="background:#ffffff; border:1px dashed #94a3b8; border-radius:4px; padding:10px 14px; font-size:12.5px; color:#334155; margin-top:8px;">
            <strong style="color:#b45309;">💰 核心资金结算机制与风控屏障:</strong> {target_row['付款核心机制']}
        </div>
    </div>
    """

    # 全盘 135 份四大集群透视表
    cluster_table = mo.ui.table(
        portfolio_135_df,
        page_size=5,
        label="📊 广田云软装平台全生命周期 135 份盖章合同四大集群透视表"
    )

    tab3_content = mo.vstack([
        mo.md("### 📑 24 大核心标杆工程与公司全盘 135 份盖章合同总盘穿透\n\n数据 100% 映射 DuckDB 湖仓 `v_gt_contracts_master` 与 `v_gt_portfolio_all_135`。覆盖从遵义三大破亿工程到全国五星酒店、文旅胜地与地产战采，支持按业态筛选并点击表格任意行穿透单项工程核算底账！明确打标区分**梁清波敏捷专班操盘工程**与**企业平台重大标杆**。"),
        category_filter,
        contracts_table,
        mo.Html(detail_card),
        mo.md("---"),
        mo.md("#### 🏢 广田云软装平台 135 份盖章合同四大集群汇总底册"),
        cluster_table,
    ])

    return (
        filtered_contracts_df,
        target_row,
        detail_card,
        cluster_table,
        tab3_content,
    )


@app.cell
def render_dossier_tab(mo):
    dossier_accordion = mo.accordion({
        "📜 1. 广田集团 3,000 万元超募资金设立全资子公司批文与工商底册": mo.md("""
- **设立背景**：2014 年 2 月，深圳广田装饰集团股份有限公司（SZ.002482）第四届董事会第十二次会议审议通过《关于使用部分超募资金投资设立全资子公司的议案》，以超募资金 3,000.00 万元出资设立深圳市广田软装艺术有限公司（后更名为广田云软装）；
- **法定代表人与任职**：梁清波作为全资子公司筹办与初创核心负责人，直接对接集团总裁办与证券事务部推进工商注册、验资审计与牌照封包；
- **经营范围刚性界定**：建筑软装工程设计与施工、室内装饰艺术品配饰研发、定制家具、布艺软包、地毯灯具采销与供应链管理。
"""),
        "📑 2. 《广田云软装管理制度》八大模块 730 条刚性条款汇编": mo.md("""
- **制度主笔人实证**：梁清波亲自主持起草《广田云软装公司管理制度全编》，分为八大模块共计 730 条刚性条款，配套 28 类电子审批流与 OA 协同中枢；
- **八大管理制度模块结构**：
  * **奖惩管理与合规红线**（145条，占比 19.86%）：确立材料假冒伪劣一票否决制、收受商业回扣一票否决；
  * **考勤与工时休假管理**（112条，占比 15.34%）：多地项目驻场打卡与工时指纹核验；
  * **培训与专业技能发展**（96条，占比 13.15%）：软装设计师梯队导师制、物料选样与施工放线交底标准；
  * **招聘与录用合规程序**（88条，占比 12.05%）：专业测评、背调与 100% 劳动合同前置签署；
  * **薪酬福利与绩效双轨制**（85条，占比 11.64%）：首年薪酬盘 513.6 万元，推行底薪+项目提成双轨制；
  * **绩效考核与评估机制**（78条，占比 10.68%）：绑定利润达成率、回款周期与客户满意度；
  * **行政资产与展厅物业**（68条，占比 9.32%）：规范艺展中心 1,491 ㎡ 美学展厅资产与盛华大厦总部维护；
  * **商务出差与报销标准**（58条，占比 7.95%）：精细化区域差旅与商务核销标准，行政费压降 14.2%。
"""),
        "👥 3. 45 人初创团队编制、劳动合同 100% 签署与十年零仲裁存证": mo.md("""
- **45 人跨职系组织架构**：
  * **方案设计与深化研发中心（18人，40.0%）**：软装空间解读、物料白皮书编制、艺术品配饰深化与 3D 表达；
  * **工程实施与驻场交付中心（12人，26.7%）**：现场放线交底、多工种交叉施工、大宗货品摆场保护；
  * **商务采销与成本核算中心（8人，17.8%）**：采销双轨比价、工厂裸价锁定、送审签证与认价答辩；
  * **行政人事与运营综合中心（7人，15.5%）**：制度宣贯考核、展厅运营与后勤保障；
- **十年零仲裁法律凭据**：初创第一年实现 45 人 100% 依法签署正式劳动合同、足额缴纳五险一金，2014 至 2024 十年历程中实现**零劳动争议、零劳动仲裁、零行政处罚**！
"""),
        "🏢 4. 艺展中心 1,491 ㎡ 美学展厅与盛华大厦总部资产巡检台账": mo.md("""
- **展厅空间定位**：选址深圳罗湖艺展中心三期核心区，租用并精装 1,491 ㎡ 高端软装美学展厅，作为全国地产商战采选样、高端五星级酒店业主封样接待的大本营；
- **全案实景资产**：展厅涵盖 8 大实景风格样板空间（新中式、现代轻奢、法式古典、东南亚度假、商务总裁室、艺术品长廊等），陈列定制家具、手工地毯、雕塑油画与智能灯饰；
- **运营管控闭环**：建立展厅入库货品一物一码巡检机制，接待全国顶级房企、国际酒店管理集团考察 320+ 批次，支撑起大盘 6.83 亿元业务承接源头！
"""),
        "⚖️ 5. 全盘 135 份盖章合同大盘与遵义三大破亿标杆工程审计确权原件卷宗": mo.md("""
- **135 份真实合同大盘**：涵盖签约合同 6.83 亿元（68,348 万元），锁定审定产值 5.92 亿元（59,215.5 万元）；
- **遵义三大破亿工程审计确权原件索引**：
  * **遵义大酒店软装工程**（GY-2018-YW-131）：合同金额 12,500.00 万元，审定金额 9,300.00 万元，遵义道桥建设集团发包，比例联动回款；
  * **汇川区汇川温泉康养城**（汇川城投2017合同）：合同金额 10,900.00 万元，审定金额 9,800.00 万元，汇川区城投发包；
  * **遵义开元名都大酒店**（开元名都2017合同）：合同金额 10,300.00 万元，审定金额 9,500.00 万元，遵义新区房开发包。
""")
    })

    tab4_content = mo.vstack([
        mo.md("### ⚖️ 法定初创资质、集团制度与审计卷宗索引\n\n本专案全盘事实严格对照《公司法》、《劳动合同法》与上市公司信息披露法定档案归档："),
        dossier_accordion
    ])

    return (
        dossier_accordion,
        tab4_content,
    )


@app.cell
def assemble_full_app(
    mo,
    status_banner,
    kpi_cards_view,
    tab1_content,
    tab2_content,
    tab3_content,
    tab4_content,
):
    latex_style = mo.Html("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

      body, .marimo-app, h1, h2, h3, h4, h5, h6, p, li, blockquote, div {
        font-family: "Latin Modern Roman", "Computer Modern Serif", "Noto Serif SC", "Source Han Serif SC", "SimSun", serif !important;
      }

      h1, h2, h3 {
        color: #0f172a !important;
        letter-spacing: -0.01em;
      }

      blockquote {
        border-left: 3px solid #162a45 !important;
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

      /* 强制所有图表具备 100% 容器自适应缩放与弹性伸缩 */
      *, *::before, *::after {
        box-sizing: border-box !important;
      }

      svg {
        max-width: 100% !important;
        height: auto !important;
        width: 100% !important;
        display: block !important;
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

      [data-radix-toast-viewport], ol[tabindex="-1"], li[role="status"], a[href*="marimo-team/marimo"], a[href*="marimo.io"] {
        display: none !important;
      }
    </style>
    """)

    header_html = """
    <div style="border-bottom:1px solid #e2e8f0; padding-bottom:16px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="background:#162a45; color:#fff; font-size:11px; padding:3px 8px; border-radius:4px; font-weight:600; letter-spacing:0.5px;">CAREER ARCHIVAL MONOGRAPH</span>
                <span style="color:#64748b; font-size:12px; margin-left:8px; font-family:'monospace';">GUANGTIAN-CLOUD-DECO-10Y-MASTER</span>
            </div>
            <div style="color:#64748b; font-size:12px;">梁清波 商业专案典藏录</div>
        </div>
        <h1 style="font-size:26px; font-weight:800; color:#0f172a; margin:12px 0 6px 0; font-family:'Noto Serif CJK SC',serif;">深圳市广田云软装科技全生命周期商业操盘与供应链大盘研报</h1>
        <div style="font-size:13.5px; color:#475569; line-height:1.6;">
            <strong>全资子公司从 0 到 1 组建奠基与企业平台 135 份合同 6.83 亿元全周期工程大盘</strong>：承接广田集团（SZ.002482）3,000 万元超募资金设立子公司，组建 45 人跨职系团队，主笔 730 条管理制度，打造 1,491 ㎡ 艺展中心展厅；平台统筹 135 份真实盖章合同（签约 6.83 亿 / 审定 5.92 亿），贯通遵义三大破亿工程、全国五星酒店集群、文旅胜地与地产战采！
        </div>
    </div>
    """

    main_tabs = mo.ui.tabs({
        "🏛️ 全景深度商业研报": tab1_content,
        "👥 初创组织架构与八大制度 730 条刚性底细": tab2_content,
        "📑 24 大标杆工程与公司 135 份合同底账": tab3_content,
        "⚖️ 法定初创资质与审计卷宗索引": tab4_content,
    })

    app_layout = mo.vstack([
        latex_style,
        mo.Html(header_html),
        status_banner,
        kpi_cards_view,
        main_tabs,
    ])
    return (app_layout,)


@app.cell
def render_main_view(app_layout):
    app_layout
    return


if __name__ == "__main__":
    app.run()
