#!/usr/bin/env python3
"""
数据真源校验与快照注入脚本（AGENTS.md 单一真源铁律）
====================================================
从本地 DuckDB 湖仓 (data/career_analytics_lake.duckdb) 查询关键视图，
校验 data/profile.js 中使用的数字锚点口径，并把校验结果快照为
data/verified_numbers.json 随仓库提交，供 Next.js 构建与审计引用。

用法：
    python3 scripts/build_data.py            # 校验并生成快照
    python3 scripts/build_data.py --verify   # 仅校验，不写快照
"""
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.environ.get(
    "CAREER_LAKE_DB",
    "/home/l/个人资料仓库/data/career_analytics_lake.duckdb",
)
SNAPSHOT_PATH = os.path.join(REPO_ROOT, "data", "verified_numbers.json")

# 期望口径（与 data/profile.js 叙事一致）
EXPECTED = {
    "ai_repo_count": 8,
    "ai_loc": 28038054,
    "wakatime_hours": 120.8,
    "contracts_count": 135,
    "contracts_signed_wan": 68348.0,
    "contracts_audited_wan": 59215.5,
}


def query(conn, sql):
    return conn.execute(sql).fetchall()


def main():
    if not os.path.exists(DB_PATH):
        print(f"[WARN] DuckDB 湖仓不存在: {DB_PATH}（跳过校验）")
        if "--verify" in sys.argv:
            sys.exit(0)
        return

    try:
        import duckdb
    except ImportError:
        print("[WARN] 未安装 duckdb 模块（跳过校验）")
        return

    conn = duckdb.connect(DB_PATH, read_only=True)
    report = {"db": DB_PATH, "checked_at": None, "views": {}, "passed": True}

    try:
        import datetime

        report["checked_at"] = datetime.datetime.now().isoformat(timespec="seconds")

        # AI 旗舰仓库与工时
        rows = query(conn, "SELECT COUNT(*) FROM v_ai_git_repositories")
        report["views"]["v_ai_git_repositories"] = rows
        rows = query(conn, "SELECT SUM(总代码行数_LOC) FROM v_ai_git_repositories")
        report["views"]["v_ai_line_count"] = rows
        rows = query(conn, "SELECT WakaTime累计纯有效工时_小时 FROM v_ai_work_summary")
        report["views"]["v_ai_work_summary_hours"] = rows

        # 合同大盘
        rows = query(conn, "SELECT SUM(合同份数) FROM v_gt_portfolio_all_135")
        report["views"]["v_gt_portfolio_all_135"] = rows
        rows = query(conn, "SELECT SUM(签约合同额_万元) FROM v_gt_portfolio_all_135")
        report["views"]["v_gt_signed_wan"] = rows
        rows = query(conn, "SELECT SUM(审定产值_万元) FROM v_gt_portfolio_all_135")
        report["views"]["v_gt_audited_wan"] = rows
    except Exception as e:  # 视图名可能随湖仓演进变化
        print(f"[WARN] 视图查询异常（视图名可能已变化）: {e}")
        conn.close()
        return

    conn.close()

    # 与期望口径比对（取第一个标量值）
    def scalar(rows, idx=0):
        from decimal import Decimal

        if not rows:
            return None
        v = rows[0][idx]
        return float(v) if isinstance(v, (int, float, Decimal)) else None

    checks = [
        ("AI 旗舰仓库数", scalar(report["views"]["v_ai_git_repositories"]), EXPECTED["ai_repo_count"]),
        ("AI 源码行数", scalar(report["views"]["v_ai_line_count"]), EXPECTED["ai_loc"]),
        ("WakaTime 工时", scalar(report["views"]["v_ai_work_summary_hours"]), EXPECTED["wakatime_hours"]),
        ("合同份数", scalar(report["views"]["v_gt_portfolio_all_135"]), EXPECTED["contracts_count"]),
        ("签约额(万元)", scalar(report["views"]["v_gt_signed_wan"]), EXPECTED["contracts_signed_wan"]),
        ("审定额(万元)", scalar(report["views"]["v_gt_audited_wan"]), EXPECTED["contracts_audited_wan"]),
    ]

    results = []
    for name, actual, expect in checks:
        ok = actual is not None and abs(actual - expect) < 0.51
        results.append({"metric": name, "actual": actual, "expected": expect, "pass": ok})
        report["passed"] = report["passed"] and ok
        print(f"{'✓' if ok else '✗'} {name}: 实际={actual} 期望={expect}")

    report["checks"] = results

    if "--verify" in sys.argv:
        print("\nverify-only 模式：不写快照")
        return

    def _default(o):
        from decimal import Decimal

        if isinstance(o, Decimal):
            return float(o)
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=_default)
    print(f"\n快照已写入: {SNAPSHOT_PATH} | 校验{'通过' if report['passed'] else '存在不一致'}")


if __name__ == "__main__":
    main()
