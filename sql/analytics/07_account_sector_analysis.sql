
-- ============================================================================
-- 07_account_sector_analysis.sql
-- Business Question: "Which accounts and sectors drive the most
--                     volume and revenue?"
-- Schema: crm_sales
-- ============================================================================
-- IMPORTANT:
--   1,425 opportunities have NULL account (early-stage). These are NOT
--   silently discarded — they are explicitly counted.
--   Only closed deals (Won, Lost) have non-NULL accounts.
--
-- SQL Techniques: LEFT JOIN, CTEs, conditional aggregation, window functions
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: NULL Account Audit
-- Shows how many opportunities have no account, by stage.
-- ---------------------------------------------------------------------------
SELECT
    deal_stage,
    COUNT(*)                                                    AS total,
    COUNT(account)                                              AS with_account,
    COUNT(*) - COUNT(account)                                   AS null_account,
    ROUND(
        (COUNT(*) - COUNT(account)) * 100.0 / COUNT(*),
        2
    )                                                           AS pct_null
FROM crm_sales.sales_pipeline
GROUP BY deal_stage
ORDER BY
    CASE deal_stage
        WHEN 'Prospecting' THEN 1
        WHEN 'Engaging'    THEN 2
        WHEN 'Won'         THEN 3
        WHEN 'Lost'        THEN 4
    END;

-- ---------------------------------------------------------------------------
-- Query 2: Top Accounts by Won Revenue
-- ---------------------------------------------------------------------------
SELECT
    sp.account,
    a.sector,
    a.office_location,
    a.revenue                                                   AS account_annual_revenue,
    a.employees,
    COUNT(sp.opportunity_id)                                    AS total_opportunities,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
    ROUND(
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(sp.opportunity_id)
                 FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                           AS win_rate_pct,
    COALESCE(SUM(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won'), 0)
                                                                AS won_revenue,
    ROUND(
        AVG(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won'),
        2
    )                                                           AS avg_deal_size
FROM crm_sales.sales_pipeline sp
INNER JOIN crm_sales.accounts a
    ON sp.account = a.account
GROUP BY sp.account, a.sector, a.office_location, a.revenue, a.employees
ORDER BY won_revenue DESC
LIMIT 20;

-- ---------------------------------------------------------------------------
-- Query 3: Sector Analysis — Opportunity Volume
-- Uses LEFT JOIN so all 8,800 opportunities are accounted for,
-- explicitly labeling NULL accounts as 'Unknown / Unassigned Account'.
-- ---------------------------------------------------------------------------
SELECT
    COALESCE(a.sector, 'Unknown / Unassigned Account')          AS sector,
    COUNT(sp.opportunity_id)                                    AS total_opportunities,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Prospecting', 'Engaging'))
                                                                    AS open,
    ROUND(
        COUNT(sp.opportunity_id) * 100.0
        / SUM(COUNT(sp.opportunity_id)) OVER (),
        2
    )                                                           AS pct_of_total_opps
FROM crm_sales.sales_pipeline sp
LEFT JOIN crm_sales.accounts a
    ON sp.account = a.account
GROUP BY COALESCE(a.sector, 'Unknown / Unassigned Account')
ORDER BY total_opportunities DESC;

-- ---------------------------------------------------------------------------
-- Query 4: Sector Analysis — Win Rate
-- Uses LEFT JOIN and NULLIF to prevent division by zero.
-- ---------------------------------------------------------------------------
SELECT
    COALESCE(a.sector, 'Unknown / Unassigned Account')          AS sector,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost'))
                                                                    AS closed_total,
    ROUND(
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(sp.opportunity_id)
                 FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                           AS win_rate_pct
FROM crm_sales.sales_pipeline sp
LEFT JOIN crm_sales.accounts a
    ON sp.account = a.account
WHERE sp.deal_stage IN ('Won', 'Lost')
GROUP BY COALESCE(a.sector, 'Unknown / Unassigned Account')
ORDER BY win_rate_pct DESC;

-- ---------------------------------------------------------------------------
-- Query 5: Sector Analysis — Revenue
-- ---------------------------------------------------------------------------
SELECT
    COALESCE(a.sector, 'Unknown / Unassigned Account')          AS sector,
    COUNT(sp.opportunity_id)                                    AS won_deals,
    SUM(sp.close_value)                                         AS sector_revenue,
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
ORDER BY sector_revenue DESC;

-- ---------------------------------------------------------------------------
-- Query 6: Accounts with No Pipeline Activity
-- Accounts that exist in the accounts table but have no associated deals.
-- ---------------------------------------------------------------------------
SELECT
    a.account,
    a.sector,
    a.office_location,
    a.revenue                                                   AS account_annual_revenue
FROM crm_sales.accounts a
LEFT JOIN crm_sales.sales_pipeline sp
    ON a.account = sp.account
WHERE sp.opportunity_id IS NULL
ORDER BY a.account;
