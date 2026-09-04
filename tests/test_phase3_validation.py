"""
Phase 3 Validation — CRM Analytics & KPI Cross-Check
=====================================================
Runs key SQL queries against PostgreSQL and independently computes the same
KPIs using pandas. Cross-checks for correctness across:
- Opportunity counts (total, open, closed, by stage)
- Won/Lost counts
- Win rate (63.15%)
- Won revenue ($10,005,534.0), average deal size ($2,360.91)
- Average sales cycle (47.99 days)
- NULL handling
- No duplicate counting
- 30 active pipeline agents, 35 team agents, 85 accounts, 7 products
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
import pandas as pd
from decimal import Decimal
from config.settings import get_db_params

PASS_COUNT = 0
FAIL_COUNT = 0

def check(description: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  [PASS] {description}")
    else:
        FAIL_COUNT += 1
        print(f"  [FAIL] {description}")
        if detail:
            print(f"         Detail: {detail}")

def query_scalar(cur, sql):
    cur.execute(sql)
    return cur.fetchone()[0]

def query_row(cur, sql):
    cur.execute(sql)
    return cur.fetchone()

def query_all(cur, sql):
    cur.execute(sql)
    return cur.fetchall()

def to_float(val):
    if isinstance(val, Decimal):
        return float(val)
    return float(val) if val is not None else None

def run_phase3_validation():
    global PASS_COUNT, FAIL_COUNT
    PASS_COUNT = 0
    FAIL_COUNT = 0

    params = get_db_params()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    print("=" * 80)
    print("PHASE 3 CRM ANALYTICS COMPREHENSIVE VALIDATION")
    print("=" * 80)

    # ========================================================================
    # 1. SQL Execution Validation — All CRM analytics files parse and run
    # ========================================================================
    print("\n--- 1. SQL File Execution ---")

    sql_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "sql", "analytics")
    expected_files = [
        "01_pipeline_overview.sql",
        "02_win_rate.sql",
        "03_revenue_analysis.sql",
        "04_sales_cycle.sql",
        "05_agent_performance.sql",
        "06_product_performance.sql",
        "07_account_sector_analysis.sql",
        "08_sales_funnel.sql",
        "09_sales_time_analysis.sql",
        "10_pipeline_value.sql",
    ]

    for fname in expected_files:
        fpath = os.path.join(sql_dir, fname)
        file_exists = os.path.isfile(fpath)
        check(f"SQL file exists: {fname}", file_exists)
        if file_exists:
            with open(fpath, "r", encoding="utf-8") as f:
                sql_content = f.read()
            cleaned_lines = []
            for line in sql_content.split("\n"):
                stripped = line.split("--")[0]
                cleaned_lines.append(stripped)
            cleaned_sql = "\n".join(cleaned_lines)
            statements = [s.strip() for s in cleaned_sql.split(";") if s.strip()]
            try:
                for stmt in statements:
                    if not stmt.strip():
                        continue
                    cur.execute(stmt)
                conn.rollback()
                check(f"SQL executes successfully: {fname}", True)
            except Exception as e:
                conn.rollback()
                check(f"SQL executes successfully: {fname}", False, str(e))

    # ========================================================================
    # 2. Independent CSV/Pandas Calculation vs PostgreSQL SQL Validation
    # ========================================================================
    print("\n--- 2. Opportunity Count & Pipeline Cross-Check (Pandas CSV vs PostgreSQL SQL) ---")

    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
    sales_csv_path = os.path.join(data_dir, "crm_sales", "sales_pipeline.csv")

    df_sales = pd.read_csv(sales_csv_path)

    # Opportunity Counts
    py_total_opps = len(df_sales)
    sql_total_opps = query_scalar(cur, "SELECT COUNT(*) FROM crm_sales.sales_pipeline")
    check(f"Total opportunities: SQL={sql_total_opps}, Pandas={py_total_opps} (expected 8800)",
          sql_total_opps == 8800 and py_total_opps == 8800)

    py_won = len(df_sales[df_sales['deal_stage'] == 'Won'])
    sql_won = query_scalar(cur, "SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE deal_stage = 'Won'")
    check(f"Won opportunities: SQL={sql_won}, Pandas={py_won} (expected 4238)",
          sql_won == 4238 and py_won == 4238)

    py_lost = len(df_sales[df_sales['deal_stage'] == 'Lost'])
    sql_lost = query_scalar(cur, "SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE deal_stage = 'Lost'")
    check(f"Lost opportunities: SQL={sql_lost}, Pandas={py_lost} (expected 2473)",
          sql_lost == 2473 and py_lost == 2473)

    py_prospecting = len(df_sales[df_sales['deal_stage'] == 'Prospecting'])
    sql_prospecting = query_scalar(cur, "SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE deal_stage = 'Prospecting'")
    check(f"Prospecting opportunities: SQL={sql_prospecting}, Pandas={py_prospecting} (expected 500)",
          sql_prospecting == 500 and py_prospecting == 500)

    py_engaging = len(df_sales[df_sales['deal_stage'] == 'Engaging'])
    sql_engaging = query_scalar(cur, "SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE deal_stage = 'Engaging'")
    check(f"Engaging opportunities: SQL={sql_engaging}, Pandas={py_engaging} (expected 1589)",
          sql_engaging == 1589 and py_engaging == 1589)

    py_open = len(df_sales[df_sales['deal_stage'].isin(['Prospecting', 'Engaging'])])
    sql_open = query_scalar(cur, "SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE deal_stage IN ('Prospecting', 'Engaging')")
    check(f"Open opportunities: SQL={sql_open}, Pandas={py_open} (expected 2089)",
          sql_open == 2089 and py_open == 2089)

    py_closed = py_won + py_lost
    sql_closed = query_scalar(cur, "SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE deal_stage IN ('Won', 'Lost')")
    check(f"Closed opportunities: SQL={sql_closed}, Pandas={py_closed} (expected 6711)",
          sql_closed == 6711 and py_closed == 6711)

    check(f"Sum of stages = total (got {sql_won + sql_lost + sql_prospecting + sql_engaging})",
          sql_won + sql_lost + sql_prospecting + sql_engaging == sql_total_opps)

    # ========================================================================
    # 3. Win Rate Cross-Check (Pandas CSV vs PostgreSQL SQL)
    # ========================================================================
    print("\n--- 3. Win Rate Cross-Check ---")

    sql_wr = to_float(query_scalar(cur, """
        SELECT ROUND(
            COUNT(*) FILTER (WHERE deal_stage = 'Won') * 100.0
            / NULLIF(COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost')), 0),
            2
        )
        FROM crm_sales.sales_pipeline
    """))
    py_wr = round(py_won * 100.0 / (py_won + py_lost), 2)

    check(f"SQL win rate = {sql_wr}%, Pandas CSV win rate = {py_wr}%",
          abs(sql_wr - py_wr) < 0.01 and abs(sql_wr - 63.15) < 0.01,
          f"SQL={sql_wr}, Pandas={py_wr}")

    check(f"Win rate denominator excludes open deals (denom={sql_won + sql_lost}, not {sql_total_opps})",
          sql_won + sql_lost == 6711)

    # ========================================================================
    # 4. Won Revenue & Deal Size Cross-Check (Pandas CSV vs PostgreSQL SQL)
    # ========================================================================
    print("\n--- 4. Won Revenue & Deal Size Cross-Check ---")

    sql_revenue = to_float(query_scalar(cur, """
        SELECT SUM(close_value) FROM crm_sales.sales_pipeline WHERE deal_stage = 'Won'
    """))
    py_revenue = float(df_sales[df_sales['deal_stage'] == 'Won']['close_value'].sum())

    check(f"SQL won revenue = {sql_revenue}, Pandas CSV = {py_revenue} (expected 10005534.0)",
          abs(sql_revenue - py_revenue) < 0.01 and abs(sql_revenue - 10005534.0) < 0.01)

    sql_avg_deal = to_float(query_scalar(cur, """
        SELECT ROUND(AVG(close_value), 2)
        FROM crm_sales.sales_pipeline WHERE deal_stage = 'Won'
    """))
    py_avg_deal = round(float(df_sales[df_sales['deal_stage'] == 'Won']['close_value'].mean()), 2)

    check(f"SQL avg deal size = {sql_avg_deal}, Pandas CSV = {py_avg_deal} (expected 2360.91)",
          abs(sql_avg_deal - py_avg_deal) < 0.01 and abs(sql_avg_deal - 2360.91) < 0.01)

    lost_revenue = to_float(query_scalar(cur, """
        SELECT COALESCE(SUM(close_value), 0)
        FROM crm_sales.sales_pipeline WHERE deal_stage = 'Lost'
    """))
    py_lost_rev = float(df_sales[df_sales['deal_stage'] == 'Lost']['close_value'].fillna(0).sum())
    check(f"Lost revenue = $0 (SQL=${lost_revenue}, Pandas=${py_lost_rev})",
          lost_revenue == 0.0 and py_lost_rev == 0.0)

    open_non_null = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_pipeline
        WHERE deal_stage IN ('Prospecting', 'Engaging') AND close_value IS NOT NULL
    """)
    py_open_non_null = int(df_sales[df_sales['deal_stage'].isin(['Prospecting', 'Engaging'])]['close_value'].notna().sum())
    check(f"Open deals with non-NULL close_value = 0 (SQL={open_non_null}, Pandas={py_open_non_null})",
          open_non_null == 0 and py_open_non_null == 0)

    # ========================================================================
    # 5. Sales Cycle Cross-Check (Pandas CSV vs PostgreSQL SQL)
    # ========================================================================
    print("\n--- 5. Sales Cycle Cross-Check ---")

    row = query_row(cur, """
        SELECT
            COUNT(*),
            ROUND(AVG(close_date - engage_date), 2),
            MIN(close_date - engage_date),
            MAX(close_date - engage_date)
        FROM crm_sales.sales_pipeline
        WHERE deal_stage IN ('Won', 'Lost')
          AND engage_date IS NOT NULL
          AND close_date  IS NOT NULL
    """)
    cycle_count, sql_avg_cycle, min_cycle, max_cycle = row
    sql_avg_cycle = to_float(sql_avg_cycle)

    df_closed = df_sales[df_sales['deal_stage'].isin(['Won', 'Lost']) &
                         df_sales['engage_date'].notna() &
                         df_sales['close_date'].notna()].copy()
    df_closed['cycle_days'] = (pd.to_datetime(df_closed['close_date']) - pd.to_datetime(df_closed['engage_date'])).dt.days

    py_avg_cycle = round(float(df_closed['cycle_days'].mean()), 2)
    py_min_cycle = int(df_closed['cycle_days'].min())
    py_max_cycle = int(df_closed['cycle_days'].max())

    check(f"Sales cycle computed on {cycle_count} closed deals (Pandas={len(df_closed)}, expected 6711)",
          cycle_count == 6711 and len(df_closed) == 6711)
    check(f"Min cycle >= 0 days (SQL={min_cycle}, Pandas={py_min_cycle})", min_cycle == py_min_cycle and min_cycle >= 0)
    check(f"Max cycle is reasonable (SQL={max_cycle} days, Pandas={py_max_cycle} days)", max_cycle == py_max_cycle and max_cycle <= 365)
    check(f"SQL avg cycle = {sql_avg_cycle}, Pandas CSV = {py_avg_cycle} (expected 47.99)",
          abs(sql_avg_cycle - py_avg_cycle) < 0.05 and abs(sql_avg_cycle - 47.99) < 0.05)

    neg_cycles = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_pipeline
        WHERE (close_date - engage_date) < 0
    """)
    py_neg_cycles = int((df_closed['cycle_days'] < 0).sum())
    check(f"No negative sales cycles (SQL={neg_cycles}, Pandas={py_neg_cycles})", neg_cycles == 0 and py_neg_cycles == 0)

    # ========================================================================
    # 6. NULL Handling Validation
    # ========================================================================
    print("\n--- 6. NULL Handling ---")

    null_account = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE account IS NULL
    """)
    check(f"NULL accounts = 1425 (got {null_account})", null_account == 1425)

    null_engage = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE engage_date IS NULL
    """)
    check(f"NULL engage_date = 500 (got {null_engage})", null_engage == 500)

    null_close_dt = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE close_date IS NULL
    """)
    check(f"NULL close_date = 2089 (got {null_close_dt})", null_close_dt == 2089)

    null_close_val = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE close_value IS NULL
    """)
    check(f"NULL close_value = 2089 (got {null_close_val})", null_close_val == 2089)

    null_cv_closed = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_pipeline
        WHERE deal_stage IN ('Won', 'Lost') AND close_value IS NULL
    """)
    check(f"No NULL close_value in Won/Lost (got {null_cv_closed})",
          null_cv_closed == 0)

    # ========================================================================
    # 7. No Duplicate Counting
    # ========================================================================
    print("\n--- 7. Duplicate Check ---")

    dup_opps = query_scalar(cur, """
        SELECT COUNT(*) - COUNT(DISTINCT opportunity_id)
        FROM crm_sales.sales_pipeline
    """)
    check(f"No duplicate opportunity_ids (dupes={dup_opps})", dup_opps == 0)

    # ========================================================================
    # 8. Agent & Product Reference Integrity
    # ========================================================================
    print("\n--- 8. Reference Integrity ---")

    agents_in_pipeline = query_scalar(cur, """
        SELECT COUNT(DISTINCT sales_agent) FROM crm_sales.sales_pipeline
    """)
    agents_in_teams = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_teams
    """)
    check(f"30 active agents in pipeline, 35 total in teams "
          f"(pipeline={agents_in_pipeline}, teams={agents_in_teams})",
          agents_in_pipeline == 30 and agents_in_teams == 35)

    products_in_pipeline = query_scalar(cur, """
        SELECT COUNT(DISTINCT product) FROM crm_sales.sales_pipeline
    """)
    check(f"7 products in pipeline (got {products_in_pipeline})",
          products_in_pipeline == 7)

    # GTX Pro standardization
    gtxpro_raw = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE product = 'GTXPro'
    """)
    gtx_pro = query_scalar(cur, """
        SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE product = 'GTX Pro'
    """)
    check(f"GTXPro standardized to GTX Pro (GTXPro={gtxpro_raw}, GTX Pro={gtx_pro})",
          gtxpro_raw == 0 and gtx_pro > 0)

    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "=" * 80)
    print(f"TOTAL: {PASS_COUNT} PASSED, {FAIL_COUNT} FAILED "
          f"out of {PASS_COUNT + FAIL_COUNT} validation checks.")
    print("=" * 80)

    cur.close()
    conn.close()

    return FAIL_COUNT == 0

def test_phase3_validation():
    assert run_phase3_validation() is True

if __name__ == "__main__":
    success = run_phase3_validation()
    sys.exit(0 if success else 1)
