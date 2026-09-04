-- ============================================================================
-- 03_revenue_analysis.sql
-- Business Question: "What is our total and segmented won revenue?"
-- Schema: crm_sales
-- ============================================================================
-- Definition:
--   Revenue = SUM(close_value) for Won opportunities ONLY.
--   Lost opportunities (close_value = 0) are NOT included.
--   Open opportunities (NULL close_value) are NOT included.
--
-- SQL Techniques: CTEs, window functions, PERCENTILE_CONT, date functions
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: Total Revenue Summary
-- ---------------------------------------------------------------------------
SELECT
    COUNT(*)                                                    AS won_deals,
    SUM(close_value)                                            AS total_won_revenue,
    ROUND(AVG(close_value), 2)                                  AS avg_deal_size,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY close_value))::NUMERIC,
        2
    )                                                           AS median_deal_size,
    MIN(close_value)                                            AS min_deal_size,
    MAX(close_value)                                            AS max_deal_size,
    ROUND(STDDEV(close_value)::NUMERIC, 2)                      AS stddev_deal_size
FROM crm_sales.sales_pipeline
WHERE deal_stage = 'Won';

-- ---------------------------------------------------------------------------
-- Query 2: Revenue by Product
-- ---------------------------------------------------------------------------
SELECT
    sp.product,
    p.series,
    p.sales_price                                               AS catalog_price,
    COUNT(*)                                                    AS won_deals,
    SUM(sp.close_value)                                         AS total_revenue,
    ROUND(AVG(sp.close_value), 2)                               AS avg_deal_size,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sp.close_value))::NUMERIC,
        2
    )                                                           AS median_deal_size,
    ROUND(
        SUM(sp.close_value) * 100.0
        / SUM(SUM(sp.close_value)) OVER (),
        2
    )                                                           AS pct_of_total_revenue
FROM crm_sales.sales_pipeline sp
INNER JOIN crm_sales.products p
    ON sp.product = p.product
WHERE sp.deal_stage = 'Won'
GROUP BY sp.product, p.series, p.sales_price
ORDER BY total_revenue DESC;

-- ---------------------------------------------------------------------------
-- Query 3: Revenue by Sales Agent (Top performers)
-- ---------------------------------------------------------------------------
SELECT
    sp.sales_agent,
    st.manager,
    st.regional_office,
    COUNT(*)                                                    AS won_deals,
    SUM(sp.close_value)                                         AS total_revenue,
    ROUND(AVG(sp.close_value), 2)                               AS avg_deal_size,
    ROUND(
        SUM(sp.close_value) * 100.0
        / SUM(SUM(sp.close_value)) OVER (),
        2
    )                                                           AS pct_of_total_revenue,
    -- Cumulative share (for Pareto-style analysis)
    ROUND(
        SUM(SUM(sp.close_value)) OVER (ORDER BY SUM(sp.close_value) DESC)
        * 100.0
        / SUM(SUM(sp.close_value)) OVER (),
        2
    )                                                           AS cumulative_revenue_pct
FROM crm_sales.sales_pipeline sp
INNER JOIN crm_sales.sales_teams st
    ON sp.sales_agent = st.sales_agent
WHERE sp.deal_stage = 'Won'
GROUP BY sp.sales_agent, st.manager, st.regional_office
ORDER BY total_revenue DESC;

-- ---------------------------------------------------------------------------
-- Query 4: Revenue by Sector
-- Uses LEFT JOIN to account defensively for all Won deals.
-- ---------------------------------------------------------------------------
SELECT
    COALESCE(a.sector, 'Unknown / Unassigned Account')          AS sector,
    COUNT(*)                                                    AS won_deals,
    SUM(sp.close_value)                                         AS total_revenue,
    ROUND(AVG(sp.close_value), 2)                               AS avg_deal_size,
    ROUND(
        SUM(sp.close_value) * 100.0
        / SUM(SUM(sp.close_value)) OVER (),
        2
    )                                                           AS pct_of_total_revenue
FROM crm_sales.sales_pipeline sp
LEFT JOIN crm_sales.accounts a
    ON sp.account = a.account
WHERE sp.deal_stage = 'Won'
GROUP BY COALESCE(a.sector, 'Unknown / Unassigned Account')
ORDER BY total_revenue DESC;

-- ---------------------------------------------------------------------------
-- Query 5: Monthly Revenue Over Time
-- Uses close_date for Won deals to show when revenue was realized.
-- ---------------------------------------------------------------------------
SELECT
    DATE_TRUNC('month', close_date)::DATE                       AS revenue_month,
    COUNT(*)                                                    AS won_deals,
    SUM(close_value)                                            AS monthly_revenue,
    ROUND(AVG(close_value), 2)                                  AS avg_deal_size,
    -- Running total
    SUM(SUM(close_value)) OVER (ORDER BY DATE_TRUNC('month', close_date))
                                                                AS cumulative_revenue
FROM crm_sales.sales_pipeline
WHERE deal_stage = 'Won'
GROUP BY DATE_TRUNC('month', close_date)
ORDER BY revenue_month;
