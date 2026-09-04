-- ============================================================================
-- 09_sales_time_analysis.sql
-- Business Question: "How does sales performance trend over time?"
-- Schema: crm_sales
-- ============================================================================
-- Date range: October 2016 — December 2017 (14 months)
-- Uses engage_date for opportunity creation timing and close_date for
-- outcome timing. Monthly aggregation.
--
-- SQL Techniques: DATE_TRUNC, EXTRACT, CTEs, window functions
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: Monthly Opportunities Created (by engage_date)
-- engage_date represents when the deal entered the Engaging stage.
-- Prospecting deals (500) have NULL engage_date and are excluded.
-- ---------------------------------------------------------------------------
SELECT
    DATE_TRUNC('month', engage_date)::DATE                      AS month,
    COUNT(*)                                                    AS opportunities_engaged,
    COUNT(*) FILTER (WHERE deal_stage = 'Won')                  AS eventually_won,
    COUNT(*) FILTER (WHERE deal_stage = 'Lost')                 AS eventually_lost,
    COUNT(*) FILTER (WHERE deal_stage = 'Engaging')             AS still_open
FROM crm_sales.sales_pipeline
WHERE engage_date IS NOT NULL
GROUP BY DATE_TRUNC('month', engage_date)
ORDER BY month;

-- ---------------------------------------------------------------------------
-- Query 2: Monthly Closed Deals & Revenue (by close_date)
-- ---------------------------------------------------------------------------
SELECT
    DATE_TRUNC('month', close_date)::DATE                       AS month,
    COUNT(*)                                                    AS deals_closed,
    COUNT(*) FILTER (WHERE deal_stage = 'Won')                  AS won_deals,
    COUNT(*) FILTER (WHERE deal_stage = 'Lost')                 AS lost_deals,
    SUM(close_value) FILTER (WHERE deal_stage = 'Won')          AS won_revenue,
    ROUND(AVG(close_value) FILTER (WHERE deal_stage = 'Won'), 2) AS avg_won_deal_size,
    -- Win rate per month (only meaningful with sufficient volume)
    ROUND(
        COUNT(*) FILTER (WHERE deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(*), 0),
        2
    )                                                           AS monthly_win_rate_pct
FROM crm_sales.sales_pipeline
WHERE deal_stage IN ('Won', 'Lost')
GROUP BY DATE_TRUNC('month', close_date)
ORDER BY month;

-- ---------------------------------------------------------------------------
-- Query 3: Monthly Win Rate with Volume Context
-- Flags months with fewer than 30 closed deals as potentially unreliable.
-- ---------------------------------------------------------------------------
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', close_date)::DATE                   AS month,
        COUNT(*) FILTER (WHERE deal_stage = 'Won')              AS won,
        COUNT(*) FILTER (WHERE deal_stage = 'Lost')             AS lost,
        COUNT(*)                                                AS closed_total
    FROM crm_sales.sales_pipeline
    WHERE deal_stage IN ('Won', 'Lost')
    GROUP BY DATE_TRUNC('month', close_date)
)
SELECT
    month,
    won,
    lost,
    closed_total,
    ROUND(won * 100.0 / NULLIF(closed_total, 0), 2)            AS win_rate_pct,
    CASE
        WHEN closed_total < 30 THEN 'Low volume — interpret with caution'
        ELSE 'Sufficient volume'
    END                                                         AS reliability_note
FROM monthly
ORDER BY month;

-- ---------------------------------------------------------------------------
-- Query 4: Quarterly Summary
-- Aggregated to quarters for smoother trend view.
-- ---------------------------------------------------------------------------
SELECT
    EXTRACT(YEAR FROM close_date)                               AS year,
    EXTRACT(QUARTER FROM close_date)                            AS quarter,
    COUNT(*)                                                    AS deals_closed,
    COUNT(*) FILTER (WHERE deal_stage = 'Won')                  AS won,
    COUNT(*) FILTER (WHERE deal_stage = 'Lost')                 AS lost,
    ROUND(
        COUNT(*) FILTER (WHERE deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(*), 0),
        2
    )                                                           AS win_rate_pct,
    COALESCE(SUM(close_value) FILTER (WHERE deal_stage = 'Won'), 0)
                                                                AS won_revenue,
    ROUND(AVG(close_value) FILTER (WHERE deal_stage = 'Won'), 2) AS avg_deal_size
FROM crm_sales.sales_pipeline
WHERE deal_stage IN ('Won', 'Lost')
GROUP BY EXTRACT(YEAR FROM close_date), EXTRACT(QUARTER FROM close_date)
ORDER BY year, quarter;
