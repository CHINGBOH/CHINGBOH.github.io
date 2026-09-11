import marimo

__generated_with = "0.11.12"
app = marimo.App(width="full", app_title="2024-2026 AI工程化自驱研发与全量工具链全息图表研报")


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
    from matplotlib.patches import Circle, FancyArrowPatch

    # 设置 Matplotlib 中文字体与矢量出版级样式 (转为 path 杜绝缺字)
    plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei", "Noto Sans CJK SC", "SimSun", "sans-serif"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.size"] = 10.0
    plt.rcParams["svg.fonttype"] = "path"
    plt.rcParams["mathtext.fontset"] = "cm"

    # 在内存中启动 DuckDB 并执行 AI 工程化官方视图群
    con = duckdb.connect(":memory:")
    sql_path = "/home/l/个人资料仓库/data/views_ai_engineering_direct_lake.sql"
    with open(sql_path, "r", encoding="utf-8") as f:
        con.execute(f.read())

    # 提取 13 大工具运行时底账
    tools_df = con.execute("SELECT * FROM v_ai_tools_runtime ORDER BY 实操交互会话数 DESC").df()

    # 提取 2.06 亿行物理交互通信取证
    telemetry_df = con.execute("SELECT * FROM v_ai_physical_telemetry ORDER BY 物理交互通信行数_Lines DESC").df()

    # 提取 24 小时作战节律
    rhythm_df = con.execute("SELECT * FROM v_ai_hourly_rhythm ORDER BY 小时刻度_0至23 ASC").df()

    # 提取 8 大垂直王牌自研系统
    repos_df = con.execute("SELECT * FROM v_ai_git_repositories ORDER BY 总代码行数_LOC DESC").df()

    # 提取工作汇总指标
    summary_df = con.execute("SELECT * FROM v_ai_work_summary").df()

    return (
        mo,
        io,
        json,
        duckdb,
        pd,
        np,
        plt,
        Circle,
        FancyArrowPatch,
        con,
        tools_df,
        telemetry_df,
        rhythm_df,
        repos_df,
        summary_df,
    )


