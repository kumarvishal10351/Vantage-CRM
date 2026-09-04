-- ============================================================================
-- 08_sales_funnel.sql
-- Business Question: "What is the stage distribution of the pipeline?"
-- Schema: crm_sales
-- ============================================================================
-- IMPORTANT DISTINCTION:
--   This analysis shows STAGE DISTRIBUTION (a point-in-time snapshot),
--   NOT true cohort conversion rates.
--
--   True cohort conversion requires tracking individual opportunities
--   from one stage to the next over time. This dataset is a snapshot —
--   the 500 Prospecting deals are CURRENT Prospecting deals, not a
--   cohort that started prospecting together.
--
--   The only defensible "conversion" is Won/(Won+Lost), because all
--   closed deals progressed through the pipeline to a terminal state.
--
-- SQL Techniques: CTE, CASE, window functions
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: Stage Distribution (Funnel Shape)
-- ---------------------------------------------------------------------------
WITH stage_counts AS (
    SELECT
        deal_stage,
        COUNT(*)                                                AS stage_count,
        CASE deal_stage
            WHEN 'Prospecting' THEN 1
            WHEN 'Engaging'    THEN 2
            WHEN 'Won'         THEN 3
            WHEN 'Lost'        THEN 4
        END                                                     AS stage_order
    FROM crm_sales.sales_pipeline
    GROUP BY deal_stage
),
totals AS (
    SELECT SUM(stage_count) AS total_opportunities FROM stage_counts
)
SELECT
    sc.deal_stage,
    sc.stage_count,
    ROUND(sc.stage_count * 100.0 / t.total_opportunities, 2)   AS pct_of_total
FROM stage_counts sc
CROSS JOIN totals t
ORDER BY sc.stage_order;

-- ---------------------------------------------------------------------------
-- Query 2: Closed-Deal Conversion Rate (Defensible)
-- Won / (Won + Lost) — the only conversion rate this dataset supports.
-- ---------------------------------------------------------------------------
SELECT
    COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost'))       AS total_closed,
    COUNT(*) FILTER (WHERE deal_stage = 'Won')                  AS won,
    COUNT(*) FILTER (WHERE deal_stage = 'Lost')                 AS lost,
    ROUND(
        COUNT(*) FILTER (WHERE deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                           AS closed_deal_conversion_pct,
    -- For context: what fraction of ALL opportunities resulted in a Win
    ROUND(
        COUNT(*) FILTER (WHERE deal_stage = 'Won') * 100.0
        / COUNT(*),
        2
    )                                                           AS won_pct_of_all_opps
FROM crm_sales.sales_pipeline;

-- ---------------------------------------------------------------------------
-- Query 3: Funnel Stage Summary with Data Completeness
-- Documents what data is available at each stage to explain why
-- true inter-stage conversion cannot be computed.
-- ---------------------------------------------------------------------------
SELECT
    deal_stage,
    COUNT(*)                                                    AS opportunities,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2)        AS pct_of_total,
    -- Data completeness at each stage
    ROUND(COUNT(account)     * 100.0 / COUNT(*), 1)            AS pct_has_account,
    ROUND(COUNT(engage_date) * 100.0 / COUNT(*), 1)            AS pct_has_engage_date,
    ROUND(COUNT(close_date)  * 100.0 / COUNT(*), 1)            AS pct_has_close_date,
    ROUND(COUNT(close_value) * 100.0 / COUNT(*), 1)            AS pct_has_close_value
FROM crm_sales.sales_pipeline
GROUP BY deal_stage
ORDER BY
    CASE deal_stage
        WHEN 'Prospecting' THEN 1
        WHEN 'Engaging'    THEN 2
        WHEN 'Won'         THEN 3
        WHEN 'Lost'        THEN 4
    END;

-- ============================================================================
-- NOTE ON COHORT CONVERSION:
--
-- A true sales funnel conversion analysis requires:
--   1. A cohort of opportunities that entered Prospecting in the same period
--   2. Tracking each opportunity as it moves through stages over time
--   3. Measuring what fraction advance from each stage to the next
--
-- This dataset is a SNAPSHOT. The 500 Prospecting opportunities are
-- currently in Prospecting — they are not a cohort that was tracked.
-- We cannot determine what fraction of prospects became engaged, because
-- engaged deals are currently in Engaging/Won/Lost, not Prospecting.
--
-- The stage counts (500 → 1589 → 4238/2473) do NOT represent a funnel
-- where 500 entered and 4238 made it to Won. Many more opportunities
-- entered Prospecting over the 14-month period and progressed.
-- ============================================================================
