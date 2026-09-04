-- ============================================================================
-- 02_win_rate.sql
-- Business Question: "What is our win rate overall and by key dimensions?"
-- Schema: crm_sales
-- ============================================================================
-- Definition:
--   Win Rate = Won / (Won + Lost)
--   Denominator: CLOSED opportunities only (deal_stage IN ('Won', 'Lost'))
--   Open opportunities (Prospecting, Engaging) are EXCLUDED.
--
-- SQL Techniques: CTEs, LEFT JOIN, conditional aggregation, FILTER
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: Overall Win Rate
-- ---------------------------------------------------------------------------
SELECT
    COUNT(*) FILTER (WHERE deal_stage = 'Won')                  AS won,
    COUNT(*) FILTER (WHERE deal_stage = 'Lost')                 AS lost,
    COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost'))       AS closed_total,
    ROUND(
        COUNT(*) FILTER (WHERE deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                           AS win_rate_pct
FROM crm_sales.sales_pipeline;

-- ---------------------------------------------------------------------------
-- Query 2: Win Rate by Sales Agent
-- LEFT JOIN ensures agents with zero pipeline activity are included.
-- ---------------------------------------------------------------------------
SELECT
    st.sales_agent,
    st.manager,
    st.regional_office,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost'))
                                                                    AS closed_total,
    CASE
        WHEN COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')) = 0
        THEN NULL  -- No closed deals; win rate is undefined
        ELSE ROUND(
            COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won') * 100.0
            / COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')),
            2
        )
    END                                                             AS win_rate_pct
FROM crm_sales.sales_teams st
LEFT JOIN crm_sales.sales_pipeline sp
    ON st.sales_agent = sp.sales_agent
GROUP BY st.sales_agent, st.manager, st.regional_office
ORDER BY win_rate_pct DESC NULLS LAST;

-- ---------------------------------------------------------------------------
-- Query 3: Win Rate by Product
-- ---------------------------------------------------------------------------
SELECT
    p.product,
    p.series,
    p.sales_price,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost'))
                                                                    AS closed_total,
    ROUND(
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                               AS win_rate_pct
FROM crm_sales.products p
LEFT JOIN crm_sales.sales_pipeline sp
    ON p.product = sp.product
GROUP BY p.product, p.series, p.sales_price
ORDER BY win_rate_pct DESC;

-- ---------------------------------------------------------------------------
-- Query 4: Win Rate by Sector
-- Uses LEFT JOIN to account for all closed opportunities.
-- Note: all closed deals have known accounts, but LEFT JOIN provides defensive handling.
-- ---------------------------------------------------------------------------
SELECT
    COALESCE(a.sector, 'Unknown / Unassigned Account')          AS sector,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost'))
                                                                    AS closed_total,
    ROUND(
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                               AS win_rate_pct
FROM crm_sales.sales_pipeline sp
LEFT JOIN crm_sales.accounts a
    ON sp.account = a.account
WHERE sp.deal_stage IN ('Won', 'Lost')
GROUP BY COALESCE(a.sector, 'Unknown / Unassigned Account')
ORDER BY win_rate_pct DESC;

-- ---------------------------------------------------------------------------
-- Query 5: Win Rate by Regional Office
-- Defensible: regional_office is an attribute of the agent, not the account.
-- All agents have a regional_office, so this is complete for closed deals.
-- ---------------------------------------------------------------------------
SELECT
    st.regional_office,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost'))
                                                                    AS closed_total,
    ROUND(
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                               AS win_rate_pct
FROM crm_sales.sales_pipeline sp
INNER JOIN crm_sales.sales_teams st
    ON sp.sales_agent = st.sales_agent
WHERE sp.deal_stage IN ('Won', 'Lost')
GROUP BY st.regional_office
ORDER BY win_rate_pct DESC;
