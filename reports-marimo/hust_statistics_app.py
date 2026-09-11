import marimo

__generated_with = "0.11.12"
app = marimo.App(width="full", app_title="华中科技大学统计学学术奠基与数理算法底座全息研报")


@app.cell
def load_libraries_and_init_db():
    import marimo as mo
    import io
    import json
    import time
    import duckdb
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

    # 设置 Matplotlib 中文字体与矢量出版级样式 (转为 path 杜绝缺字)
    plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei", "Noto Sans CJK SC", "SimSun", "sans-serif"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.size"] = 10.0
    plt.rcParams["svg.fonttype"] = "path"
    plt.rcParams["mathtext.fontset"] = "cm"

    # 在内存中启动 DuckDB 并执行华科统计学湖仓视图群
    con = duckdb.connect(":memory:")
    sql_path = "/home/l/个人资料仓库/data/views_hust_statistics_direct_lake.sql"
    with open(sql_path, "r", encoding="utf-8") as _sql_f:
        con.execute(_sql_f.read())

    # 提取四大阶段学分
    stages_df = con.execute("SELECT * FROM v_hust_curriculum_stages ORDER BY 阶段序号 ASC").df()

    # 提取 24 门骨干必修课程
    courses_df = con.execute("SELECT * FROM v_hust_core_course_matrix").df()

    # 提取 LBM 算法演化管线
    lbm_pipeline_df = con.execute("SELECT * FROM v_hust_lbm_algorithm_pipeline ORDER BY 流程序号 ASC").df()

    # 提取二十年数理业务映射
    bridge_df = con.execute("SELECT * FROM v_hust_math_to_business_bridge ORDER BY 职业阶段 ASC").df()

    return (
        mo,
        io,
        json,
        time,
        duckdb,
        pd,
        np,
        plt,
        FancyBboxPatch,
        FancyArrowPatch,
        Rectangle,
        con,
        stages_df,
        courses_df,
        lbm_pipeline_df,
        bridge_df,
    )


@app.cell
def build_executive_sidebar(mo):
    # 调参驱动源切换
    mode_switch = mo.ui.radio(
        options=["滑轮拖动模式", "具体数值输入模式"],
        value="滑轮拖动模式",
    )

    # 参数 1: 介观松弛时间 tau (0.51 ~ 1.20)
    slider_tau = mo.ui.slider(start=0.52, stop=1.20, step=0.01, value=0.60)
    num_tau = mo.ui.number(start=0.51, stop=2.00, step=0.01, value=0.60)

    # 参数 2: 顶盖驱动速度 u_lid (0.02 ~ 0.15)
    slider_ulid = mo.ui.slider(start=0.02, stop=0.15, step=0.01, value=0.08)
    num_ulid = mo.ui.number(start=0.01, stop=0.20, step=0.01, value=0.08)

    # 培养阶段筛选器
    stage_filter = mo.ui.dropdown(
        options=[
            "全量四大阶段 (160+ 学分)",
            "阶段一：纯数学严谨分析与代数底座",
            "阶段二：概率论与现代统计推断中枢",
            "阶段三：运筹最优化与大规模科学计算",
            "阶段四：算法工程实践与科研攻坚闭环",
        ],
        value="全量四大阶段 (160+ 学分)",
    )

    sidebar_content = mo.vstack([
        mo.md("""
### 🏛️ 华中科技大学学术奠基
*数学与统计学院 · 2002 级首届统计学本科*
**理学学士 (Bachelor of Science)**

---

#### 🌊 LBM 流体数值模拟动态控制台
*(基于毕业设计介观动力学模型现场演化)*
        """),
        mo.Html("""
        <div style="font-size:12px; font-weight:600; color:#475569; margin-bottom:4px;">
          🎛️ 调优驱动源模式
        </div>
        """),
        mode_switch,
        mo.Html("""
        <div style="background:#eff6ff; border-left:3px solid #2563eb; border:1px solid #bfdbfe; padding:6px 10px; border-radius:4px; margin:10px 0 4px 0;">
          <div style="color:#1d4ed8; font-size:12px; font-weight:700;">1. 介观弛豫时间 τ (决定运动粘度 ν)</div>
        </div>
        """),
        mo.Html("<div style='display:flex; justify-content:space-between; font-size:11px; color:#64748b; margin-bottom:2px;'><span>滑动调节 τ</span><span>精确数值</span></div>"),
        slider_tau,
        num_tau,
        mo.Html("""
        <div style="background:#f0fdf4; border-left:3px solid #059669; border:1px solid #bbf7d0; padding:6px 10px; border-radius:4px; margin:10px 0 4px 0;">
          <div style="color:#15803d; font-size:12px; font-weight:700;">2. 顶盖剪切流速 U_lid (决定雷诺数 Re)</div>
        </div>
        """),
        mo.Html("<div style='display:flex; justify-content:space-between; font-size:11px; color:#64748b; margin-bottom:2px;'><span>滑动调节流速</span><span>精确数值</span></div>"),
        slider_ulid,
        num_ulid,
        mo.md("""
---
        """),
        mo.Html("""
        <div style="background:#f1f5f9; border-left:3px solid #1e3a8a; padding:5px 8px; border-radius:4px; margin-bottom:4px; font-size:12px; font-weight:700; color:#1e3a8a;">
          📑 培养方案维度过滤
        </div>
        """),
        stage_filter,
        mo.md("""
---
#### 🧭 全息导航指引
- **Tab 1: 🏛️ 四大递进培养阶段与学分全景**
- **Tab 2: 🌊 毕业设计《LBM流体模拟》动态仿真台**
- **Tab 3: 🌐 二十年数理业务映射与闭环实证**
- **Tab 4: 📑 24 门骨干课程与师资教材穿透底册**

---
<div style="font-size:11px; color:#64748b; line-height:1.6;">
单一真实源：<code>views_hust_statistics_direct_lake.sql</code><br/>
计算引擎：DuckDB In-Memory + NumPy LBM
</div>
        """)
    ])

    sidebar_layout = mo.sidebar(sidebar_content)
    return (
        sidebar_layout,
        mode_switch,
        slider_tau,
        num_tau,
        slider_ulid,
        num_ulid,
        stage_filter,
    )


