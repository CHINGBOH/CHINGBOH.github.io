# -*- coding: utf-8 -*-
import marimo

__generated_with = "0.11.12"
app = marimo.App(width="full", app_title="BOONE LIANG / 梁清波 · 实证商业操盘与个人履历全息总谱 (Marimo 旗舰版)")


@app.cell
def load_lakehouse_and_styles():
    import marimo as mo
    import io
    import base64
    import duckdb
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 字体与防乱码基准配置 (出版级矢量路径)
    plt.rcParams["font.sans-serif"] = [
        "WenQuanYi Zen Hei",
        "Noto Serif CJK SC",
        "Noto Sans CJK SC",
        "DejaVu Sans",
        "SimSun",
        "sans-serif",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.size"] = 10.0
    plt.rcParams["svg.fonttype"] = "path"

    # 经典商业配色 (Quiet Luxury 配色规范)
    NAVY = "#162a45"
    BRONZE = "#8a6839"
    GOLD = "#c8a45d"
    SLATE = "#475569"
    BG_CREAM = "#faf8f5"
    BORDER_HAIR = "rgba(22, 42, 69, 0.12)"

    # 在内存中启动 DuckDB 并执行四大垂直官方湖仓视图群 (100% 单一真实源)
    con = duckdb.connect(":memory:")
    sql_files = [
        "/home/l/个人资料仓库/data/views_hust_statistics_direct_lake.sql",
        "/home/l/个人资料仓库/data/views_board_and_gm_direct_lake.sql",
        "/home/l/个人资料仓库/data/views_guangtian_cloud_master.sql",
        "/home/l/个人资料仓库/data/views_ai_engineering_direct_lake.sql"
    ]
    for sql_p in sql_files:
        with open(sql_p, "r", encoding="utf-8") as _f:
            con.execute(_f.read())

    return (
        mo,
        io,
        base64,
        duckdb,
        pd,
        np,
        matplotlib,
        plt,
        NAVY,
        BRONZE,
        GOLD,
        SLATE,
        BG_CREAM,
        BORDER_HAIR,
        con,
    )


@app.cell
def setup_sidebar_controls(mo, NAVY, BRONZE, BG_CREAM):
    # 侧边栏控制器定义
    career_stage_radio = mo.ui.radio(
        options=[
            "全景总览 (2002 - 2026)",
            "🎓 华科统计学学术奠基 (2002-2006)",
            "🏛️ 上市公司董办与总经办 (2011-2014)",
            "🏢 广田云实体采销大盘 (2014-2024)",
            "💻 现代自主AI湖仓工程 (2024-至今)",
        ],
        value="全景总览 (2002 - 2026)",
        label="生涯全景阶段导航",
    )

    sidebar_panel = mo.sidebar(
        [
            mo.md(
                f"""
                <div style="padding: 12px 0 14px 0; border-bottom: 1px solid rgba(22,42,69,0.12); margin-bottom: 14px;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: {BRONZE}; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 700; margin-bottom: 4px;">
                        EXECUTIVE DOSSIER · MASTER BI
                    </div>
                    <div style="font-size: 20px; font-weight: 900; color: {NAVY}; display: flex; align-items: baseline; gap: 8px;">
                        梁清波 <span style="font-size: 13px; font-weight: 500; color: #64748b; font-style: italic;">Boone Liang</span>
                    </div>
                    <div style="font-size: 11.5px; color: #475569; margin-top: 5px; line-height: 1.5;">
                        华中科技大学统计学理学学士<br>
                        实证商业操盘 · 上市公司合规 · 现代自研工程
                    </div>
                </div>
                """
            ),
            mo.md("#### 🧭 生涯阶段直达"),
            career_stage_radio,
            mo.md("<hr style='margin: 14px 0; border: none; border-top: 1px dashed rgba(22,42,69,0.15);'>"),
            mo.md("#### 🎯 四大核心价值支柱索引"),
            mo.md(
                f"""
                <div style="background: {BG_CREAM}; border: 1px solid rgba(138,104,57,0.2); border-radius: 4px; padding: 10px 12px; margin-bottom: 12px; font-size: 11.5px; line-height: 1.6; color: #334155;">
                    <div style="margin-bottom: 6px;">
                        <strong style="color: {BRONZE};">① 成本穿透</strong> (2014-2024)<br>
                        <span style="color: {NAVY}; font-weight: 600;">成本穿透与利润造血</span> · 守住 30%~35% 毛利
                    </div>
                    <div style="margin-bottom: 6px;">
                        <strong style="color: {BRONZE};">② 过程风控</strong> (2014-2024)<br>
                        <span style="color: {NAVY}; font-weight: 600;">过程风控与确权回款</span> · 签证审计闭环
                    </div>
                    <div style="margin-bottom: 6px;">
                        <strong style="color: {BRONZE};">③ 顶层治理</strong> (2011-2014)<br>
                        <span style="color: {NAVY}; font-weight: 600;">顶层治理与合规底盘</span> · 206篇A级信披/12亿债
                    </div>
                    <div>
                        <strong style="color: {BRONZE};">④ 数字化杠杆</strong> (2024-至今)<br>
                        <span style="color: {NAVY}; font-weight: 600;">数字化自主构建杠杆</span> · DuckDB湖仓/2800万行
                    </div>
                </div>
                """
            ),
            mo.md("<hr style='margin: 14px 0; border: none; border-top: 1px dashed rgba(22,42,69,0.15);'>"),
            mo.md("#### 🏛️ 审计级湖仓单一真实源"),
            mo.md(
                f"""
                <div style="font-size: 11px; color: #64748b; line-height: 1.6;">
                    全量数据直连本地 DuckDB Direct-Lake <strong>37 个物理湖仓视图</strong>，弃用 YAML 中间层，100% 物理可查验。
                </div>
                """
            ),
            mo.md("<hr style='margin: 14px 0; border: none; border-top: 1px dashed rgba(22,42,69,0.15);'>"),
            mo.md("#### 📞 主官直接联络"),
            mo.md(
                f"""
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: #334155; line-height: 1.8;">
                    📱 <strong>130-7787-2618</strong><br>
                    ✉️ <a href="mailto:kinpual@foxmail.com" style="color: {NAVY}; text-decoration: none; font-weight: 600;">kinpual@foxmail.com</a><br>
                    📍 中国 · 深圳
                </div>
                """
            ),
        ]
    )
    return career_stage_radio, sidebar_panel


@app.cell
def render_sidebar(sidebar_panel):
    sidebar_panel
    return


@app.cell
def render_hero_frontispiece(mo, NAVY, BRONZE, BG_CREAM, BORDER_HAIR):
    # 典藏级超级大扉页 (Grand Frontispiece & 4-Pillar Spec Grid)
    hero_frontispiece = mo.md(
        f"""
        <style>
          *, *::before, *::after {{
            box-sizing: border-box !important;
          }}
          svg {{
            width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
            display: block !important;
          }}
          img {{
            max-width: 100% !important;
            height: auto !important;
          }}
          [style*="display:grid"], [style*="display: grid"], [style*="display:flex"], [style*="display: flex"] {{
            box-sizing: border-box !important;
            max-width: 100% !important;
          }}
          [style*="display:grid"] > div, [style*="display: grid"] > div, [style*="display:flex"] > div, [style*="display: flex"] > div {{
            min-width: 0 !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
          }}
          [data-radix-toast-viewport], ol[tabindex="-1"], li[role="status"], a[href*="marimo-team/marimo"], a[href*="marimo.io"] {{
            display: none !important;
          }}
        </style>
        <div style="border-bottom: 1px solid {BORDER_HAIR}; padding-bottom: 24px; margin-bottom: 24px;">
            <!-- 档案题眉 -->
            <div style="display: flex; justify-content: space-between; align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: {BRONZE}; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 10px;">
                <span>BOONE LIANG / PROFESSIONAL PORTFOLIO / SELECTED WORK</span>
                <span>ARCHIVAL DOSSIER · MASTER BI</span>
            </div>

            <!-- 主官抬头与联系信息 -->
            <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 12px; margin-bottom: 12px;">
                <div style="display: flex; align-items: baseline; gap: 12px;">
                    <h1 style="font-size: 32px; font-weight: 900; color: {NAVY}; margin: 0; line-height: 1.2;">
                        梁清波 <span style="font-family: 'EB Garamond', serif; font-size: 20px; font-weight: 500; color: #64748b; font-style: italic;">Boone Liang</span>
                    </h1>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #475569; display: flex; gap: 14px; flex-wrap: wrap;">
                    <span>♂ 男</span>
                    <span>📍 中国 · 深圳</span>
                    <span>📱 130-7787-2618</span>
                    <span>✉️ <a href="mailto:kinpual@foxmail.com" style="color: inherit; text-decoration: none;">kinpual@foxmail.com</a></span>
                </div>
            </div>

            <!-- 定位标签 -->
            <div style="margin-bottom: 14px;">
                <span style="display: inline-block; font-family: 'Noto Serif SC', serif; font-size: 14.5px; font-weight: 700; color: {NAVY}; background: rgba(22, 42, 69, 0.04); border: 1px solid rgba(22, 42, 69, 0.15); padding: 4px 14px; border-radius: 4px; letter-spacing: 0.04em;">
                    [ 实证商业操盘 · 上市公司合规底盘 · 现代数字化自研工程 ]
                </span>
            </div>

            <!-- 核心公理论纲 (Executive Thesis) -->
            <div style="font-size: 14px; font-weight: 500; color: #1e293b; line-height: 1.85; background: #ffffff; border: 1px solid {BORDER_HAIR}; border-left: 4px solid {BRONZE}; padding: 16px 20px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); text-align: justify; margin-bottom: 18px;">
                华中科技大学统计学理学学士。二十年职业经历坚持一条原则：<strong>在不确定的商业环境中，以严密的数理逻辑与确凿的实证证据，构建确定性的商业结果。</strong>早年历练于广田股份（SZ.002482）总经办与董办，执笔 206 篇法定公告（深交所 A 级考评 0 问询），深度参与 12 亿公司债发债尽调，具备扎实的合规风控与资本视野；深耕工程软装与供应链采销十余年，主导 135 份供货合同、签约逾 6.8 亿元，精通源头成本穿透、多轨报价测算、过程签证闭环与结算审计确权，在复杂现场严守利润并兑现回款；近年将数理功底与业务经验全面数字化，自主研发 DuckDB 湖仓分析体系与自动化提效工具，兼具战略高度理解力、地面穿透执行力与代码级系统构建能力。
            </div>

            <!-- 四大核心价值兑现支柱 (4-Pillar Spec Grid) -->
            <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 14px;">
                <!-- ① 成本穿透 -->
                <div style="background: {BG_CREAM}; border: 1px solid {BORDER_HAIR}; border-top: 3px solid {BRONZE}; border-radius: 4px; padding: 14px 16px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-bottom: 6px;">
                            <span style="font-weight: 700; color: {BRONZE};">① 成本穿透</span>
                            <span style="color: #64748b;">2014-2024</span>
                        </div>
                        <div style="font-size: 14.5px; font-weight: 700; color: {NAVY}; margin-bottom: 6px;">成本穿透与利润造血<br><span style="font-size: 12px; font-weight: normal; color: #64748b;">(Profitability)</span></div>
                        <div style="font-size: 12.5px; color: #334155; line-height: 1.6; margin-bottom: 10px;">
                            拒绝拍脑袋报价与模糊预估。基于数理精算穿透非标供应链源头工坊底牌，建立“成本→内控→底限→报价”多轨动态防线，在激烈竞标中守住 30%~35% 的真实毛利。
                        </div>
                    </div>
                    <div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: {BRONZE}; background: #ffffff; padding: 5px 8px; border: 1px dashed rgba(138,104,57,0.3); border-radius: 2px; margin-bottom: 8px;">
                            源头成本底盘 · 多轨报价 · 价值工程 · 毛利防线
                        </div>
                        <a href="/monographs/marimo_cloud_deco.html" target="_blank" style="display: inline-block; font-size: 12px; font-weight: 700; color: {NAVY}; text-decoration: none;">
                            [ 查看专案 → ]
                        </a>
                    </div>
                </div>

                <!-- ② 过程风控 -->
                <div style="background: {BG_CREAM}; border: 1px solid {BORDER_HAIR}; border-top: 3px solid {BRONZE}; border-radius: 4px; padding: 14px 16px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-bottom: 6px;">
                            <span style="font-weight: 700; color: {BRONZE};">② 过程风控</span>
                            <span style="color: #64748b;">2014-2024</span>
                        </div>
                        <div style="font-size: 14.5px; font-weight: 700; color: {NAVY}; margin-bottom: 6px;">过程风控与确权回款<br><span style="font-size: 12px; font-weight: normal; color: #64748b;">(Assurance)</span></div>
                        <div style="font-size: 12.5px; color: #334155; line-height: 1.6; margin-bottom: 10px;">
                            懂人性，懂现场扯皮，更懂法律与审计。从合同条款拟定、履约签证留痕到多轮审计对抗，建立滴水不漏的证据链，把账面应收稳步转化为真实的银行回款。
                        </div>
                    </div>
                    <div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: {BRONZE}; background: #ffffff; padding: 5px 8px; border: 1px dashed rgba(138,104,57,0.3); border-radius: 2px; margin-bottom: 8px;">
                            合同闭环 · 签证留痕 · 审计抗辩 · 账款回笼
                        </div>
                        <a href="/monographs/marimo_honghuagang.html" target="_blank" style="display: inline-block; font-size: 12px; font-weight: 700; color: {NAVY}; text-decoration: none;">
                            [ 查看专案 → ]
                        </a>
                    </div>
                </div>

                <!-- ③ 顶层治理 -->
                <div style="background: {BG_CREAM}; border: 1px solid {BORDER_HAIR}; border-top: 3px solid {BRONZE}; border-radius: 4px; padding: 14px 16px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-bottom: 6px;">
                            <span style="font-weight: 700; color: {BRONZE};">③ 顶层治理</span>
                            <span style="color: #64748b;">2011-2014</span>
                        </div>
                        <div style="font-size: 14.5px; font-weight: 700; color: {NAVY}; margin-bottom: 6px;">顶层治理与合规底盘<br><span style="font-size: 12px; font-weight: normal; color: #64748b;">(Governance)</span></div>
                        <div style="font-size: 12.5px; color: #334155; line-height: 1.6; margin-bottom: 10px;">
                            历经百亿市值上市公司董办与总经办淬炼，深刻理解资本市场规则、三会运作与信息披露底线。具备统筹发债尽调、同业对标与公司治理的高维视野，守住合规红线。
                        </div>
                    </div>
                    <div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: {BRONZE}; background: #ffffff; padding: 5px 8px; border: 1px dashed rgba(138,104,57,0.3); border-radius: 2px; margin-bottom: 8px;">
                            上市公司合规 · 206篇A级信披 · 12亿发债尽调
                        </div>
                        <a href="/monographs/marimo_board_and_gm.html" target="_blank" style="display: inline-block; font-size: 12px; font-weight: 700; color: {NAVY}; text-decoration: none;">
                            [ 查看专案 → ]
                        </a>
                    </div>
                </div>

                <!-- ④ 数字化杠杆 -->
                <div style="background: {BG_CREAM}; border: 1px solid {BORDER_HAIR}; border-top: 3px solid {BRONZE}; border-radius: 4px; padding: 14px 16px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-bottom: 6px;">
                            <span style="font-weight: 700; color: {BRONZE};">④ 数字化杠杆</span>
                            <span style="color: #64748b;">2024-至今</span>
                        </div>
                        <div style="font-size: 14.5px; font-weight: 700; color: {NAVY}; margin-bottom: 6px;">数字化自主构建杠杆<br><span style="font-size: 12px; font-weight: normal; color: #64748b;">(Digital Ops)</span></div>
                        <div style="font-size: 12.5px; color: #334155; line-height: 1.6; margin-bottom: 10px;">
                            拒绝“PPT 数字化”与外包黑盒。具备亲自编写 Python/SQL/DuckDB 湖仓的系统构建能力，把复杂的业务流程、成本核算与履约监控转化为可落地的自动化工具。
                        </div>
                    </div>
                    <div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: {BRONZE}; background: #ffffff; padding: 5px 8px; border: 1px dashed rgba(138,104,57,0.3); border-radius: 2px; margin-bottom: 8px;">
                            自主全栈 · DuckDB湖仓 · 业务提效工具 · 零黑盒
                        </div>
                        <a href="/monographs/marimo_ai_engineering.html" target="_blank" style="display: inline-block; font-size: 12px; font-weight: 700; color: {NAVY}; text-decoration: none;">
                            [ 查看专案 → ]
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """
    )
    return (hero_frontispiece,)


@app.cell
def render_tab1_hust(con, pd, np, plt, io, base64, NAVY, BRONZE, GOLD, SLATE):
    # Tab 1 图表生成：华中科技大学学术奠基 (FIG 01 & FIG 02)
    df_stage = con.execute(
        "SELECT 阶段名称, 学分总数, 核心科目数 FROM v_hust_curriculum_stages ORDER BY 阶段序号 ASC"
    ).df()

    fig1, ax1 = plt.subplots(figsize=(7, 3.2), dpi=130)
    fig1.patch.set_facecolor("#ffffff")
    ax1.set_facecolor("#ffffff")

    _bars = ax1.barh(
        df_stage["阶段名称"],
        df_stage["学分总数"],
        color=[NAVY, BRONZE, GOLD, SLATE],
        height=0.55,
    )
    for _b in _bars:
        _w = _b.get_width()
        ax1.text(
            _w + 1.2,
            _b.get_y() + _b.get_height() / 2,
            f"{int(_w)} 学分",
            va="center",
            ha="left",
            fontsize=9.5,
            fontweight="bold",
            color=NAVY,
        )

    ax1.set_xlim(0, 60)
    ax1.set_xlabel("必修与骨干学分 (Credits)", fontsize=9.5, fontweight="bold", color=NAVY)
    ax1.set_title("FIG.01 华中科大统计学专业四大递进培养阶段学分分布 (总学分: 160+)", fontsize=11, fontweight="bold", color=NAVY, pad=10)
    ax1.grid(axis="x", linestyle="--", alpha=0.3)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    plt.tight_layout()

    buf1 = io.BytesIO()
    fig1.savefig(buf1, format="png", bbox_inches="tight")
    plt.close(fig1)
    img_hust1 = base64.b64encode(buf1.getvalue()).decode()

    # 雷达图 FIG 02
    categories = [
        "数理逻辑演绎\n(公理化体系 98分)",
        "随机过程推断\n(Kolmogorov 96分)",
        "高维空间流形\n(矩阵分析 95分)",
        "最优化调度求解\n(运筹规划 94分)",
        "底层连续内存算法\n(C语言指针 95分)",
        "离散状态机机制\n(LBM流体 97分)",
    ]
    values = [98, 96, 95, 94, 95, 97]
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig2, ax2 = plt.subplots(figsize=(4.5, 3.2), subplot_kw=dict(polar=True), dpi=130)
    fig2.patch.set_facecolor("#ffffff")
    ax2.set_facecolor("#ffffff")
    ax2.plot(angles, values, color=NAVY, linewidth=1.8)
    ax2.fill(angles, values, color=NAVY, alpha=0.15)
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(categories, fontsize=7.5, color=NAVY, fontweight="bold")
    ax2.set_ylim(0, 105)
    ax2.set_title("FIG.02 统计学专业核心素养雷达基准", fontsize=10, fontweight="bold", color=NAVY, pad=12)
    plt.tight_layout()

    buf2 = io.BytesIO()
    fig2.savefig(buf2, format="png", bbox_inches="tight")
    plt.close(fig2)
    img_hust2 = base64.b64encode(buf2.getvalue()).decode()

    # 提取 24 门数理核心骨干课
    df_courses = con.execute(
        "SELECT 课程编号, 课程名称, 学分, 经典教材及出处, 数理学术核心训练, 所属模块 FROM v_hust_core_course_matrix"
    ).df()

    return img_hust1, img_hust2, df_courses


@app.cell
def render_tab2_board(con, pd, plt, io, base64, NAVY, BRONZE, GOLD):
    # Tab 2 图表生成：广田股份 (SZ.002482) 董办与总经办
    df_timeline = con.execute(
        "SELECT 季度节点, 总市值_亿元, 重大资本运作与经营里程碑 FROM v_sec_market_cap_timeline ORDER BY 基准日期 ASC"
    ).df()

    fig3, ax3 = plt.subplots(figsize=(7.5, 3.3), dpi=130)
    fig3.patch.set_facecolor("#ffffff")
    ax3.set_facecolor("#ffffff")

    _x = range(len(df_timeline))
    ax3.bar(
        _x,
        df_timeline["总市值_亿元"],
        color=NAVY,
        alpha=0.3,
        width=0.55,
        label="季度市值规模 (亿元)",
    )
    ax3.plot(
        _x,
        df_timeline["总市值_亿元"],
        color=NAVY,
        marker="o",
        linewidth=2,
        label="任期市值走势",
    )

    # 标注发债与高点
    ax3.annotate(
        "12 亿公司债顺利发行\n(深交所零问询)",
        xy=(5, 108.5),
        xytext=(3.5, 122),
        arrowprops=dict(facecolor=BRONZE, shrink=0.08, width=1, headwidth=5),
        fontsize=8.5,
        fontweight="bold",
        color=BRONZE,
    )
    ax3.annotate(
        "市值跨越 132.2 亿巅峰",
        xy=(10, 132.2),
        xytext=(8.2, 138),
        arrowprops=dict(facecolor="red", shrink=0.08, width=1, headwidth=5),
        fontsize=8.5,
        fontweight="bold",
        color="red",
    )

    ax3.set_xticks(_x)
    ax3.set_xticklabels(df_timeline["季度节点"], rotation=35, ha="right", fontsize=8)
    ax3.set_ylabel("总市值 (亿元 RMB)", fontsize=9.5, fontweight="bold", color=NAVY)
    ax3.set_title("FIG.03 深圳广田股份 (SZ.002482) 任期市值走势与重大资本事件 (2011-2014)", fontsize=11, fontweight="bold", color=NAVY, pad=10)
    ax3.grid(axis="y", linestyle="--", alpha=0.3)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.legend(loc="upper left", fontsize=8.5)
    plt.tight_layout()

    buf3 = io.BytesIO()
    fig3.savefig(buf3, format="png", bbox_inches="tight")
    plt.close(fig3)
    img_board1 = base64.b64encode(buf3.getvalue()).decode()

    # 206 篇公告底账前 20 篇
    df_announcements = con.execute(
        "SELECT 发布日期, 公告标题, 业务事件归类, 公告类型 FROM v_sec_announcements_tenure ORDER BY 发布日期 DESC LIMIT 20"
    ).df()

    # 12 亿发债尽调 55 个模块
    df_bond_modules = con.execute(
        "SELECT 模块编号, 尽调专业模块, 调查事项, 详细核查内容, 责任归口 FROM v_sec_bond_due_diligence ORDER BY 模块编号 ASC"
    ).df()

    return img_board1, df_announcements, df_bond_modules


@app.cell
def render_tab3_cloud(con, pd, plt, io, base64, NAVY, BRONZE, GOLD):
    # Tab 3 图表生成：广田云软装 135 份合同大盘
    df_cats = con.execute(
        "SELECT 业态大类, 项目数量, 合同总额_万元, 审定总额_万元 FROM v_gt_contracts_by_type ORDER BY 合同总额_万元 DESC"
    ).df()

    fig4, ax4 = plt.subplots(figsize=(7.5, 3.2), dpi=130)
    fig4.patch.set_facecolor("#ffffff")
    ax4.set_facecolor("#ffffff")

    _y_pos = range(len(df_cats))
    _bar_h = 0.35
    ax4.barh([y - _bar_h/2 for y in _y_pos], df_cats["合同总额_万元"] / 10000, height=_bar_h, color=NAVY, label="签约总额 (亿元)")
    ax4.barh([y + _bar_h/2 for y in _y_pos], df_cats["审定总额_万元"] / 10000, height=_bar_h, color=GOLD, label="审定产值 (亿元)")

    ax4.set_yticks(_y_pos)
    ax4.set_yticklabels(df_cats["业态大类"], fontsize=8.5, fontweight="bold")
    ax4.set_xlabel("金额规模 (亿元 RMB)", fontsize=9.5, fontweight="bold", color=NAVY)
    ax4.set_title("FIG.04 广田云软装 135 份合同四大业务集群签约与审定产值底账", fontsize=11, fontweight="bold", color=NAVY, pad=10)
    ax4.grid(axis="x", linestyle="--", alpha=0.3)
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    ax4.legend(loc="lower right", fontsize=8.5)
    plt.tight_layout()

    buf4 = io.BytesIO()
    fig4.savefig(buf4, format="png", bbox_inches="tight")
    plt.close(fig4)
    img_cloud1 = base64.b64encode(buf4.getvalue()).decode()

    # 24 大核心工程清单
    df_landmarks = con.execute(
        "SELECT 序号, 项目名称, 发包业主, 业态分类, 合同金额_万元, 审定金额_万元, 付款核心机制 FROM v_gt_contracts_master ORDER BY 合同金额_万元 DESC"
    ).df()

    return img_cloud1, df_landmarks


@app.cell
def render_tab4_ai(con, pd, plt, io, base64, NAVY, BRONZE, GOLD):
    # Tab 4 图表生成：AI 全栈自研工程
    df_ai_repos = con.execute(
        "SELECT 代码工程仓库名, 系统工程评级, 总代码行数_LOC, 核心技术概览, STAR成果与实战亮点 FROM v_ai_git_repositories ORDER BY 总代码行数_LOC DESC"
    ).df()

    fig5, ax5 = plt.subplots(figsize=(7.5, 3.6), dpi=130)
    fig5.patch.set_facecolor("#ffffff")
    ax5.set_facecolor("#ffffff")

    _bars5 = ax5.bar(range(len(df_ai_repos)), df_ai_repos["总代码行数_LOC"] / 10000, color=NAVY, width=0.55)
    for _b in _bars5:
        _h = _b.get_height()
        ax5.text(_b.get_x() + _b.get_width()/2, _h + 15, f"{int(_h)}万行", ha="center", va="bottom", fontsize=8, fontweight="bold", color=BRONZE)

    ax5.set_xticks(range(len(df_ai_repos)))
    ax5.set_xticklabels(df_ai_repos["代码工程仓库名"], rotation=30, ha="right", fontsize=8)
    ax5.set_ylabel("代码行数 (万行 LOC)", fontsize=9.5, fontweight="bold", color=NAVY)
    ax5.set_title("FIG.05 梁清波 8 大企业级自研核心系统代码资产规模 (总代码: 2,804 万行)", fontsize=11, fontweight="bold", color=NAVY, pad=10)
    ax5.grid(axis="y", linestyle="--", alpha=0.3)
    ax5.spines["top"].set_visible(False)
    ax5.spines["right"].set_visible(False)
    plt.subplots_adjust(bottom=0.22, top=0.88)

    buf5 = io.BytesIO()
    fig5.savefig(buf5, format="png", bbox_inches="tight")
    plt.close(fig5)
    img_ai1 = base64.b64encode(buf5.getvalue()).decode()

    # 提取工时与实测底账
    df_ai_summary = con.execute("SELECT * FROM v_ai_work_summary").df().T.reset_index()
    df_ai_summary.columns = ["工时度量指标", "度量实测值"]

    return img_ai1, df_ai_repos, df_ai_summary


@app.cell
def assemble_master_application(
    mo,
    hero_frontispiece,
    img_hust1,
    img_hust2,
    df_courses,
    img_board1,
    df_announcements,
    df_bond_modules,
    img_cloud1,
    df_landmarks,
    img_ai1,
    df_ai_repos,
    df_ai_summary,
    NAVY,
    BRONZE,
    BG_CREAM,
    BORDER_HAIR,
):
    # Tab 1: 华科统计学学术奠基
    tab_hust = mo.md(
        f"""
        <div style="padding: 12px 0;">
            <div style="background: {BG_CREAM}; border: 1px solid rgba(22,42,69,0.12); padding: 14px 18px; border-radius: 4px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h3 style="margin: 0; color: {NAVY}; font-size: 18px;">🎓 华中科技大学统计学学术奠基与数理算法底座</h3>
                    <a href="/monographs/marimo_hust_statistics.html" target="_blank" style="font-size: 12.5px; font-weight: 700; color: {BRONZE}; text-decoration: none; border: 1px solid {BRONZE}; padding: 3px 10px; border-radius: 3px;">
                        打开独立全息研报 ↗
                    </a>
                </div>
                <div style="font-size: 13px; color: #475569; line-height: 1.6;">
                    华中科技大学数学与统计学院 · 2002 级首届统计学本科 · 理学学士 (B.S.)<br>
                    <strong>培养规格</strong>：四年 160+ 必修学分 · 30+ 门数理与计算机骨干课程 · 《Lattice Boltzmann (LBM) 算法与流体模拟》毕业科研攻坚。
                </div>
            </div>

            <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 18px;">
                <div style="flex: 1.5; min-width: 320px;">
                    <img src="data:image/png;base64,{img_hust1}" style="width: 100%; border: 1px solid #e2e8f0; border-radius: 4px;" />
                </div>
                <div style="flex: 1; min-width: 280px;">
                    <img src="data:image/png;base64,{img_hust2}" style="width: 100%; border: 1px solid #e2e8f0; border-radius: 4px;" />
                </div>
            </div>

            <h4 style="color: {NAVY}; margin: 16px 0 8px 0;">📑 24 门数理核心骨干课程与底层思维训练穿透台账</h4>
            {mo.ui.table(df_courses, selection=None, pagination=True)}
        </div>
        """
    )

    # Tab 2: 广田股份董办与总经办
    tab_board = mo.md(
        f"""
        <div style="padding: 12px 0;">
            <div style="background: {BG_CREAM}; border: 1px solid rgba(22,42,69,0.12); padding: 14px 18px; border-radius: 4px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h3 style="margin: 0; color: {NAVY}; font-size: 18px;">🏛️ 深圳广田股份 (SZ.002482) 董办合规资本运作与总经办企业运营</h3>
                    <a href="/monographs/marimo_board_and_gm.html" target="_blank" style="font-size: 12.5px; font-weight: 700; color: {BRONZE}; text-decoration: none; border: 1px solid {BRONZE}; padding: 3px 10px; border-radius: 3px;">
                        打开独立全息研报 ↗
                    </a>
                </div>
                <div style="font-size: 13px; color: #475569; line-height: 1.6;">
                    历经百亿市值上市公司治理中枢：执笔 206 篇法定公告（深交所最高 A 级信披考评、0 监管函件）、协同 12 亿元公司债发债与 55 个尽调模块封包、总经办经营例会决议 97.8% 闭环督办；任期主导与见证广田股份市值跨越 132.2 亿元巅峰。
                </div>
            </div>

            <div style="margin-bottom: 18px;">
                <img src="data:image/png;base64,{img_board1}" style="width: 100%; border: 1px solid #e2e8f0; border-radius: 4px;" />
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 16px; margin-bottom: 16px;">
                <div>
                    <h4 style="color: {NAVY}; margin: 8px 0;">📜 深交所法定信息披露官方公告底账 (206篇抽样)</h4>
                    {mo.ui.table(df_announcements, selection=None, pagination=True)}
                </div>
                <div>
                    <h4 style="color: {NAVY}; margin: 8px 0;">💼 12 亿元公司债发债 55 个专业尽调模块</h4>
                    {mo.ui.table(df_bond_modules, selection=None, pagination=True)}
                </div>
            </div>
        </div>
        """
    )

    # Tab 3: 广田云软装 135 份合同大盘
    tab_cloud = mo.md(
        f"""
        <div style="padding: 12px 0;">
            <div style="background: {BG_CREAM}; border: 1px solid rgba(22,42,69,0.12); padding: 14px 18px; border-radius: 4px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h3 style="margin: 0; color: {NAVY}; font-size: 18px;">🏢 深圳市广田云软装科技 135 份盖章合同 6.83 亿元大盘商业操盘</h3>
                    <a href="/monographs/marimo_cloud_deco.html" target="_blank" style="font-size: 12.5px; font-weight: 700; color: {BRONZE}; text-decoration: none; border: 1px solid {BRONZE}; padding: 3px 10px; border-radius: 3px;">
                        打开独立全息研报 ↗
                    </a>
                </div>
                <div style="font-size: 13px; color: #475569; line-height: 1.6;">
                    全资子公司从 0 到 1 组建奠基：组建 45 人编制、主笔 730 条制度总纲；统筹 135 份真实合同（签约 6.83 亿 / 审定 5.92 亿），在非标供应链复杂博弈中牢牢守住 30%~35% 的真实综合毛利率底线，攻坚遵义三大破亿工程、全国五星级酒店群与头部房企战采。
                </div>
            </div>

            <div style="margin-bottom: 18px;">
                <img src="data:image/png;base64,{img_cloud1}" style="width: 100%; border: 1px solid #e2e8f0; border-radius: 4px;" />
            </div>

            <h4 style="color: {NAVY}; margin: 16px 0 8px 0;">📑 24 大核心标杆工程全生命周期核算底账</h4>
            {mo.ui.table(df_landmarks, selection=None, pagination=True)}
        </div>
        """
    )

    # Tab 4: 现代 AI 全栈工程与自治湖仓
    tab_ai = mo.md(
        f"""
        <div style="padding: 12px 0;">
            <div style="background: {BG_CREAM}; border: 1px solid rgba(22,42,69,0.12); padding: 14px 18px; border-radius: 4px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h3 style="margin: 0; color: {NAVY}; font-size: 18px;">💻 现代自主 AI 全栈工程、自治湖仓与自动化系统研发</h3>
                    <a href="/monographs/marimo_ai_engineering.html" target="_blank" style="font-size: 12.5px; font-weight: 700; color: {BRONZE}; text-decoration: none; border: 1px solid {BRONZE}; padding: 3px 10px; border-radius: 3px;">
                        打开独立全息研报 ↗
                    </a>
                </div>
                <div style="font-size: 13px; color: #475569; line-height: 1.6;">
                    将二十年商业经验深度代码化：完全独立自研 8 套工业级系统、2,804 万行源码，接入 DuckDB 现代湖仓一体与 WakaTime 国际标准 120.8 小时纯有效工时，实现 100% 实证闭环。
                </div>
            </div>

            <div style="margin-bottom: 18px;">
                <img src="data:image/png;base64,{img_ai1}" style="width: 100%; border: 1px solid #e2e8f0; border-radius: 4px;" />
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 16px; margin-bottom: 16px;">
                <div>
                    <h4 style="color: {NAVY}; margin: 8px 0;">🚀 8 大工业级核心代码资产与商业能力穿透</h4>
                    {mo.ui.table(df_ai_repos, selection=None, pagination=True)}
                </div>
                <div>
                    <h4 style="color: {NAVY}; margin: 8px 0;">⏱️ WakaTime 国际标准工作量度量底账</h4>
                    {mo.ui.table(df_ai_summary, selection=None, pagination=True)}
                </div>
            </div>
        </div>
        """
    )

    # Tab 5: 历史商业专案底稿与审计归档 (手风琴)
    tab_archived = mo.accordion(
        {
            "🗄️ ARCH-ZY-01: 遵义大酒店 · 五星级软装工程全周期商业操盘研报 (1.25亿暂定总价 / 审定9300万)": mo.md(
                """
                - **商业模式**：遵义道桥建设集团发包，中建四局总包，深圳广田专业分包；
                - **审定结果**：合同暂定金额 12,500.00 万元，最终结算审计审定 9,300.00 万元；
                - **核心机制**：穿透珠三角源头工坊出厂成本，预留多级调价博弈弹性；签证留痕，结算审计据理力争，各节点款项按期安全回笼。
                - 🔗 [查看独立 Marimo 反应式研报](/monographs/marimo_cloud_deco.html) | [查看原版静态研报档案 (HTML)](/monographs/遵义大酒店五星级软装工程全周期商业操盘研报.html)
                """
            ),
            "🗄️ ARCH-HHG-02: 遵义红花岗综合体 · 政府大盘全生命周期商业研报 (3502.9万申报 / 2408.99万认价锁定)": mo.md(
                """
                - **商业统筹**：遵义红花岗区城投国资发包，中建四局总包，广田专业分包；
                - **资金破局**：直面业主决策层化解千万元垫资风险，争取到 1,000 万元业主无息周转借款平账；
                - **实物盘量**：激光实测据实核定 16,478 ㎡，穿透 390 行原子级 BOM 物料台账，完成 14,950 件(套) 物理实物开箱交付。
                - 🔗 [查看独立 Marimo 反应式研报](/monographs/marimo_honghuagang.html) | [查看原版静态研报档案 (HTML)](/monographs/红花岗项目全生命周期深度商业研报.html)
                """
            ),
            "🗄️ ARCH-MT-03: 遵义湄潭温泉酒店 · 全生命周期数据洞察研报 (单方1537元/㎡ / 审计零坏账安全回笼)": mo.md(
                """
                - **项目承揽**：贵州茶旅一体化 AAAA 级景区核心配套，中建四局专业分包，签约 3,380.00 万元；
                - **降本与回款**：样板房开模先行，52 套客房大货集采单件刚性降本超 36%；出厂货款覆盖率 144% 刚性回笼；
                - **结算收口**：激光实测 17,241 ㎡，按包干综合单方 1,537 元/㎡ 据实核定，多轮严苛财评零坏账退出。
                - 🔗 [查看独立 Marimo 反应式研报](/monographs/marimo_meitan.html) | [查看原版静态研报档案 (HTML)](/monographs/湄潭项目全生命周期数据洞察研报.html)
                """
            ),
            "🗄️ ARCH-HT-04: 上海华泰中心售楼处 · 五轮竞标商业操盘研报 (正式闭口价中标 / 零垫资风控)": mo.md(
                """
                - **竞标模式**：开发商正式招投标，五轮商务与方案博弈，闭口价 156.66 万元中标；
                - **风控防线**：设立对等防守条款，款项到位为发货前提，实现全案零垫资出货与零纠纷交付；
                - **战略战采**：同线斩获陆川九龙山庄 28 天极限抢工项目与中国奥园集团三大全国战略集采。
                - 🔗 [查看独立 Marimo 反应式研报](/monographs/marimo_huatai.html) | [查看原版静态研报档案 (HTML)](/monographs/上海华泰中心售楼处全生命周期商业操盘研报.html)
                """
            ),
            "🗄️ ARCH-PROV-05: 专案数据与底稿穿透索引 (11.96 MB 历史原件总库)": mo.md(
                """
                - **底稿归档总盘**：汇集全量合同原件盖章扫描件、经营决议月度督办单、发债尽调专业工作底稿、现场联系签证单与审计确权凭证；
                - 🔗 [直达 11.96 MB 专案数据与底稿穿透总索引](/专案数据与底稿穿透索引.html)
                """
            ),
        }
    )

    # 5 大多维视角总装 Tabs
    main_tabs = mo.ui.tabs(
        {
            "🎓 学术奠基 · 数理底座": tab_hust,
            "🏛️ 顶层治理 · 资本合规": tab_board,
            "🏢 产业操盘 · 供应链大盘": tab_cloud,
            "💻 现代工程 · 自治湖仓": tab_ai,
            "🗄️ 历史专案底稿归档": tab_archived,
        }
    )

    # 页面最终总装
    app_layout = mo.vstack(
        [
            hero_frontispiece,
            main_tabs,
            mo.md(
                f"""
                <div style="text-align: center; padding: 28px 0 16px 0; color: #94a3b8; font-size: 11.5px; border-top: 1px solid {BORDER_HAIR}; margin-top: 30px;">
                    © 2026 Boone Liang (梁清波) · 个人履历与二十年商业操盘全息总谱 (Marimo 旗舰版) · 驱动引擎: DuckDB Direct-Lake · 弃用 YAML 中间层
                </div>
                """
            ),
        ]
    )
    return (app_layout,)


@app.cell
def render_main_view(app_layout):
    app_layout
    return


if __name__ == "__main__":
    app.run()
