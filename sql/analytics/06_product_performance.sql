-- ============================================================================
-- 06_product_performance.sql
-- Business Question: "How do products perform in terms of volume,
--                     win rate, and revenue?"
-- Schema: crm_sales
-- ============================================================================
-- Notes:
--   "GTXPro" was standardized to "GTX Pro" in Phase 2 data cleaning.
--   All 7 products from the catalog are included via LEFT JOIN.
--
-- SQL Techniques: LEFT JOIN, conditional aggregation, window functions
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: Product Performance Summary
-- ---------------------------------------------------------------------------
SELECT
    p.product,
    p.series,
    p.sales_price                                               AS catalog_price,

    -- Volume
    COUNT(sp.opportunity_id)                                    AS total_opportunities,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Prospecting', 'Engaging'))
                                                                    AS open,

    -- Win rate
    ROUND(
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(sp.opportunity_id)
                 FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                           AS win_rate_pct,

    -- Revenue (Won only)
    COALESCE(SUM(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won'), 0)
                                                                AS won_revenue,
    ROUND(
        AVG(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won'),
        2
    )                                                           AS avg_deal_size,

    -- Revenue share
    ROUND(
        COALESCE(SUM(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won'), 0)
        * 100.0
        / NULLIF(SUM(
            COALESCE(SUM(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won'), 0)
        ) OVER (), 0),
        2
    )                                                           AS pct_of_won_revenue,

    -- Average close_value vs catalog price (for Won deals)
    ROUND(
        AVG(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won') - p.sales_price,
        2
    )                                                           AS avg_deviation_from_catalog

FROM crm_sales.products p
LEFT JOIN crm_sales.sales_pipeline sp
    ON p.product = sp.product
GROUP BY p.product, p.series, p.sales_price
ORDER BY won_revenue DESC;

-- ---------------------------------------------------------------------------
-- Query 2: Product Win Rate vs Volume Scatter Data
-- Useful for identifying products with high volume but low win rate
-- or vice versa.
-- ---------------------------------------------------------------------------
SELECT
    product,
    COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost'))       AS closed_deals,
    COUNT(*) FILTER (WHERE deal_stage = 'Won')                  AS won_deals,
    ROUND(
        COUNT(*) FILTER (WHERE deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                           AS win_rate_pct,
    COALESCE(SUM(close_value) FILTER (WHERE deal_stage = 'Won'), 0)
                                                                AS won_revenue
FROM crm_sales.sales_pipeline
GROUP BY product
ORDER BY closed_deals DESC;

-- ---------------------------------------------------------------------------
-- Query 3: GTX Pro Standardization Verification
-- Confirms the Phase 2 fix: "GTXPro" → "GTX Pro".
-- ---------------------------------------------------------------------------
SELECT
    product,
    COUNT(*) AS opportunity_count
FROM crm_sales.sales_pipeline
WHERE product ILIKE '%gtx%pro%'
GROUP BY product;
