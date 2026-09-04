-- ============================================================================
-- 10_pipeline_value.sql
-- Business Question: "What is the size and composition of the open pipeline?"
-- Schema: crm_sales
-- ============================================================================
-- IMPORTANT — MONETARY PIPELINE VALUE:
--
--   Monetary pipeline value is NOT directly available in the source dataset.
--   Open opportunities (Prospecting, Engaging) have NULL close_value.
--   There is no "expected_value", "weighted_value", or "probability" field.
--
--   The products table has a catalog sales_price, but multiplying
--   catalog price × opportunity count is NOT defensible because:
--   1. Won deal close_values vary from catalog prices
--   2. There is no documented methodology supporting this calculation
--   3. It would fabricate a metric not present in the source data
--
--   Therefore this analysis provides:
--   - Open opportunity COUNTS (by stage, agent, product)
--   - But NOT fabricated monetary estimates
--
-- SQL Techniques: LEFT JOIN, conditional aggregation, CASE
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: Open Pipeline Summary
-- ---------------------------------------------------------------------------
SELECT
    'Monetary pipeline value is not directly available in the source dataset.'
        AS pipeline_value_note,
    COUNT(*)                                                    AS open_opportunities,
    COUNT(*) FILTER (WHERE deal_stage = 'Prospecting')          AS prospecting,
    COUNT(*) FILTER (WHERE deal_stage = 'Engaging')             AS engaging
FROM crm_sales.sales_pipeline
WHERE deal_stage IN ('Prospecting', 'Engaging');

-- ---------------------------------------------------------------------------
-- Query 2: Open Opportunities by Stage
-- ---------------------------------------------------------------------------
SELECT
    deal_stage,
    COUNT(*)                                                    AS open_count,
    COUNT(account)                                              AS with_account,
    COUNT(*) - COUNT(account)                                   AS without_account,
    COUNT(engage_date)                                          AS with_engage_date
FROM crm_sales.sales_pipeline
WHERE deal_stage IN ('Prospecting', 'Engaging')
GROUP BY deal_stage
ORDER BY
    CASE deal_stage
        WHEN 'Prospecting' THEN 1
        WHEN 'Engaging'    THEN 2
    END;

-- ---------------------------------------------------------------------------
-- Query 3: Open Opportunities by Sales Agent
-- ---------------------------------------------------------------------------
SELECT
    st.sales_agent,
    st.manager,
    st.regional_office,
    COUNT(sp.opportunity_id)                                    AS open_opportunities,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Prospecting')
                                                                AS prospecting,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Engaging')
                                                                AS engaging
FROM crm_sales.sales_teams st
LEFT JOIN crm_sales.sales_pipeline sp
    ON st.sales_agent = sp.sales_agent
    AND sp.deal_stage IN ('Prospecting', 'Engaging')
GROUP BY st.sales_agent, st.manager, st.regional_office
ORDER BY open_opportunities DESC;

-- ---------------------------------------------------------------------------
-- Query 4: Open Opportunities by Product
-- ---------------------------------------------------------------------------
SELECT
    p.product,
    p.series,
    p.sales_price                                               AS catalog_price,
    COUNT(sp.opportunity_id)                                    AS open_opportunities,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Prospecting')
                                                                AS prospecting,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Engaging')
                                                                AS engaging
    -- NOTE: We intentionally do NOT multiply catalog_price × count.
    -- This would fabricate a monetary pipeline value not supported by the data.
FROM crm_sales.products p
LEFT JOIN crm_sales.sales_pipeline sp
    ON p.product = sp.product
    AND sp.deal_stage IN ('Prospecting', 'Engaging')
GROUP BY p.product, p.series, p.sales_price
ORDER BY open_opportunities DESC;

-- ---------------------------------------------------------------------------
-- Query 5: Open Pipeline by Regional Office
-- ---------------------------------------------------------------------------
SELECT
    st.regional_office,
    COUNT(sp.opportunity_id)                                    AS open_opportunities,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Prospecting')
                                                                AS prospecting,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Engaging')
                                                                AS engaging
FROM crm_sales.sales_pipeline sp
INNER JOIN crm_sales.sales_teams st
    ON sp.sales_agent = st.sales_agent
WHERE sp.deal_stage IN ('Prospecting', 'Engaging')
GROUP BY st.regional_office
ORDER BY open_opportunities DESC;