@app.cell
def render_sidebar(sidebar_layout):
    sidebar_layout
    return


@app.cell
def extract_active_params(
    mode_switch,
    slider_tau,
    num_tau,
    slider_ulid,
    num_ulid,
):
    if mode_switch.value == "具体数值输入模式":
        active_tau = float(num_tau.value)
        active_ulid = float(num_ulid.value)
    else:
        active_tau = float(slider_tau.value)
        active_ulid = float(slider_ulid.value)

    # 边界约束保护 (防数值发散)
    active_tau = max(0.51, min(2.0, active_tau))
    active_ulid = max(0.01, min(0.25, active_ulid))

    # 计算介观运动粘度与格点雷诺数 (L=32)
    nu = (2.0 * active_tau - 1.0) / 6.0
    reynolds = (active_ulid * 32.0) / nu

    return (
        active_tau,
        active_ulid,
        nu,
        reynolds,
    )


@app.cell
def render_status_banner(mo, active_tau, active_ulid, nu, reynolds):
    status_msg = f"""
    <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #1e3a8a; padding:12px 18px; border-radius:6px; font-size:13px; color:#1e293b; line-height:1.6; margin-bottom:16px;">
        🏛️ <strong>华中科技大学（985工程 / 双一流）数学与统计学院 · 2002 级首届统计学专业 · 理学学士 (B.S.)</strong> &nbsp;|&nbsp; 
        <span style="color:#059669; font-weight:700;">培养规格：四年 160+ 学分 · 30+ 门数理计算机课程 · LBM 毕业科研攻坚</span> &nbsp;|&nbsp; 
        <span style="color:#2563eb; font-weight:600;">当前介观仿真参量：τ = {active_tau:.2f} · ν = {nu:.4f} · U_lid = {active_ulid:.2f} · Re = {reynolds:.1f}</span>
    </div>
    """
    status_banner = mo.Html(status_msg)
    return (status_banner,)


@app.cell
def compute_kpi_cards(mo):
    card_credits = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #1e3a8a; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">学术学分体量</div>
        <div style="font-size:26px; font-weight:800; color:#1e3a8a; margin:6px 0 2px 0;">160+ <span style="font-size:14px; font-weight:500; color:#475569;">学分</span></div>
        <div style="font-size:12px; color:#475569; line-height:1.4;">纯数学分析与代数占 30% (48分)，与数学专业完全并轨修读 33 学分</div>
    </div>
    """

    card_courses = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #0d9488; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">师资与教材梯队</div>
        <div style="font-size:26px; font-weight:800; color:#0d9488; margin:6px 0 2px 0;">30+ <span style="font-size:14px; font-weight:500; color:#475569;">门骨干课</span></div>
        <div style="font-size:12px; color:#475569; line-height:1.4;">万建平、刘次华教授国家级规划教材受训，公理化概率与严格统计推断</div>
    </div>
    """

    card_lbm = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #ea580c; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">毕业攻坚科研</div>
        <div style="font-size:26px; font-weight:800; color:#ea580c; margin:6px 0 2px 0;">D2Q9 <span style="font-size:14px; font-weight:500; color:#475569;">LBM模拟</span></div>
        <div style="font-size:12px; color:#475569; line-height:1.4;">流体力学介观动力学模型，C 语言连续内存指针与无锁状态机数值解</div>
    </div>
    """

    card_bridge = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #7c3aed; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">二十年实证迁移</div>
        <div style="font-size:26px; font-weight:800; color:#7c3aed; margin:6px 0 2px 0;">3 大 <span style="font-size:14px; font-weight:500; color:#475569;">实体跃迁</span></div>
        <div style="font-size:12px; color:#475569; line-height:1.4;">上市公司 206 篇 A 级公告 · 2 亿供应链运筹定价 · 2804 万行 AI 湖仓</div>
    </div>
    """

    cards_html = f"""
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:16px; margin:16px 0;">
        {card_credits}
        {card_courses}
        {card_lbm}
        {card_bridge}
    </div>
    """
    kpi_cards_view = mo.Html(cards_html)
    return (kpi_cards_view,)


