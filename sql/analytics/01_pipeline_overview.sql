-- ============================================================================
-- 01_pipeline_overview.sql
-- Business Question: "How is the sales pipeline distributed across stages?"
-- Schema: crm_sales
-- ============================================================================
-- Logic:
--   Open  = Prospecting + Engaging (no close_date, no close_value)
--   Closed = Won + Lost (have close_date and close_value)
--   NULL close_value is NOT treated as zero.
--
-- SQL Techniques: Conditional aggregation, CASE, GROUP BY
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: Pipeline Distribution Summary
-- ---------------------------------------------------------------------------
SELECT
    COUNT(*)                                                    AS total_opportunities,
    COUNT(*) FILTER (WHERE deal_stage IN ('Prospecting', 'Engaging'))  AS open_opportunities,
    COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost'))              AS closed_opportunities,
    COUNT(*) FILTER (WHERE deal_stage = 'Prospecting')                 AS prospecting,
    COUNT(*) FILTER (WHERE deal_stage = 'Engaging')                    AS engaging,
    COUNT(*) FILTER (WHERE deal_stage = 'Won')                         AS won,
    COUNT(*) FILTER (WHERE deal_stage = 'Lost')                        AS lost
FROM crm_sales.sales_pipeline;

-- ---------------------------------------------------------------------------
-- Query 2: Stage Distribution with Percentages
-- ---------------------------------------------------------------------------
SELECT
    deal_stage,
    COUNT(*)                                                    AS opportunity_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2)        AS pct_of_total,
    -- Summarize data availability per stage
    COUNT(engage_date)                                          AS has_engage_date,
    COUNT(close_date)                                           AS has_close_date,
    COUNT(close_value)                                          AS has_close_value,
    COUNT(account)                                              AS has_account
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
-- Query 3: Open vs Closed Summary
-- ---------------------------------------------------------------------------
SELECT
    CASE
        WHEN deal_stage IN ('Prospecting', 'Engaging') THEN 'Open'
        WHEN deal_stage IN ('Won', 'Lost')             THEN 'Closed'
    END                                                         AS pipeline_status,
    COUNT(*)                                                    AS opportunity_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2)        AS pct_of_total
FROM crm_sales.sales_pipeline
GROUP BY
    CASE
        WHEN deal_stage IN ('Prospecting', 'Engaging') THEN 'Open'
        WHEN deal_stage IN ('Won', 'Lost')             THEN 'Closed'
    END
ORDER BY pipeline_status;

-- ---------------------------------------------------------------------------
-- Query 4: NULL Audit for Pipeline Fields
-- Verifies expected NULL patterns documented in Phase 2.
-- ---------------------------------------------------------------------------
SELECT
    deal_stage,
    COUNT(*)                                                    AS total,
    SUM(CASE WHEN account     IS NULL THEN 1 ELSE 0 END)      AS null_account,
    SUM(CASE WHEN engage_date IS NULL THEN 1 ELSE 0 END)      AS null_engage_date,
    SUM(CASE WHEN close_date  IS NULL THEN 1 ELSE 0 END)      AS null_close_date,
    SUM(CASE WHEN close_value IS NULL THEN 1 ELSE 0 END)      AS null_close_value
FROM crm_sales.sales_pipeline
GROUP BY deal_stage
ORDER BY
    CASE deal_stage
        WHEN 'Prospecting' THEN 1
        WHEN 'Engaging'    THEN 2
        WHEN 'Won'         THEN 3
        WHEN 'Lost'        THEN 4
    END;
