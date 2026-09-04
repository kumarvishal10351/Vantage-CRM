# SQL Analytics Guide

**Domain:** B2B Sales CRM & Pipeline Management  
**Database:** `crm_platform` (PostgreSQL)  
**Schema:** `crm_sales`  

---

## File Organization

All analytical SQL scripts are located in `sql/analytics/`:

| # | File | Domain | Business Question |
|---|------|--------|-------------------|
| 01 | `01_pipeline_overview.sql` | Sales Pipeline | How is the pipeline distributed across stages (count, open vs. closed)? |
| 02 | `02_win_rate.sql` | Sales Performance | What is the overall and segmented win rate across products, agents, sectors? |
| 03 | `03_revenue_analysis.sql` | Revenue & Pricing | What is total won revenue, average deal size, distribution, and product contribution? |
| 04 | `04_sales_cycle.sql` | Velocity | How long does it take to close deals (Won vs. Lost, product, sector)? |
| 05 | `05_agent_performance.sql` | Sales Reps | How do individual sales reps compare in volume, win rate, revenue, and deal size? |
| 06 | `06_product_performance.sql` | Products | How do products perform in volume, win rate, revenue, and list price realization? |
| 07 | `07_account_sector_analysis.sql` | Accounts & Sectors | Which enterprise accounts and industry sectors drive the most won revenue? |
| 08 | `08_sales_funnel.sql` | Funnel Conversion | What is the stage-by-stage conversion distribution through the sales pipeline? |
| 09 | `09_sales_time_analysis.sql` | Temporal Trends | How does performance, deal volume, and won revenue trend over time? |
| 10 | `10_pipeline_value.sql` | Pipeline Health | What is the composition and stage progression of currently open opportunities? |

---

## How to Run

Each file contains standalone, modular analytical queries separated by semicolons. Execute them against the `crm_platform` database:

```bash
# Run a single analytics file
psql -d crm_platform -U postgres -f sql/analytics/01_pipeline_overview.sql

# Run all sales analytics files in order
for f in sql/analytics/*.sql; do psql -d crm_platform -U postgres -f "$f"; done
```

Or execute them through the automated verification test suite:
```bash
pytest tests/test_phase3_validation.py -v
```

---

## SQL Techniques Demonstrated

| Technique | Where Used | Purpose |
|-----------|-----------|---------|
| `INNER JOIN` | Win rate by sector (02), Revenue by product (03) | Relate pipeline deals to dimension tables |
| `LEFT JOIN` | Agent scorecard (05), Product performance (06) | Retain all 35 sales agents, including those with zero pipeline deals |
| `GROUP BY` | All analytics files | Multi-dimensional aggregation |
| `CASE` | Age bands, stage ordering, deal sizing tiers | Categorical segmentation |
| `CTEs` | Sales cycle (04), Agent scorecard (05), Funnel (08) | Modular, readable multi-step queries |
| `Window functions` | Revenue share (03), Percentile rank (05), Cumulative revenue (03) | Analytical row calculations and rankings |
| `Date functions` | Time analysis (09): `DATE_TRUNC`, `EXTRACT` | Monthly/quarterly aggregation and seasonality |
| `Conditional aggregation` | `COUNT(*) FILTER (WHERE ...)` throughout | Stage-specific counting without subqueries |
| `PERCENTILE_CONT` | Revenue median (03), Sales cycle median (04) | Robust central tendency metrics resistant to outliers |

---

## Key Design Decisions & Business Rules

### 1. Win Rate Denominator
Win rate uses **strictly closed deals** (Won + Lost = 6,711). Open deals (2,089) are excluded from the denominator:
$$\text{Win Rate} = \frac{\text{Won Deals}}{\text{Won Deals} + \text{Lost Deals}} = \frac{4,238}{6,711} = 63.15\%$$

### 2. Revenue Definition
Revenue is defined strictly as `SUM(close_value)` for deals where `deal_stage = 'Won'` ($10,005,534.00). Lost deals have `close_value = 0` by definition. Open deals have `NULL close_value`.

### 3. Open Pipeline Handling
Open opportunities (Prospecting and Engaging) have `NULL close_value` in the raw dataset. Monetary close values are **never fabricated or imputed**. Open pipeline tracking is based on actual opportunity volume, stage progression, aging duration, and deterministic prioritization tiers.

### 4. Sales Cycle Calculation
Sales cycle duration is defined as `close_date - engage_date` in days. It is computed for closed deals having both dates populated. Prospecting deals (which lack `engage_date`) are excluded from engagement-to-close cycle metrics.

### 5. Sales Agent Inclusivity
A `LEFT JOIN` from `sales_teams` to `sales_pipeline` guarantees all 35 sales agents are included in reporting, properly reflecting the 5 agents with zero pipeline activity rather than omitting them.