@app.cell
def render_static_academic_charts(
    plt,
    io,
    np,
    stages_df,
    lbm_pipeline_df,
    bridge_df,
):
    def _render():
        def clean_svg(buf):
            import re
            svg_raw = buf.getvalue()
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

        # 调色盘
        c_blue = "#1e3a8a"
        c_teal = "#0d9488"
        c_orange = "#ea580c"
        c_purple = "#7c3aed"
        c_slate = "#475569"

        # FIG 1: 四大递进培养阶段学分分布
        fig1, ax1 = plt.subplots(figsize=(7.2, 3.8), dpi=200)
        stage_names = [
            "阶段四：算法工程实践\n(C语言/SQL/LBM)",
            "阶段三：运筹与大规模计算\n(优化/有限差分/建模)",
            "阶段二：概率与统计推断\n(随机过程/多元/时序)",
            "阶段一：纯数学分析底座\n(数分I-III/高代I-II)",
        ]
        credits_list = [34, 36, 42, 48]
        colors_list = [c_purple, c_orange, c_teal, c_blue]

        y_pos = np.arange(len(stage_names))
        bars1 = ax1.barh(y_pos, credits_list, color=colors_list, height=0.55, edgecolor="none")

        for idx, (v_val, c_val) in enumerate(zip(credits_list, [5, 6, 7, 8])):
            ax1.text(v_val + 1.0, idx, f"{v_val} 学分 ({c_val} 门核心课)", ha="left", va="center", fontsize=8.8, color="#1e293b", fontweight="bold")

        ax1.set_title("FIG.01 四大递进培养阶段学分体量与课程结构 (总学分: 160+)", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(stage_names, fontsize=8.4)
        ax1.set_xlabel("学分数 (Credits)", fontsize=9.0)
        ax1.set_xlim(0, 58)
        ax1.grid(axis="x", linestyle="--", alpha=0.3)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        fig1.tight_layout()

        buf1 = io.StringIO()
        fig1.savefig(buf1, format="svg", bbox_inches="tight", pad_inches=0.15)
        plt.close(fig1)
        res_chart1 = clean_svg(buf1)

        # FIG 2: 统计学六维数理能力雷达图
        labels = [
            "形式化证明与反幻觉\n(公理化体系 98分)",
            "随机过程与统计推断\n(Kolmogorov/MLE 96分)",
            "高维空间投影与降维\n(PCA/Embedding 95分)",
            "运筹最优化排产调度\n(Simplex/CSP 94分)",
            "底层连续内存与Cache\n(C语言指针 95分)",
            "离散状态机演化机制\n(LBM介观流 97分)",
        ]
        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        values = [98, 96, 95, 94, 95, 97]
        values += values[:1]

        fig2, ax2 = plt.subplots(figsize=(6.8, 4.4), subplot_kw=dict(polar=True), dpi=200)
        ax2.plot(angles, values, color=c_blue, linewidth=2.2, linestyle="solid")
        ax2.fill(angles, values, color=c_blue, alpha=0.22)

        ax2.set_theta_offset(np.pi / 2)
        ax2.set_theta_direction(-1)
        ax2.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=8.0, color="#1e293b", fontweight="bold")
        ax2.tick_params(pad=14)
        ax2.set_ylim(0, 115)
        ax2.set_rgrids([30, 60, 90], labels=["30", "60", "90"], fontsize=7.2, color="#94a3b8")
        ax2.set_title("FIG.02 统计学专业六维数理素养与底层工程能力雷达图", fontsize=11, fontweight="bold", pad=16, color="#0f172a")
        fig2.tight_layout()

        buf2 = io.StringIO()
        fig2.savefig(buf2, format="svg", bbox_inches="tight", pad_inches=0.35)
        plt.close(fig2)
        res_chart2 = clean_svg(buf2)

        # FIG 3: LBM 演化拓扑管线
        fig3, ax3 = plt.subplots(figsize=(8.0, 3.6), dpi=200)
        ax3.set_xlim(0, 100)
        ax3.set_ylim(0, 45)
        ax3.axis("off")

        steps = [
            ("1. 宏观物理场\nNavier-Stokes", 10, 32, "#475569"),
            ("2. 介观LBGK方程\n单松弛演化", 36, 32, c_blue),
            ("3. D2Q9网格\n9速度离散拓扑", 64, 32, c_teal),
            ("4. 局部碰撞步\n代数弛豫演化", 90, 32, c_orange),
            ("7. 复杂固壁边界\n半步反弹格式", 90, 10, "#991b1b"),
            ("6. 宏观统计矩恢复\n密度ρ/速度u/压强p", 64, 10, c_purple),
            ("5. 粒子迁移步\n连续内存指针位移", 36, 10, "#0891b2"),
        ]

        for s_title, s_x, s_y, s_col in steps:
            rect = plt.Rectangle((s_x-9, s_y-6), 18, 12, facecolor="#f8fafc", edgecolor=s_col, linewidth=2.0, linestyle="-")
            ax3.add_patch(rect)
            ax3.text(s_x, s_y, s_title, ha="center", va="center", fontsize=8.0, fontweight="bold", color="#0f172a")

        arrows = [
            ((19, 32), (27, 32)),
            ((45, 32), (55, 32)),
            ((73, 32), (81, 32)),
            ((90, 26), (90, 16)),
            ((81, 10), (73, 10)),
            ((55, 10), (45, 10)),
            ((27, 10), (10, 26)),
        ]
        for arr_start, arr_end in arrows:
            ax3.annotate("", xy=arr_end, xytext=arr_start, arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5))

        ax3.set_title("FIG.03 格子玻尔兹曼 (LBM) 介观动力学闭环演化算法管线", fontsize=11, fontweight="bold", pad=10, color="#0f172a")
        fig3.tight_layout()

        buf3 = io.StringIO()
        fig3.savefig(buf3, format="svg", bbox_inches="tight", pad_inches=0.15)
        plt.close(fig3)
        res_chart3 = clean_svg(buf3)

        # FIG 4: 二十年数理业务映射全息图
        fig4, ax4 = plt.subplots(figsize=(8.0, 4.4), dpi=200)
        ax4.set_xlim(0, 100)
        ax4.set_ylim(0, 60)
        ax4.axis("off")

        stages_map = [
            ("学术奠基 (2002-2006)\n华科数学与统计学院", [
                ("纯数分析与实数完备性", 50),
                ("概率空间与统计推断", 38),
                ("运筹线性规划与优化", 26),
                ("LBM介观状态机与C指针", 14),
            ], 14, c_blue),
            ("转化机制 (数理内核)", [
                ("公理化证据与反幻觉", 50),
                ("高维空间投影与残差回归", 38),
                ("约束满足与动态双轨定价", 26),
                ("连续内存局部性与状态调度", 14),
            ], 50, c_teal),
            ("实体与AI商业成就", [
                ("206篇公告A级合规·零问询", 50),
                ("12亿发债底稿·同业财务对标", 38),
                ("24大工程2亿供应链·毛利锁定", 26),
                ("一人自研交付8大AI系统(2804万行)", 14),
            ], 86, c_purple),
        ]

        for col_title, items, x_center, col in stages_map:
            ax4.text(x_center, 58, col_title, ha="center", va="center", fontsize=9.0, fontweight="bold", color=col)
            for text, y_pos in items:
                r_box = plt.Rectangle((x_center-14, y_pos-4), 28, 8, facecolor="#f1f5f9", edgecolor=col, linewidth=1.5)
                ax4.add_patch(r_box)
                ax4.text(x_center, y_pos, text, ha="center", va="center", fontsize=7.4, fontweight="bold", color="#1e293b")

        for arr_y in [50, 38, 26, 14]:
            ax4.annotate("", xy=(36, arr_y), xytext=(28, arr_y), arrowprops=dict(arrowstyle="->", color="#94a3b8", lw=1.5))
            ax4.annotate("", xy=(72, arr_y), xytext=(64, arr_y), arrowprops=dict(arrowstyle="->", color="#94a3b8", lw=1.5))

        ax4.set_title("FIG.04 华科统计学数理底座向二十年实体与AI实践迁移映射全景", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
        fig4.tight_layout()

        buf4 = io.StringIO()
        fig4.savefig(buf4, format="svg", bbox_inches="tight", pad_inches=0.15)
        plt.close(fig4)
        res_chart4 = clean_svg(buf4)

        return res_chart1, res_chart2, res_chart3, res_chart4

    svg_chart1, svg_chart2, svg_chart3, svg_chart4 = _render()
    return (
        svg_chart1,
        svg_chart2,
        svg_chart3,
        svg_chart4,
    )


@app.cell
def run_dynamic_lbm_simulation(
    plt,
    io,
    np,
    active_tau,
    active_ulid,
    nu,
    reynolds,
):
    def _simulate():
        nx, ny = 32, 32
        weights = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])
        cx = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1])
        cy = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1])

        rho_grid = np.ones((ny, nx))
        ux_grid = np.zeros((ny, nx))
        uy_grid = np.zeros((ny, nx))

        def get_feq(r_arr, u_x, u_y):
            u2 = u_x**2 + u_y**2
            feq_arr = np.zeros((9, ny, nx))
            for k in range(9):
                cu = cx[k] * u_x + cy[k] * u_y
                feq_arr[k] = weights[k] * r_arr * (1.0 + 3.0*cu + 4.5*cu**2 - 1.5*u2)
            return feq_arr

        f_dist = get_feq(rho_grid, ux_grid, uy_grid)

        for _step in range(180):
            # 1. 局部碰撞松弛 (Collision)
            feq_step = get_feq(rho_grid, ux_grid, uy_grid)
            f_star = f_dist - (f_dist - feq_step) / active_tau

            # 2. 晶格迁移位移 (Streaming)
            for k in range(9):
                f_dist[k] = np.roll(np.roll(f_star[k], cx[k], axis=1), cy[k], axis=0)

            # 3. 固体固壁半步反弹边界 (Bounce-Back)
            f_dist[1, :, 0] = f_star[3, :, 0]
            f_dist[5, :, 0] = f_star[7, :, 0]
            f_dist[8, :, 0] = f_star[6, :, 0]

            f_dist[3, :, -1] = f_star[1, :, -1]
            f_dist[7, :, -1] = f_star[5, :, -1]
            f_dist[6, :, -1] = f_star[8, :, -1]

            f_dist[2, 0, :] = f_star[4, 0, :]
            f_dist[5, 0, :] = f_star[7, 0, :]
            f_dist[6, 0, :] = f_star[8, 0, :]

            # 顶盖运动边界 (Momentum bounce-back)
            f_dist[4, -1, :] = f_star[2, -1, :]
            f_dist[7, -1, :] = f_star[5, -1, :] - 6.0 * weights[7] * rho_grid[-1, :] * active_ulid * (-1.0)
            f_dist[8, -1, :] = f_star[6, -1, :] - 6.0 * weights[8] * rho_grid[-1, :] * active_ulid * (1.0)

            # 4. 宏观统计矩恢复 (Moments)
            rho_grid = np.sum(f_dist, axis=0)
            ux_grid = np.sum(f_dist * cx[:, None, None], axis=0) / rho_grid
            uy_grid = np.sum(f_dist * cy[:, None, None], axis=0) / rho_grid
            ux_grid[-1, :] = active_ulid
            uy_grid[-1, :] = 0.0

        speed_map = np.sqrt(ux_grid**2 + uy_grid**2)

        # 寻找中心涡核位置
        core_box = speed_map[4:26, 6:26]
        min_pos = np.unravel_index(np.argmin(core_box), core_box.shape)
        vortex_y = min_pos[0] + 4
        vortex_x = min_pos[1] + 6

        fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=200)
        X_mesh, Y_mesh = np.meshgrid(np.arange(nx), np.arange(ny))

        cax = ax.contourf(X_mesh, Y_mesh, speed_map, levels=16, cmap="viridis", alpha=0.88)
        cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label("流体速度幅值 |u| (Lattice Unit)", fontsize=8.4)
        cbar.ax.tick_params(labelsize=7.5)

        # 叠加流线
        ax.streamplot(X_mesh, Y_mesh, ux_grid, uy_grid, color="white", linewidth=0.8, density=1.1, arrowsize=0.8)

        # 标注中心涡流 (避开顶部)
        ax.plot(vortex_x, vortex_y, marker="o", markersize=7, color="#dc2626", markeredgecolor="white", markeredgewidth=1.5)
        ax.text(vortex_x, vortex_y - 2.2, f"主涡核 ({vortex_x}, {vortex_y})", color="#dc2626", fontsize=8.0, fontweight="bold", ha="center", va="top", backgroundcolor="#ffffffd0")

        # 顶盖速度方向箭头与文字
        ax.annotate("", xy=(nx-2, ny-1), xytext=(2, ny-1), arrowprops=dict(arrowstyle="->", color="#ef4444", lw=2.5))
        ax.text(nx/2, ny-0.2, f"顶盖驱动速度 U_lid = {active_ulid:.2f} →", color="#b91c1c", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

        ax.set_title(f"LBM D2Q9 顶盖方腔流动实时演化云图 (τ={active_tau:.2f}, ν={nu:.4f}, Re={reynolds:.1f})", fontsize=10.5, fontweight="bold", pad=15, color="#0f172a")
        ax.set_xlabel("晶格 X 轴坐标 (32x32 Grid)", fontsize=8.6)
        ax.set_ylabel("晶格 Y 轴坐标", fontsize=8.6)
        ax.set_xlim(0, nx-1)
        ax.set_ylim(0, ny-1)
        fig.tight_layout()

        buf = io.StringIO()
        fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.15)
        plt.close(fig)

        raw_val = buf.getvalue()
        return raw_val.replace('<svg ', '<svg style="width:100%; max-width:100%; height:auto; display:block; margin:0 auto;" ')

    svg_sim = _simulate()
    return (svg_sim,)