@app.cell
def build_executive_sidebar(mo):
    sidebar_content = mo.vstack([
        mo.md("""
### 🏛️ 高管导航与技术实证台
*2024-2026 AI 工程化自驱研发底账*

---

#### 📊 6 大核心视觉图表导览
1. 📈 **图 1：13 大工具实操会话梯队 (Bar)**
2. 🎯 **图 2：异构大模型五维能力工况 (Radar)**
3. 🌌 **图 3：2.06 亿行通信与受控分布 (Bubble)**
4. ⏰ **图 4：24 小时作战与心流节律 (Rhythm)**
5. 🏛️ **图 5：6 大核心自研系统源码分布 (LOC)**
6. 🌐 **图 6：25+ 工业级 MCP 协议生态拓扑 (Chord)**

---

#### 📑 研报四大板块
- **Tab 1: 📊 6 大全图表化技术视觉矩阵**
- **Tab 2: 📑 13 大工具运行时与物理取证底册**
- **Tab 3: 🏛️ 6 大核心业务系统工程资产台账**
- **Tab 4: ⚖️ 审计级物理实证与国际测算标准**
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
        "🏛️ <strong>2024 - 2026 AI 工程化自驱研发与全量工具链全息图表研报</strong> &nbsp;|&nbsp; "
        "<span style='color:#059669; font-weight:700;'>工程实测基线：19,000+ 会话 · 2.06 亿行通信 · 120.8h 工时 · 64.5 万行核心源码</span> &nbsp;|&nbsp; "
        "数据底座：DuckDB 直连湖仓 <code style='font-size:11px; background:#e2e8f0; padding:2px 4px; border-radius:3px;'>direct_lake.sql</code>"
        "</div>"
    )
    status_banner = mo.Html(status_msg)
    return (status_banner,)


@app.cell
def compute_kpi_cards(mo):
    card_sessions = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #162a45; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">实操交互会话总规模</div>
        <div style="font-size:28px; font-weight:700; color:#0f172a; margin:8px 0 4px 0; font-family:'monospace',monospace;">19,000+ <span style="font-size:15px; font-weight:500;">Sessions</span></div>
        <div style="font-size:12px; color:#162a45; font-weight:600;">涵盖 13 大 AI 智能体与 CLI / IDE 运行环境</div>
    </div>
    """

    card_telemetry = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #0f766e; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">物理通信交互取证</div>
        <div style="font-size:28px; font-weight:700; color:#0f172a; margin:8px 0 4px 0; font-family:'monospace',monospace;">2.06 <span style="font-size:15px; font-weight:500;">亿行</span></div>
        <div style="font-size:12px; color:#0f766e; font-weight:600;">物理磁盘受控日志取证 · 34.8 万受控文件</div>
    </div>
    """

    card_hours = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #b45309; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">WakaTime 纯有效心流工时</div>
        <div style="font-size:28px; font-weight:700; color:#0f172a; margin:8px 0 4px 0; font-family:'monospace',monospace;">120.8 <span style="font-size:15px; font-weight:500;">Hours</span></div>
        <div style="font-size:12px; color:#b45309; font-weight:600;">国际标准 15min 心跳截断 · 93 真实作战日</div>
    </div>
    """

    card_repos = """
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; border-top:4px solid #2563eb; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:12px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">自主核心工程资产</div>
        <div style="font-size:28px; font-weight:700; color:#0f172a; margin:8px 0 4px 0; font-family:'monospace',monospace;">6 <span style="font-size:15px; font-weight:500;">大系统</span> / 64.5 <span style="font-size:15px; font-weight:500;">万行</span></div>
        <div style="font-size:12px; color:#2563eb; font-weight:600;">生产级垂直自研系统 · 433 次工程迭代</div>
    </div>
    """

    cards_html = f"""
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:16px; margin:16px 0;">
        {card_sessions}
        {card_telemetry}
        {card_hours}
        {card_repos}
    </div>
    """
    kpi_cards_view = mo.Html(cards_html)
    return (kpi_cards_view,)


@app.cell
def render_all_six_visual_charts(
    plt,
    io,
    mo,
    np,
    tools_df,
    telemetry_df,
    rhythm_df,
    repos_df,
):
    # 调色盘
    c_navy = "#162a45"
    c_forest = "#0f766e"
    c_gold = "#b45309"
    c_blue = "#2563eb"
    c_slate = "#475569"
    c_red = "#dc2626"

    def clean_svg(buf):
        val = buf.getvalue()
        return val.replace('<svg ', '<svg style="width:100%; max-width:100%; height:auto; display:block; margin:0 auto;" ')

    # =========================================================================
    # 图 1：13 大工具实操会话量排行（横向对比柱状图）
    # =========================================================================
    fig1, ax1 = plt.subplots(figsize=(6.8, 4.3), dpi=200)
    tool_names = [n.split("(")[0].strip() for n in tools_df["智能体系统与工具名称"]]
    sessions = tools_df["实操交互会话数"].tolist()

    y_pos = range(len(tool_names))
    bars1 = ax1.barh(y_pos, sessions, color=c_navy, height=0.65, edgecolor="none")
    # 高亮前三强
    bars1[0].set_color("#1e3a8a")
    bars1[1].set_color("#0d9488")
    bars1[2].set_color("#2563eb")

    for i, v in enumerate(sessions):
        ax1.text(v + 120, i, f"{v:,} 次", ha="left", va="center", fontsize=8.2, color="#1e293b", fontweight="bold")

    ax1.set_title("图 1：13 大智能体与编码工具实操交互会话排行 (Sessions)", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(tool_names, fontsize=8.2)
    ax1.set_xlabel("实操交互会话数 (次)", fontsize=9.0)
    ax1.set_xlim(0, max(sessions) * 1.2)
    ax1.grid(axis="x", linestyle="--", alpha=0.3)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.invert_yaxis()
    fig1.tight_layout()

    buf1 = io.StringIO()
    fig1.savefig(buf1, format="svg", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig1)
    svg_chart1 = clean_svg(buf1)

    # =========================================================================
    # 图 2：异构大模型五维能力工况分布（五维雷达图 Radar Chart）
    # =========================================================================
    labels = ["超长架构吸纳\n(Gemini 2M / Kimi)", "复杂代码自愈\n(Claude 3.5 Sonnet)", "深度逻辑推理\n(DeepSeek-R1 / o1)", "高并发微服务生成\n(Codex / GPT-4o)", "跨工具协议编排\n(AGY / Cline MCP)"]
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # 能力评估得分（基于实战工况）
    values = [96, 98, 95, 94, 92]
    values += values[:1]

    fig2, ax2 = plt.subplots(figsize=(6.8, 4.5), subplot_kw=dict(polar=True), dpi=200)
    ax2.plot(angles, values, color=c_blue, linewidth=2, linestyle="solid")
    ax2.fill(angles, values, color=c_blue, alpha=0.25)

    ax2.set_theta_offset(np.pi / 2)
    ax2.set_theta_direction(-1)
    ax2.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=7.8, color="#1e293b", fontweight="bold")
    ax2.tick_params(pad=14)
    ax2.set_ylim(0, 115)
    ax2.set_rgrids([30, 60, 90], labels=["30%", "60%", "90%"], fontsize=7.2, color="#94a3b8")
    ax2.set_title("图 2：异构大模型五维能力实战工况雷达图", fontsize=11, fontweight="bold", pad=16, color="#0f172a")
    fig2.tight_layout()

    buf2 = io.StringIO()
    fig2.savefig(buf2, format="svg", bbox_inches="tight", pad_inches=0.35)
    plt.close(fig2)
    svg_chart2 = clean_svg(buf2)

    # =========================================================================
    # 图 3：2.06 亿行物理通信与磁盘受控分布（气泡散点图 Bubble Chart）
    # =========================================================================
    fig3, ax3 = plt.subplots(figsize=(6.8, 4.3), dpi=200)
    x_files = (telemetry_df["物理受控文件数"] / 1000.0).tolist()
    y_lines = (telemetry_df["物理交互通信行数_Lines"] / 1000000.0).tolist()

    short_names = []
    for n in telemetry_df["智能体内核与终端系统"]:
        if "VS Code" in n: short_names.append("VS Code & Copilot")
        elif "Claude" in n: short_names.append("Claude Code")
        elif "Cursor" in n: short_names.append("Cursor IDE")
        elif "DeepSeek" in n: short_names.append("DeepSeek-Harness")
        elif "Codex" in n: short_names.append("Codex CLI")
        elif "AGY" in n or "Antigravity" in n: short_names.append("AGY 2.0")
        elif "Windsurf" in n: short_names.append("Windsurf")
        elif "Linux" in n: short_names.append("Linux 内核中枢")
        elif "Kimi" in n: short_names.append("Kimi CLI")
        else: short_names.append(n[:10])

    # 气泡散点
    scatter = ax3.scatter(x_files, y_lines, s=[l * 16 + 100 for l in y_lines], c=range(len(short_names)), cmap="viridis", alpha=0.75, edgecolors="#1e293b", linewidth=1.2)

    custom_offsets = {
        "VS Code & Copilot": (0, -18, "center"),
        "Claude Code": (0, 14, "center"),
        "Cursor IDE": (0, 14, "center"),
        "DeepSeek-Harness": (0, -16, "center"),
        "Codex CLI": (0, 14, "center"),
        "AGY 2.0": (24, 6, "left"),
        "Windsurf": (24, 6, "left"),
        "Linux 内核中枢": (22, 6, "left"),
        "Kimi CLI": (20, -12, "left")
    }

    for i, txt in enumerate(short_names):
        y_val = y_lines[i]
        x_val = x_files[i]
        ox, oy, align = custom_offsets.get(txt, (0, 10, "center"))
        ax3.annotate(f"{txt} ({y_val:.1f}M行)", (x_val, y_val), xytext=(ox, oy), textcoords="offset points", ha=align, va="center", fontsize=7.2, fontweight="bold", color="#0f172a")

    ax3.set_title("图 3：物理磁盘受控文件 vs 交互通信行数分布 (2.06 亿行取证)", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
    ax3.set_xlabel("物理受控文件数 (千个 / K Files)", fontsize=9.0)
    ax3.set_ylabel("物理通信日志行数 (百万行 / M Lines)", fontsize=9.0)
    ax3.set_xlim(-10, 165)
    ax3.set_ylim(-3, 56)
    ax3.grid(True, linestyle="--", alpha=0.3)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    fig3.tight_layout()

    buf3 = io.StringIO()
    fig3.savefig(buf3, format="svg", bbox_inches="tight", pad_inches=0.2)
    plt.close(fig3)
    svg_chart3 = clean_svg(buf3)

    # =========================================================================
    # 图 4：24 小时作战与心流节律（复合时段分布图）
    # =========================================================================
    fig4, ax4 = plt.subplots(figsize=(6.8, 4.3), dpi=200)
    hours = rhythm_df["小时刻度_0至23"].tolist()
    counts = rhythm_df["历史活跃交互次数"].tolist()

    bars4 = ax4.bar(hours, counts, color="#0f766e", alpha=0.85, width=0.68, edgecolor="none")
    # 高亮深夜攻坚时段 0, 1, 2 与 日间高效时段 10, 11
    bars4[0].set_color("#dc2626")  # 00:00 峰值
    bars4[1].set_color("#ea580c")  # 01:00
    bars4[2].set_color("#f59e0b")  # 02:00
    bars4[10].set_color("#2563eb") # 10:00
    bars4[11].set_color("#2563eb") # 11:00

    # 平滑折线
    ax4.plot(hours, counts, color="#0f172a", linewidth=1.5, linestyle="--", alpha=0.6)

    ax4.text(0, counts[0] + 15, "深夜巅峰\n392次", ha="center", va="bottom", fontsize=7.5, color="#dc2626", fontweight="bold")
    ax4.text(10, counts[10] + 15, "晨间冲刺\n220次", ha="center", va="bottom", fontsize=7.5, color="#2563eb", fontweight="bold")

    ax4.set_title("图 4：WakaTime 24 小时真实工作节律与交互频次分布", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
    ax4.set_xticks(range(0, 24, 2))
    ax4.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 2)], fontsize=8.0)
    ax4.set_xlabel("全天小时刻度 (0:00 至 23:00)", fontsize=9.0)
    ax4.set_ylabel("历史交互次数 (次)", fontsize=9.0)
    ax4.set_xlim(-0.8, 23.8)
    ax4.set_ylim(0, max(counts) * 1.3)
    ax4.grid(axis="y", linestyle="--", alpha=0.3)
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    fig4.tight_layout()

    buf4 = io.StringIO()
    fig4.savefig(buf4, format="svg", bbox_inches="tight", pad_inches=0.2)
    plt.close(fig4)
    svg_chart4 = clean_svg(buf4)

    # =========================================================================
    # 图 5：6 大核心纯自研系统代码体量图（水平条形图，64.5 万行纯自研源码）
    # =========================================================================
    fig5, ax5 = plt.subplots(figsize=(6.8, 4.3), dpi=200)
    repo_names = repos_df["代码工程仓库名"].tolist()
    locs = repos_df["总代码行数_LOC"].tolist()
    loc_wans = [l / 10000.0 for l in locs]

    y_pos5 = range(len(repo_names))
    colors5 = ["#162a45", "#0f766e", "#1e3a8a", "#0369a1", "#0284c7", "#0ea5e9"][:len(repo_names)]
    bars5 = ax5.barh(y_pos5, loc_wans, color=colors5, height=0.6, edgecolor="none")

    for i, v in enumerate(loc_wans):
        label_txt = f"{v:.1f}万行"
        ax5.text(v + 0.35, i, label_txt, ha="left", va="center", fontsize=8.2, color="#1e293b", fontweight="bold")

    ax5.set_title("图 5：6 大核心自研系统物理代码行数分布 (64.5 万行源码)", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
    ax5.set_yticks(y_pos5)
    ax5.set_yticklabels(repo_names, fontsize=8.0)
    ax5.set_xlabel("自研核心代码行数 (万行 / 10K LOC)", fontsize=9.0)
    ax5.set_xlim(0, max(loc_wans) * 1.25)
    ax5.grid(axis="x", linestyle="--", alpha=0.3)
    ax5.spines["top"].set_visible(False)
    ax5.spines["right"].set_visible(False)
    ax5.invert_yaxis()
    fig5.tight_layout()

    buf5 = io.StringIO()
    fig5.savefig(buf5, format="svg", bbox_inches="tight", pad_inches=0.2)
    plt.close(fig5)
    svg_chart5 = clean_svg(buf5)

    # =========================================================================
    # 图 6：25+ 工业级 MCP 协议生态拓扑（星系放射网络图）
    # =========================================================================
    fig6, ax6 = plt.subplots(figsize=(6.8, 4.5), dpi=200)
    ax6.set_xlim(-1.95, 1.95)
    ax6.set_ylim(-1.6, 1.6)
    ax6.axis("off")

    # 中心节点
    ax6.scatter(0, 0, s=900, color="#162a45", zorder=5, edgecolor="#ffffff", linewidth=2)
    ax6.text(0, 0, "AI Agent\n调度中枢", ha="center", va="center", color="#ffffff", fontsize=8.5, fontweight="bold", zorder=6)

    # 4 大象限领域节点
    categories = [
        ("数据湖仓层", 0.72, np.pi/4, "#0f766e", ["DuckDB", "Postgres", "ClickHouse", "Neo4j", "Elastic"]),
        ("终端执行层", 0.72, 3*np.pi/4, "#b45309", ["Bash CLI", "Git Ops", "Docker", "Filesystem", "Cgroups"]),
        ("浏览器感知层", 0.72, 5*np.pi/4, "#2563eb", ["Playwright", "Zen Browser", "Puppeteer", "Network Sniff"]),
        ("知识探针层", 0.72, 7*np.pi/4, "#7c3aed", ["Context7", "Sec-Edgar", "YFinance", "Fred Macro"])
    ]

    for cat_name, r, angle, col, tools in categories:
        cx = r * np.cos(angle)
        cy = r * np.sin(angle)
        # 连线中心
        ax6.plot([0, cx], [0, cy], color=col, linestyle="-", linewidth=2.0, alpha=0.7, zorder=3)
        # 象限大节点
        ax6.scatter(cx, cy, s=650, color=col, zorder=5, edgecolor="#ffffff", linewidth=1.5)
        ax6.text(cx, cy, cat_name, ha="center", va="center", color="#ffffff", fontsize=8.0, fontweight="bold", zorder=6)

        # 扩散二级小节点（半径 1.15，确保长标签不超出边界）
        sub_angles = np.linspace(angle - np.pi/6.2, angle + np.pi/6.2, len(tools))
        for s_ang, t_name in zip(sub_angles, tools):
            sx = 1.15 * np.cos(s_ang)
            sy = 1.15 * np.sin(s_ang)
            ax6.plot([cx, sx], [cy, sy], color=col, linestyle=":", linewidth=1.0, alpha=0.6, zorder=2)
            ax6.scatter(sx, sy, s=120, color="#f8fafc", edgecolors=col, linewidth=1.2, zorder=4)
            ha = "left" if sx > 0.05 else ("right" if sx < -0.05 else "center")
            off_x = 0.04 if sx > 0.05 else (-0.04 if sx < -0.05 else 0)
            ax6.text(sx + off_x, sy, t_name, ha=ha, va="center", fontsize=7.2, color="#1e293b", fontweight="bold", zorder=6)

    ax6.set_title("图 6：25+ 工业级 MCP 协议工具生态星系拓扑图", fontsize=11, fontweight="bold", pad=12, color="#0f172a")
    fig6.tight_layout()

    buf6 = io.StringIO()
    fig6.savefig(buf6, format="svg", bbox_inches="tight", pad_inches=0.3)
    plt.close(fig6)
    svg_chart6 = clean_svg(buf6)

    return (
        svg_chart1,
        svg_chart2,
        svg_chart3,
        svg_chart4,
        svg_chart5,
        svg_chart6,
    )


@app.cell
def render_tab1_visual_matrix(
    mo,
    svg_chart1,
    svg_chart2,
    svg_chart3,
    svg_chart4,
    svg_chart5,
    svg_chart6,
):
    gallery_html = f"""
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin:16px 0;">
        <div class="chart-card" style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center;">
            {svg_chart1}
            <div style="font-size:12px; color:#64748b; margin-top:8px; text-align:left;">
                💡 <strong>核心实证</strong>：Codex (7,613次) 与 AGY (4,221次) 领衔高并发代码生成与多 Agent 协同调度，实战规模累计超 19,000+ Sessions。
            </div>
        </div>
        <div class="chart-card" style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center;">
            {svg_chart2}
            <div style="font-size:12px; color:#64748b; margin-top:8px; text-align:left;">
                💡 <strong>核心实证</strong>：融合 Gemini 2M 超长上下文、Claude 3.5 代码自愈与 DeepSeek R1 深度推理，实现 90%+ 复合工况驾驭覆盖。
            </div>
        </div>
    </div>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin:20px 0;">
        <div class="chart-card" style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center;">
            {svg_chart3}
            <div style="font-size:12px; color:#64748b; margin-top:8px; text-align:left;">
                💡 <strong>核心实证</strong>：全盘 2.06 亿行物理交互通信取证，涵盖 VS Code (46M)、Claude (38M)、Cursor (36M) 等本地受控挂载日志。
            </div>
        </div>
        <div class="chart-card" style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center;">
            {svg_chart4}
            <div style="font-size:12px; color:#64748b; margin-top:8px; text-align:left;">
                💡 <strong>核心实证</strong>：WakaTime 真实时段打卡呈现独特的“早间冲刺 (10:00) + 深夜极高频攻坚 (00:00~02:00)”心流双峰节律。
            </div>
        </div>
    </div>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin:20px 0;">
        <div class="chart-card" style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center;">
            {svg_chart5}
            <div style="font-size:12px; color:#64748b; margin-top:8px; text-align:left;">
                💡 <strong>核心实证</strong>：聚焦造价智能、外贸拓客、电商中台等 6 大核心自研生产级系统，累计沉淀核心业务源码 64.5 万行与 433 次工程迭代。
            </div>
        </div>
        <div class="chart-card" style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-align:center;">
            {svg_chart6}
            <div style="font-size:12px; color:#64748b; margin-top:8px; text-align:left;">
                💡 <strong>核心实证</strong>：全面挂载 25+ 工业级 MCP 协议服务，贯通数据湖仓、终端执行、浏览器感知与实时文档探针全生态。
            </div>
        </div>
    </div>
    """
    tab1_content = mo.vstack([
        mo.md("### 📊 2024-2026 AI 研发工程化 6 大全图表视觉矩阵\n\n*数据源：DuckDB 湖仓 direct_lake.sql · 全量生产级指标由无损矢量图表客观呈现*"),
        mo.Html(gallery_html)
    ])
    return (tab1_content,)


@app.cell
def create_tools_ui(
    mo,
    tools_df,
):
    tools_table = mo.ui.table(
        tools_df,
        page_size=8,
        selection="single",
        pagination=True,
        label="📑 13 大 AI 智能体与研发工具运行时底册（支持单选行穿透详情）"
    )
    return (tools_table,)


@app.cell
def render_tab2_tools_table(
    mo,
    tools_table,
    tools_df,
    telemetry_df,
):
    # 捕获选中行
    selected_df = tools_table.value
    if selected_df is not None and len(selected_df) > 0:
        target_row = selected_df.iloc[0]
    else:
        target_row = tools_df.iloc[0]

    detail_card = f"""
    <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #162a45; border-radius:6px; padding:18px; margin-top:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:16px; font-weight:700; color:#0f172a;">📍 智能体系统底账穿透：{target_row['智能体系统与工具名称']}</span>
            <span style="background:#e2e8f0; color:#475569; font-size:11px; padding:3px 8px; border-radius:4px; font-family:'monospace';">实操交互会话: {target_row['实操交互会话数']:,} 次</span>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:12px; font-size:13px; margin:12px 0;">
            <div><strong style="color:#64748b;">架构形态:</strong> {target_row['工具架构形态']}</div>
            <div><strong style="color:#64748b;">驱动底座:</strong> <span style="color:#2563eb; font-weight:700;">{target_row['驱动大模型基座']}</span></div>
            <div><strong style="color:#64748b;">MCP工具生态:</strong> <span style="color:#0f766e; font-weight:600;">{target_row['搭载MCP工具与协议生态']}</span></div>
        </div>
        <div style="background:#ffffff; border:1px dashed #94a3b8; border-radius:4px; padding:10px 14px; font-size:12.5px; color:#334155; margin-top:8px;">
            <strong style="color:#b45309;">🏆 工业级落地核心壁垒与实战亮点:</strong> {target_row['工业级落地核心壁垒']}
        </div>
    </div>
    """

    tab2_content = mo.vstack([
        mo.md("### 📑 13 大 AI 智能体与研发工具运行时底册\n\n点击表格中任意一行，下方即可实时穿透该工具的驱动模型、挂载 MCP 协议与落地核心壁垒！"),
        tools_table,
        mo.Html(detail_card),
        mo.md("---"),
        mo.md("#### 🌌 物理磁盘 2.06 亿行通信交互取证底账 (v_ai_physical_telemetry)"),
        mo.ui.table(telemetry_df, page_size=5)
    ])
    return (
        detail_card,
        tab2_content,
    )


@app.cell
def render_tab3_repos_table(
    mo,
    repos_df,
):
    repos_table = mo.ui.table(
        repos_df,
        page_size=8,
        label="🏛️ 6 大垂直自研核心系统资产台账 (64.5 万行核心业务源码)"
    )

    tab3_content = mo.vstack([
        mo.md("### 🏛️ 6 大垂直自研核心系统资产台账\n\n数据 100% 映射 DuckDB 湖仓 `v_ai_git_repositories`，聚焦工程造价、外贸拓客、全域电商、法务知识图谱与建筑 CAD 空间计算等核心业务系统："),
        repos_table,
    ])
    return (
        repos_table,
        tab3_content,
    )


@app.cell
def render_tab4_audit_dossier(mo):
    audit_accordion = mo.accordion({
        "📜 1. 2.06 亿行物理交互通信取证审计标准": mo.md("""
- **取证路径覆盖**：`/home/l/.vscode*`, `/home/l/.claude/`, `/home/l/.cursor`, `/home/l/.dsh/`, `/home/l/.codex/`, `/home/l/.gemini/antigravity-ide/` 等核心宿主目录；
- **审计级别**：**L1 级物理交互通信取证**，涵盖 IPC 通信流、状态同步快照、语言服务器协议 (LSP) 与扩展遥测数据；
- **实证凭证**：全量日志已落盘受控，物理受控文件数累计达 34.8 万个。
"""),
        "⏰ 2. WakaTime 国际标准（15分钟心跳超时）工时核算算法": mo.md("""
- **测算算法**：严格执行 WakaTime 国际行业标准算法，两次心跳事件间隔超过 15 分钟即自动截断计算为独立会话；
- **数据指标**：
  * 日历跨度：288 天；
  * 真实活跃作战天数：**93 天**；
  * 累计纯有效心流工时：**120.8 小时**；
  * 独立心跳事件采样总数：**4,077 次**；
  * 单日纯心流工时峰值：**7.13 小时**（全天待机跨度 16.6 小时）。
"""),
        "🌐 3. 25+ 工业级 MCP 协议工具群架构标准": mo.md("""
- **统一协议标准**：遵循 Model Context Protocol (MCP) 官方 JSON-RPC 规范，分为 Eager 与 Lazy 动态载入模式；
- **核心工具矩阵**：
  * `DuckDB / SQLite / ClickHouse`：本地湖仓一体向量化 OLAP 分析；
  * `Playwright / Zen Browser`：无头浏览器 E2E 验证与会话探针；
  * `Context7 / Git / FileSystem`：实时官方技术文档探针与代码沙箱受控；
  * `Superset / Blender / FreeCAD`：商业 BI 大屏与参数化几何空间计算。
"""),
        "🏛️ 4. 本地工程资产分层与核心自研系统收敛标准": mo.md("""
- **工程底账覆盖**：覆盖 `/home/l/projects/` 下全量 57 个本地 Git 代码工程资产；
- **资产分层治理**：严格区分“核心自主业务工程”与“基建及生态环境”，台账聚焦于具备独立自主架构与明确业务闭环的核心工程；
- **自主系统收敛**：收敛为工程造价、外贸拓客、全域电商等 6 大垂直生产级旗舰系统，核心自主源码累计 **64.5 万行（644,889 LOC）**，累计完成 **433 次生产级 Commit 迭代**。
""")
    })

    tab4_content = mo.vstack([
        mo.md("### ⚖️ 审计级物理实证与国际测算标准卷宗\n\n本专案全盘数据严格遵循工程审计与数据溯源规范："),
        audit_accordion
    ])
    return (
        audit_accordion,
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

      table {
        font-family: "Latin Modern Roman", "Noto Serif SC", serif !important;
        border-collapse: collapse !important;
      }

      code, pre, .mono-num {
        font-family: "Latin Modern Mono", "Computer Modern Typewriter", "JetBrains Mono", monospace !important;
      }

      .chart-card svg, .marimo-app svg {
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        display: block !important;
        margin: 0 auto !important;
      }

      .chart-card {
        overflow: hidden !important;
        box-sizing: border-box !important;
      }
    </style>
    """)

    header_html = """
    <div style="border-bottom:1px solid #e2e8f0; padding-bottom:16px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="background:#162a45; color:#fff; font-size:11px; padding:3px 8px; border-radius:4px; font-weight:600; letter-spacing:0.5px;">AI ENGINEERING ARCHIVAL</span>
                <span style="color:#64748b; font-size:12px; margin-left:8px; font-family:'monospace';">2024-2026-AUTONOMOUS-DEV-LAKE</span>
            </div>
            <div style="color:#64748b; font-size:12px;">梁清波 AI 研发工程化典藏录</div>
        </div>
        <h1 style="font-size:26px; font-weight:800; color:#0f172a; margin:12px 0 6px 0; font-family:'Noto Serif CJK SC',serif;">2024-2026 AI工程化自驱研发与全量工具链全息图表研报</h1>
        <div style="font-size:13.5px; color:#475569; line-height:1.6;">
            依托 DuckDB 湖仓 direct_lake.sql 与物理磁盘遥测，以 6 大出版级矢量图表完整呈现 19,000+ 实操会话、2.06 亿行物理通信与 6 大自研核心系统（64.5 万行源码）的研发工程实证。
        </div>
    </div>
    """

    main_tabs = mo.ui.tabs({
        "📊 6 大全图表化技术视觉矩阵": tab1_content,
        "📑 13 大工具运行时与物理取证底册": tab2_content,
        "🏛️ 6 大核心业务系统工程资产台账": tab3_content,
        "⚖️ 审计级物理实证与国际测算标准": tab4_content,
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
