-- ============================================================================
-- 04_sales_cycle.sql
-- Business Question: "How long does it take to close deals?"
-- Schema: crm_sales
-- ============================================================================
-- Definition:
--   Sales Cycle = close_date - engage_date (in days)
--   Only for closed opportunities (Won, Lost) where BOTH dates exist.
--
-- IMPORTANT METHODOLOGICAL NOTES:
--   - This measures the observed engagement-to-close duration, NOT the
--     complete lead-to-close sales cycle.
--   - Prospecting opportunities may have NULL engage_date.
--   - Do not impute missing engage dates.
--   - Do not imply that this is the total customer acquisition cycle.
--   - Open deals have NULL close_date -> excluded.
--
-- SQL Techniques: CTEs, date arithmetic, PERCENTILE_CONT, window functions
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: Overall Sales Cycle Statistics & Eligibility Audit
-- Reports total closed, eligible closed, excluded (missing engage_date),
-- average, median, min, max, and percentiles.
-- ---------------------------------------------------------------------------
WITH closed_deals AS (
    SELECT
        opportunity_id,
        deal_stage,
        engage_date,
        close_date,
        CASE
            WHEN engage_date IS NOT NULL AND close_date IS NOT NULL
            THEN (close_date - engage_date)
            ELSE NULL
        END AS cycle_days
    FROM crm_sales.sales_pipeline
    WHERE deal_stage IN ('Won', 'Lost')
)
SELECT
    COUNT(*)                                                    AS total_closed_opportunities,
    COUNT(cycle_days)                                           AS eligible_closed_opportunities,
    COUNT(*) - COUNT(cycle_days)                                AS excluded_missing_engage_date,
    ROUND(AVG(cycle_days), 1)                                   AS avg_cycle_days,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cycle_days))::NUMERIC,
        1
    )                                                           AS median_cycle_days,
    MIN(cycle_days)                                             AS min_cycle_days,
    MAX(cycle_days)                                             AS max_cycle_days,
    ROUND(STDDEV(cycle_days)::NUMERIC, 1)                       AS stddev_cycle_days,
    -- Percentiles for distribution insight
    ROUND(
        (PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY cycle_days))::NUMERIC,
        1
    )                                                           AS p25_cycle_days,
    ROUND(
        (PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY cycle_days))::NUMERIC,
        1
    )                                                           AS p75_cycle_days
FROM closed_deals;

-- ---------------------------------------------------------------------------
-- Query 2: Sales Cycle by Outcome (Won vs Lost)
-- ---------------------------------------------------------------------------
WITH cycle_data AS (
    SELECT
        deal_stage,
        (close_date - engage_date) AS cycle_days
    FROM crm_sales.sales_pipeline
    WHERE deal_stage IN ('Won', 'Lost')
      AND engage_date IS NOT NULL
      AND close_date  IS NOT NULL
)
SELECT
    deal_stage,
    COUNT(*)                                                    AS deals,
    ROUND(AVG(cycle_days), 1)                                   AS avg_cycle_days,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cycle_days))::NUMERIC,
        1
    )                                                           AS median_cycle_days,
    MIN(cycle_days)                                             AS min_cycle_days,
    MAX(cycle_days)                                             AS max_cycle_days
FROM cycle_data
GROUP BY deal_stage
ORDER BY deal_stage;

-- ---------------------------------------------------------------------------
-- Query 3: Sales Cycle by Sales Agent
-- ---------------------------------------------------------------------------
WITH cycle_data AS (
    SELECT
        sp.sales_agent,
        st.regional_office,
        sp.deal_stage,
        (sp.close_date - sp.engage_date) AS cycle_days
    FROM crm_sales.sales_pipeline sp
    INNER JOIN crm_sales.sales_teams st
        ON sp.sales_agent = st.sales_agent
    WHERE sp.deal_stage IN ('Won', 'Lost')
      AND sp.engage_date IS NOT NULL
      AND sp.close_date  IS NOT NULL
)
SELECT
    sales_agent,
    regional_office,
    COUNT(*)                                                    AS closed_deals,
    COUNT(*) FILTER (WHERE deal_stage = 'Won')                  AS won_deals,
    ROUND(AVG(cycle_days), 1)                                   AS avg_cycle_days,
    ROUND(AVG(cycle_days) FILTER (WHERE deal_stage = 'Won'), 1) AS avg_won_cycle_days,
    ROUND(AVG(cycle_days) FILTER (WHERE deal_stage = 'Lost'), 1) AS avg_lost_cycle_days,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cycle_days))::NUMERIC,
        1
    )                                                           AS median_cycle_days
