-- ============================================================================
-- 05_agent_performance.sql
-- Business Question: "How do sales agents compare across multiple
--                     performance dimensions?"
-- Schema: crm_sales
-- ============================================================================
-- Design:
--   Multi-metric scorecard — no single-metric ranking.
--   LEFT JOIN from sales_teams to include 5 agents with zero activity.
--   Agents with zero closed deals get NULL win rate (not 0%).
--
-- SQL Techniques: LEFT JOIN, CTEs, window functions, conditional aggregation
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Query 1: Agent Performance Scorecard
-- ---------------------------------------------------------------------------
WITH agent_metrics AS (
    SELECT
        st.sales_agent,
        st.manager,
        st.regional_office,

        -- Volume metrics
        COUNT(sp.opportunity_id)                                    AS total_opportunities,
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage IN ('Prospecting', 'Engaging'))
                                                                        AS open,

        -- Revenue metrics (Won only)
        COALESCE(SUM(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won'), 0)
                                                                    AS won_revenue,
        AVG(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won')   AS avg_deal_size,

        -- Cycle metric (closed deals with both dates)
        AVG(sp.close_date - sp.engage_date)
            FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')
                     AND sp.engage_date IS NOT NULL
                     AND sp.close_date  IS NOT NULL)                AS avg_cycle_days

    FROM crm_sales.sales_teams st
    LEFT JOIN crm_sales.sales_pipeline sp
        ON st.sales_agent = sp.sales_agent
    GROUP BY st.sales_agent, st.manager, st.regional_office
)
SELECT
    sales_agent,
    manager,
    regional_office,

    -- Volume
    total_opportunities,
    won,
    lost,
    open,

    -- Win rate (NULL if no closed deals)
    CASE
        WHEN (won + lost) = 0 THEN NULL
        ELSE ROUND(won * 100.0 / (won + lost), 2)
    END                                                             AS win_rate_pct,

    -- Revenue
    won_revenue,
    ROUND(avg_deal_size, 2)                                         AS avg_deal_size,
    ROUND(
        won_revenue * 100.0
        / NULLIF(SUM(won_revenue) OVER (), 0),
        2
    )                                                               AS pct_of_total_revenue,

    -- Cycle
    ROUND(avg_cycle_days, 1)                                        AS avg_cycle_days,

    -- Relative ranking (percentile within all active agents)
    CASE
        WHEN total_opportunities = 0 THEN NULL
        ELSE PERCENT_RANK() OVER (
            ORDER BY won_revenue
        )
    END                                                             AS revenue_percentile_rank

FROM agent_metrics
ORDER BY won_revenue DESC NULLS LAST;

-- ---------------------------------------------------------------------------
-- Query 2: Agent Performance by Manager/Team
-- Aggregated at manager level to compare team performance.
-- ---------------------------------------------------------------------------
SELECT
    st.manager,
    st.regional_office,
    COUNT(DISTINCT st.sales_agent)                              AS agent_count,
    COUNT(sp.opportunity_id)                                    AS total_opportunities,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won')   AS won,
    COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Lost')  AS lost,
    ROUND(
        COUNT(sp.opportunity_id) FILTER (WHERE sp.deal_stage = 'Won') * 100.0
        / NULLIF(COUNT(sp.opportunity_id)
                 FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')), 0),
        2
    )                                                           AS team_win_rate_pct,
    COALESCE(SUM(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won'), 0)
                                                                AS team_revenue,
    ROUND(
        AVG(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won'),
        2
    )                                                           AS avg_deal_size
FROM crm_sales.sales_teams st
LEFT JOIN crm_sales.sales_pipeline sp
    ON st.sales_agent = sp.sales_agent
GROUP BY st.manager, st.regional_office
ORDER BY team_revenue DESC;

-- ---------------------------------------------------------------------------
-- Query 3: Agents with Zero Pipeline Activity
-- Included to document the 5 agents with no opportunities.
-- These should NOT be labeled as poor performers — they may be
-- new hires, departed agents, or data extraction artifacts.
-- ---------------------------------------------------------------------------
SELECT
    st.sales_agent,
    st.manager,
    st.regional_office,
    'No pipeline activity in dataset' AS note
FROM crm_sales.sales_teams st
LEFT JOIN crm_sales.sales_pipeline sp
    ON st.sales_agent = sp.sales_agent
WHERE sp.opportunity_id IS NULL
ORDER BY st.sales_agent;