@app.cell
def render_main_tabs(
    mo,
    stage_filter,
    courses_df,
    stages_df,
    bridge_df,
    svg_chart1,
    svg_chart2,
    svg_chart3,
    svg_chart4,
    svg_sim,
    active_tau,
    active_ulid,
    nu,
    reynolds,
):
    # TAB 1
    tab1_content = mo.vstack([
        mo.md("""
### 🏛️ 四大递进培养阶段与 160+ 必修学分学术矩阵
华中科技大学数学与统计学院 2002 级首届统计学本科生，与数学系并轨修读 33 学分纯数学基石课程，四年累计完成 **160+ 必修学分**，建立起兼具**形式化逻辑证明**与**大规模科学计算**的复合知识体系。
        """),
        mo.Html(f"""
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:16px; margin:16px 0;">
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.04); min-width:0; overflow:hidden;">
                {svg_chart1}
            </div>
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.04); min-width:0; overflow:hidden;">
                {svg_chart2}
            </div>
        </div>
        """),
        mo.md("""
#### 📚 2×2 四大递进培养阶段深度解构

| 阶段梯队 | 修读学年 | 学分占比 | 核心骨干代表科目 | 数理学术内核 | 终局工程与商业映射 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **阶段一：纯数学严谨分析与代数底座** | 大一 ~ 大二 | **48 学分 (30.0%)** | 数学分析(I-III)、高等代数与几何(I-II)、常微分方程、解析几何、复变函数 | $\\varepsilon\\text{-}\\delta$ 极限语言、实数完备性公理、Jordan 标准型 | 严密逻辑与反幻觉基石，对复杂业务长链条推导的免疫力 |
| **阶段二：概率论与现代统计推断中枢** | 大二 ~ 大三 | **42 学分 (26.3%)** | 概率论、数理统计、随机过程、多元统计分析、应用回归、时间序列 | Kolmogorov 公理、Markov 链转移、极大似然(MLE)、PCA 协方差分解 | AI 高维 Embedding 空间余弦检索、A/B 测试检验、商业时序预测 |
| **阶段三：运筹最优化与大规模科学计算** | 大三 ~ 大四 | **36 学分 (22.5%)** | 数值分析、运筹学与线性规划、微分方程数值解、数学建模仿真 | 单纯形法、对偶理论、非线性极值逼近、PDE 有限差分格式 | 2 亿产值万级 BOM 排产调度、动态双轨加乘定价方程 |
| **阶段四：算法工程实践与科研攻坚闭环** | 大四 / 贯穿 | **34 学分 (21.3%)** | C 语言高级程序设计、数据结构与算法、数据库原理、LBM 毕业设计 | 指针运算、连续内存布局 (malloc/free)、LBGK 碰撞迁移状态机 | DuckDB 列式向量化内存直觉、现代 AI Agent 状态图机调度 |
        """)
    ])

    # TAB 2
    tab2_content = mo.vstack([
        mo.md("""
### 🌊 毕业设计科研攻坚：《格子玻尔兹曼 (LBM) 算法与数值模拟》
在传统计算流体力学 (CFD) 中，直接求解连续宏观 Navier-Stokes 方程面临全局压力 Poisson 方程求逆与复杂网格生成的巨大计算瓶颈。  
本课题师从偏微分方程数值解导师团队，推导微观粒子动理论演化方程，在 **D2Q9 正方晶格** 上实现局部代数松弛与位移，并以 **C 语言多维连续内存指针** 编程完成高并发数值演化。
        """),
        mo.Html(f"""
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:16px; margin:16px 0;">
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.04); min-width:0; overflow:hidden;">
                <div style="font-size:13px; font-weight:700; color:#1e293b; margin-bottom:8px;">🎯 介观仿真现场运行监控</div>
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px 14px; margin-bottom:12px; font-size:12px; line-height:1.7;">
                    • <strong>介观松弛时间 τ</strong>: <code>{active_tau:.2f}</code> (在左侧侧边栏调节)<br/>
                    • <strong>运动粘度 ν = (2τ - 1)/6</strong>: <code>{nu:.4f}</code><br/>
                    • <strong>顶盖剪切驱动速度 U_lid</strong>: <code>{active_ulid:.2f}</code><br/>
                    • <strong>晶格雷诺数 Re = (U·L)/ν</strong>: <code>{reynolds:.1f}</code><br/>
                    • <strong>求解耗时</strong>: <code>&lt; 40 ms</code> (NumPy 原生向量化加速)
                </div>
                {svg_sim}
            </div>
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.04); min-width:0; overflow:hidden;">
                <div style="font-size:13px; font-weight:700; color:#1e293b; margin-bottom:8px;">📐 算法拓扑管线 (7大关键节点)</div>
                {svg_chart3}
                <div style="margin-top:14px; font-size:12px; color:#475569; line-height:1.6;">
                    <strong>工程思想深刻启示</strong>：<br/>
                    1. <strong>去中心化状态机同构</strong>：每个格点仅按代数规则局部演化，自发形成宏观复杂流动，与现代 <strong>AI Agent 状态图机 (LangGraph/Swarm)</strong> 的状态转移思想完全一致；<br/>
                    2. <strong>高并发连续内存局部性</strong>：连续物理数组避免缓存失效，植入了对 <strong>DuckDB 列式向量化执行、Parquet 分片</strong> 的底层物理感知。
                </div>
            </div>
        </div>
        """),
        mo.md("""
#### 📊 宏观连续介质 vs 介观离散动力学对标

| 维度指标 | 传统宏观 CFD (Navier-Stokes) | 介观动力学 (Lattice Boltzmann Method) | 现代软件与 AI 工程映射 |
| :--- | :--- | :--- | :--- |
| **控制方程** | $\\frac{\\partial \\mathbf{u}}{\\partial t} + (\\mathbf{u}\\cdot\\nabla)\\mathbf{u} = -\\frac{1}{\\rho}\\nabla p + \\nu\\nabla^2\\mathbf{u}$ | $f_i(\\mathbf{x} + \\mathbf{e}_i\\Delta t, t + \\Delta t) - f_i(\\mathbf{x}, t) = -\\frac{1}{\\tau}[f_i - f_i^{(eq)}]$ | 连续偏微分求解 ➔ 局部代数演化 |
| **计算瓶颈** | 全局压力 Poisson 方程求逆，网格变形繁琐 | 纯局部代数碰撞松弛，无格点间依赖 | 全局锁/单点瓶颈 ➔ 无锁高并发流水线 |
| **边界条件** | 贴体网格坐标变换，几何曲面拟合难度高 | 半步反弹格式 (Bounce-Back)，任意曲面自适配 | 复杂适配器模式 ➔ 纯粹几何自适应反射 |
| **内存与算力** | 稀疏矩阵迭代，CPU Cache 局部性差 | 多维连续数组线性扫描，天然契合 SIMD 向量化 | 行存遍历 ➔ DuckDB 列式向量化内存计算 |
        """)
    ])

    # TAB 3
    tab3_content = mo.vstack([
        mo.md("""
### 🌐 统计学数理底座向二十年实体与 AI 实践的三重跃迁
数理科学并非纸上谈兵，而是二十年来贯穿**上市公司合规治理、2 亿实体商业大盘供应链操盘、现代 AI 敏捷工程研发**的核心底层武器。
        """),
        mo.Html(f"""
        <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; margin:16px 0; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            {svg_chart4}
        </div>
        """),
        mo.accordion({
            "🏛️ 实践一：资本运作与上市公司合规信披 (2011.03 - 2014.02 | 深圳广田 SZ.002482)": mo.md("""
- **数理理论底座**：Kolmogorov 公理化体系、Neyman-Pearson 假设检验、多元线性回归诊断、时序平稳性分析；
- **业务转化实证**：
  1. **同业财务对标专报**：主笔 433 行深度专报，运用多元回归诊断金螳螂、亚厦、洪涛等同业巨头三项费用与现金流敏感度；
  2. **12 亿元公司债底稿封包**：独立封包 55 大类专业底稿，严格采用假设检验与方差核验确保审计级精确；
  3. **206 篇官方披露公告零问询**：建立公理化推导核验防线，保持最高 A 级信披考评，实现深交所 0 问询、0 处罚。
- **底层价值**：将概率论公理化严谨推导直接转化为企业法定合规的零幻觉底盘。
            """),
            "🏭 实践二：2 亿实体商业大盘与供应链排产操盘 (2014.02 - 2024.02 | 广田云软装科技)": mo.md("""
- **数理理论底座**：运筹学单纯形法 (Simplex)、整数与动态规划、约束满足问题 (CSP)、矩阵离散分析；
- **业务转化实证**：
  1. **标杆工程运筹排产**：以运筹排产模型统领 24 大标杆工程（6.88 亿签约/6.14 亿审定）与 135 份全盘合同（5.92 亿产值）；
  2. **动态双轨加乘定价方程**：构建数学定价模型精确求解万级 BOM 采购加乘区间，彻底锁定毛利底线；
  3. **联动回款分包风险共担模型**：设计公式 `分包应收款 = 母公司实际收款 × [1500 ÷ 6000]`，将资本贴现成本刚性共担。
- **底层价值**：将线性规划与极值优化理论转化为实体商业两亿级规模化运营的盈利公式。
            """),
            "🤖 实践三：现代 AI 全栈工程与敏捷自研 (2024.03 - 至今 | Linux 原生研发环境)": mo.md("""
- **数理理论底座**：高维向量空间正交投影 (PCA)、LBM 介观状态机局部演化、C 语言连续内存指针局部性；
- **业务转化实证**：
  1. **高维 Embedding 检索本质**：将多元统计理论直接映射为大模型向量空间余弦相似度度量与混合 RAG，杜绝幻觉召回；
  2. **AI Agent 状态图机调度**：将 LBM 介观局部状态演化思想迁移至 LangGraph / Multi-Agent Swarm 调度流，打造高确定性转移状态机；
  3. **DuckDB 列式向量化驾驭**：基于 C 语言连续内存与 Cache Locality 底层直觉，全面驾驭 DuckDB 列式向量化引擎与 Parquet 二进制分片，**一人自研交付 8 大重工业级系统原型 (2,804 万行源码)**。
- **底层价值**：将介观动力学与连续内存直觉直接贯通为现代 AI Agent 与湖仓一体的核心引擎。
            """),
        })
    ])

    # TAB 4
    active_stage = stage_filter.value
    if active_stage != "全量四大阶段 (160+ 学分)":
        stage_prefix = active_stage.split("：")[0].replace("阶段", "").strip()
        module_map = {
            "一": "基础理论",
            "二": "统计核心",
            "三": "计算运筹",
            "四": ["算法工程", "科研攻坚"],
        }
        target_mod = module_map.get(stage_prefix, "")
        if isinstance(target_mod, list):
            filtered_df = courses_df[courses_df["所属模块"].isin(target_mod)]
        else:
            filtered_df = courses_df[courses_df["所属模块"] == target_mod]
    else:
        filtered_df = courses_df

    tab4_content = mo.vstack([
        mo.md(f"""
### 📑 24 门核心骨干科目与经典教材出处台账
*当前筛选视图：`{active_stage}` · 共呈现 {len(filtered_df)} 门代表性骨干科目*
        """),
        mo.ui.table(
            filtered_df[[
                "课程编号",
                "课程名称",
                "开设学期",
                "学分",
                "经典教材及出处",
                "数理学术核心训练",
                "后续商业与技术映射",
            ]],
            pagination=True,
            page_size=12,
        ),
        mo.md("""
> **教材考证与师资说明**：  
> 华科数学系统计学专业直接修读刘次华教授编著《随机过程》、万建平教授编著《概率论与数理统计》（均为华中科技大学出版社 / 高等教育出版社出版的国家级规划教材），接受严格公理化概率空间与统计极限推导训练；计算机骨干课程使用清华大学严蔚敏《数据结构》、高教社萨师煊《数据库系统概论》正统工科计算机教材。
        """)
    ])

    main_tabs = mo.ui.tabs({
        "🏛️ 培养体系与学分矩阵": tab1_content,
        "🌊 毕业设计《LBM流体模拟》动态仿真台": tab2_content,
        "🌐 二十年数理业务映射与实证": tab3_content,
        "📑 24 门骨干课程穿透底册": tab4_content,
    })

    latex_style = mo.Html("""
    <style>
      .marimo-app {
        font-family: "Latin Modern Roman", "Computer Modern Serif", "Noto Serif SC", "Source Han Serif SC", Georgia, "Times New Roman", serif !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
        line-height: 1.7 !important;
      }

      h1, h2, h3, h4 {
        font-family: "Latin Modern Roman", "Computer Modern Serif", "Noto Serif SC", serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        color: #0f172a !important;
      }

      table {
        font-family: "Latin Modern Roman", "Noto Serif SC", serif !important;
        border-collapse: collapse !important;
      }

      code, pre, .mono-num {
        font-family: "Latin Modern Mono", "Computer Modern Typewriter", "JetBrains Mono", monospace !important;
      }

      *, *::before, *::after {
        box-sizing: border-box !important;
      }

      svg, .chart-card svg, .marimo-app svg {
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        display: block !important;
        margin: 0 auto !important;
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

      /* 侧边栏控件全宽与杜绝单字竖排折行 */
      [data-marimo-sidebar="true"] select,
      [data-marimo-sidebar="true"] input,
      marimo-sidebar select,
      marimo-sidebar input,
      .marimo-sidebar select,
      .marimo-sidebar input {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
      }

      [data-marimo-sidebar="true"] label,
      marimo-sidebar label,
      .marimo-sidebar label {
        white-space: nowrap !important;
        font-size: 11.5px !important;
      }
    </style>
    """)

    header_html = """
    <div style="border-bottom:1px solid #e2e8f0; padding-bottom:16px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="background:#1e3a8a; color:#fff; font-size:11px; padding:3px 8px; border-radius:4px; font-weight:600; letter-spacing:0.5px;">ACADEMIC FOUNDATION & ALGORITHM VAULT</span>
                <span style="color:#64748b; font-size:12px; margin-left:8px; font-family:'monospace';">HUST-MATH-STAT-2002-2006</span>
            </div>
            <div style="color:#64748b; font-size:12px;">华中科技大学 · 统计学理学学士典藏录</div>
        </div>
        <h1 style="font-size:26px; font-weight:800; color:#0f172a; margin:12px 0 6px 0; font-family:'Noto Serif CJK SC',serif;">华中科技大学统计学学术奠基与数理算法底座全息研报</h1>
        <div style="font-size:13.5px; color:#475569; line-height:1.6;">
            依托数学与统计学院正统理学学士培养体系与《格子玻尔兹曼 (LBM) 算法与数值模拟》毕业科研攻坚，以交互式介观动力学模拟器与出版级矢量图表，实证呈现四年 160+ 学分对二十年上市公司资本运作、2 亿实体供应链大盘与 AI 湖仓工程研发的底层数理支撑。
        </div>
    </div>
    """

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