FROM cycle_data
GROUP BY sales_agent, regional_office
ORDER BY avg_cycle_days;

-- ---------------------------------------------------------------------------
-- Query 4: Sales Cycle by Product
-- ---------------------------------------------------------------------------
WITH cycle_data AS (
    SELECT
        sp.product,
        sp.deal_stage,
        (sp.close_date - sp.engage_date) AS cycle_days
    FROM crm_sales.sales_pipeline sp
    WHERE sp.deal_stage IN ('Won', 'Lost')
      AND sp.engage_date IS NOT NULL
      AND sp.close_date  IS NOT NULL
)
SELECT
    product,
    COUNT(*)                                                    AS closed_deals,
    ROUND(AVG(cycle_days), 1)                                   AS avg_cycle_days,
    ROUND(AVG(cycle_days) FILTER (WHERE deal_stage = 'Won'), 1) AS avg_won_cycle_days,
    ROUND(AVG(cycle_days) FILTER (WHERE deal_stage = 'Lost'), 1) AS avg_lost_cycle_days,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cycle_days))::NUMERIC,
        1
    )                                                           AS median_cycle_days
FROM cycle_data
GROUP BY product
ORDER BY avg_cycle_days;

-- ---------------------------------------------------------------------------
-- Query 5: Investigate Unusually Large Sales Cycles
-- Shows deals with cycle > mean + 2*stddev or > 120 days
-- ---------------------------------------------------------------------------
WITH cycle_stats AS (
    SELECT
        AVG(close_date - engage_date)    AS mean_days,
        STDDEV(close_date - engage_date) AS stddev_days
    FROM crm_sales.sales_pipeline
    WHERE deal_stage IN ('Won', 'Lost')
      AND engage_date IS NOT NULL
      AND close_date  IS NOT NULL
)
SELECT
    sp.opportunity_id,
    sp.sales_agent,
    sp.product,
    sp.account,
    sp.deal_stage,
    sp.engage_date,
    sp.close_date,
    (sp.close_date - sp.engage_date)                            AS cycle_days,
    sp.close_value
FROM crm_sales.sales_pipeline sp, cycle_stats cs
WHERE sp.deal_stage IN ('Won', 'Lost')
  AND sp.engage_date IS NOT NULL
  AND sp.close_date  IS NOT NULL
  AND (sp.close_date - sp.engage_date) > (cs.mean_days + 2 * cs.stddev_days)
ORDER BY (sp.close_date - sp.engage_date) DESC
LIMIT 20;

-- ---------------------------------------------------------------------------
-- Query 6: Sales Cycle Distribution (Histogram Buckets)
-- ---------------------------------------------------------------------------
SELECT
    CASE
        WHEN (close_date - engage_date) BETWEEN 0  AND 14  THEN '00-14 days'
        WHEN (close_date - engage_date) BETWEEN 15 AND 30  THEN '15-30 days'
        WHEN (close_date - engage_date) BETWEEN 31 AND 60  THEN '31-60 days'
        WHEN (close_date - engage_date) BETWEEN 61 AND 90  THEN '61-90 days'
        WHEN (close_date - engage_date) BETWEEN 91 AND 120 THEN '91-120 days'
        WHEN (close_date - engage_date) > 120              THEN '121+ days'
    END                                                         AS cycle_band,
    COUNT(*)                                                    AS deals,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2)        AS pct_of_total,
    COUNT(*) FILTER (WHERE deal_stage = 'Won')                  AS won,
    COUNT(*) FILTER (WHERE deal_stage = 'Lost')                 AS lost
FROM crm_sales.sales_pipeline
WHERE deal_stage IN ('Won', 'Lost')
  AND engage_date IS NOT NULL
  AND close_date  IS NOT NULL
GROUP BY cycle_band
ORDER BY cycle_band;
