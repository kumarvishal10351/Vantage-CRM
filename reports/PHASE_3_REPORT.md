# PHASE 3 REPORT — CRM SQL Analytics & KPI Layer

**Date:** 2026-08-30  
**Status:** PASSED (70/70 validation checks passed)

---

## 1. Executive Summary

Phase 3 successfully built a comprehensive SQL analytics layer on the validated `crm_platform` PostgreSQL database. 17 SQL analytics files covering 10 sales CRM analysis areas and 7 customer intelligence analysis areas were created, executed, and independently validated. All KPIs were cross-checked between SQL and Python, with 70/70 validation checks passing.

Two schemas remain fully independent — zero cross-domain joins exist in any query.

---

## 2. Queries Created

| # | File | Domain | Business Question |
|---|------|--------|-------------------|
| 01 | `01_pipeline_overview.sql` | Sales | How is the pipeline distributed across stages? |
| 02 | `02_win_rate.sql` | Sales | What is our win rate by key dimensions? |
| 03 | `03_revenue_analysis.sql` | Sales | What is our total and segmented won revenue? |
| 04 | `04_sales_cycle.sql` | Sales | How long does it take to close deals? |
| 05 | `05_agent_performance.sql` | Sales | How do agents compare across metrics? |
| 06 | `06_product_performance.sql` | Sales | How do products perform? |
| 07 | `07_account_sector_analysis.sql` | Sales | Which accounts/sectors drive revenue? |
| 08 | `08_sales_funnel.sql` | Sales | What is the pipeline stage distribution? |
| 09 | `09_sales_time_analysis.sql` | Sales | How does performance trend over time? |
| 10 | `10_pipeline_value.sql` | Sales | What is the open pipeline composition? |
| 11 | `11_customer_overview.sql` | Customer | Customer base and churn snapshot |
| 12 | `12_churn_analysis.sql` | Customer | Churn by customer attributes |
| 13 | `13_service_analysis.sql` | Customer | Services associated with churn |
| 14 | `14_billing_analysis.sql` | Customer | Billing patterns and churn |
| 15 | `15_tenure_analysis.sql` | Customer | Tenure relationship to churn |
| 16 | `16_customer_value.sql` | Customer | High vs low value customer profiles |
| 17 | `17_geographic_analysis.sql` | Customer | Geographic distribution (CA only) |

---

## 3. Business Questions Answered

### Sales CRM (10 areas)
1. Pipeline distribution across 4 stages with completeness audit
2. Win rate overall (63.15%) and by agent, product, sector, region
3. Revenue total ($10,005,534), by product, agent, sector, over time
4. Sales cycle duration with outlier investigation
5. Agent performance multi-metric scorecard (including 5 zero-activity agents)
6. Product performance with GTX Pro standardization verified
7. Account and sector analysis with explicit NULL-account handling
8. Sales funnel with clear distinction between stage distribution and cohort conversion
9. Time analysis with monthly/quarterly trends and sparse-month flagging
10. Open pipeline counts (monetary value explicitly documented as unavailable)

### Customer Intelligence (7 areas)
11. Customer overview: 7,043 total, 26.54% snapshot churn rate
12. Churn by 8 customer attributes (contract, internet, payment, tenure, etc.)
13. Service adoption and churn association (6 internet-dependent services)
14. Billing/charges band analysis with churn rates
15. Tenure band analysis (0–6m through 49–72m)
16. Customer value quintiles with churn rates
17. Geographic analysis (California only, limitation documented)

---

## 4. KPI Results (Validated)

### Sales CRM KPIs

| KPI | Value | Validation |
|-----|-------|------------|
| Total Opportunities | 8,800 | SQL = Python |
| Won Opportunities | 4,238 | SQL = Python |
| Lost Opportunities | 2,473 | SQL = Python |
| Open Opportunities | 2,089 | SQL = Python |
| **Win Rate** | **63.15%** | SQL 63.15% = Python 63.15% |
| **Total Won Revenue** | **$10,005,534.00** | SQL = Python |
| **Average Deal Size** | **$2,360.91** | SQL 2360.91 = Python 2360.91 |
| Median Deal Size | $1,117.00 | SQL verified |
| Min Deal Size | $38.00 | SQL verified |
| Max Deal Size | $30,288.00 | SQL verified |
| Lost Revenue | $0.00 | Correct (all Lost = $0) |
| **Avg Sales Cycle** | **47.99 days** | SQL 47.99 = Python 47.99 |
| Won Avg Sales Cycle | 51.8 days | SQL verified |
| Lost Avg Sales Cycle | 41.5 days | SQL verified |
| Won Median Cycle | 57.0 days | SQL verified |
| Lost Median Cycle | 14.0 days | SQL verified |
| Min Cycle | 1 day | SQL verified |
| Max Cycle | 138 days | SQL verified |

### Customer Intelligence KPIs

| KPI | Value | Validation |
|-----|-------|------------|
| Total Customers | 7,043 | SQL = Python |
| Churned Customers | 1,869 | SQL = Python |
| Retained Customers | 5,174 | SQL = Python |
| **Churn Rate (snapshot)** | **26.54%** | SQL 26.54% = Python 26.54% |
| Retention Rate | 73.46% | SQL verified |
| **Average Tenure** | **32.4 months** | SQL verified |
| **Average Monthly Charges** | **$64.76** | SQL verified |
| Average Total Charges | $2,279.73 | SQL verified |

### Win Rate by Product

| Product | Won | Closed | Win Rate |
|---------|-----|--------|----------|
| MG Special | 793 | 1,223 | 64.84% |
| GTX Plus Pro | 479 | 745 | 64.30% |
| GTX Basic | 915 | 1,436 | 63.72% |
| GTX Pro | 729 | 1,147 | 63.56% |
| GTX Plus Basic | 653 | 1,051 | 62.13% |
| MG Advanced | 654 | 1,084 | 60.33% |
| GTK 500 | 15 | 25 | 60.00% |

### Revenue by Product

| Product | Revenue | Won Deals | % of Total |
|---------|---------|-----------|------------|
| GTX Pro | $3,510,578 | 729 | 35.09% |
| GTX Plus Pro | $2,629,651 | 479 | 26.28% |
| MG Advanced | $2,216,387 | 654 | 22.15% |
| GTX Plus Basic | $705,275 | 653 | 7.05% |
| GTX Basic | $499,263 | 915 | 4.99% |
| GTK 500 | $400,612 | 15 | 4.00% |
| MG Special | $43,768 | 793 | 0.44% |

### Churn by Contract

| Contract | Customers | Churned | Churn Rate |
|----------|-----------|---------|------------|
| Month-to-month | 3,875 | 1,655 | 42.71% |
| One year | 1,473 | 166 | 11.27% |
| Two year | 1,695 | 48 | 2.83% |

### Churn by Tenure Band

| Tenure Band | Customers | Churned | Churn Rate |
|-------------|-----------|---------|------------|
| 0–6 months | 1,481 | 784 | 52.94% |
| 7–12 months | 705 | 253 | 35.89% |
| 13–24 months | 1,024 | 294 | 28.71% |
| 25–48 months | 1,594 | 325 | 20.39% |
| 49–72 months | 2,239 | 213 | 9.51% |

---

## 5. Validation Results

### Test Suite: `tests/test_phase3_validation.py`

```
================================================================================
PHASE 3 COMPREHENSIVE VALIDATION
================================================================================

--- 1. SQL File Execution ---
  [PASS] SQL file exists: 01_pipeline_overview.sql
  [PASS] SQL executes successfully: 01_pipeline_overview.sql
  [PASS] SQL file exists: 02_win_rate.sql
  [PASS] SQL executes successfully: 02_win_rate.sql
  [PASS] SQL file exists: 03_revenue_analysis.sql
  [PASS] SQL executes successfully: 03_revenue_analysis.sql
  [PASS] SQL file exists: 04_sales_cycle.sql
  [PASS] SQL executes successfully: 04_sales_cycle.sql
  [PASS] SQL file exists: 05_agent_performance.sql
  [PASS] SQL executes successfully: 05_agent_performance.sql
  [PASS] SQL file exists: 06_product_performance.sql
  [PASS] SQL executes successfully: 06_product_performance.sql
  [PASS] SQL file exists: 07_account_sector_analysis.sql
  [PASS] SQL executes successfully: 07_account_sector_analysis.sql
  [PASS] SQL file exists: 08_sales_funnel.sql
  [PASS] SQL executes successfully: 08_sales_funnel.sql
  [PASS] SQL file exists: 09_sales_time_analysis.sql
  [PASS] SQL executes successfully: 09_sales_time_analysis.sql
  [PASS] SQL file exists: 10_pipeline_value.sql
  [PASS] SQL executes successfully: 10_pipeline_value.sql
  [PASS] SQL file exists: 11_customer_overview.sql
  [PASS] SQL executes successfully: 11_customer_overview.sql
  [PASS] SQL file exists: 12_churn_analysis.sql
  [PASS] SQL executes successfully: 12_churn_analysis.sql
  [PASS] SQL file exists: 13_service_analysis.sql
  [PASS] SQL executes successfully: 13_service_analysis.sql
  [PASS] SQL file exists: 14_billing_analysis.sql
  [PASS] SQL executes successfully: 14_billing_analysis.sql
  [PASS] SQL file exists: 15_tenure_analysis.sql
  [PASS] SQL executes successfully: 15_tenure_analysis.sql
  [PASS] SQL file exists: 16_customer_value.sql
  [PASS] SQL executes successfully: 16_customer_value.sql
  [PASS] SQL file exists: 17_geographic_analysis.sql
  [PASS] SQL executes successfully: 17_geographic_analysis.sql

--- 2. Opportunity Count Cross-Check ---
  [PASS] Total opportunities = 8800 (got 8800)
  [PASS] Won opportunities = 4238 (got 4238)
  [PASS] Lost opportunities = 2473 (got 2473)
  [PASS] Prospecting opportunities = 500 (got 500)
  [PASS] Engaging opportunities = 1589 (got 1589)
  [PASS] Open opportunities = 2089 (got 2089)
  [PASS] Closed opportunities = 6711 (got 6711)
  [PASS] Sum of stages = total (got 8800)

--- 3. Win Rate Cross-Check ---
  [PASS] SQL win rate = 63.15%, Python win rate = 63.15%
  [PASS] Win rate denominator excludes open deals (denom=6711, not 8800)

--- 4. Won Revenue Cross-Check ---
  [PASS] SQL won revenue = 10005534.0, Python = 10005534.0
  [PASS] SQL avg deal size = 2360.91, Python = 2360.91
  [PASS] Lost revenue = $0 (got $0.0)
  [PASS] Open deals with non-NULL close_value = 0 (got 0)

--- 5. Sales Cycle Cross-Check ---
  [PASS] Sales cycle computed on 6711 closed deals (expected 6711)
  [PASS] Min cycle >= 0 days (got 1)
  [PASS] Max cycle is reasonable (got 138 days)
  [PASS] SQL avg cycle = 47.99, Python = 47.99
  [PASS] No negative sales cycles (got 0)

--- 6. Customer Churn Cross-Check ---
  [PASS] Total customers = 7043 (got 7043)
  [PASS] Churned customers = 1869 (got 1869)
  [PASS] Retained customers = 5174 (got 5174)
  [PASS] Churned + Retained = Total (1869 + 5174 = 7043)
  [PASS] SQL churn rate = 26.54%, Python = 26.54%
  [PASS] Churn label/value consistency (mismatches=0)

--- 7. NULL Handling ---
  [PASS] NULL accounts = 1425 (got 1425)
  [PASS] NULL engage_date = 500 (got 500)
  [PASS] NULL close_date = 2089 (got 2089)
  [PASS] NULL close_value = 2089 (got 2089)
  [PASS] No NULL close_value in Won/Lost (got 0)

--- 8. Duplicate Check ---
  [PASS] No duplicate opportunity_ids (dupes=0)
  [PASS] No duplicate customer_ids (dupes=0)

--- 9. Cross-Domain Join Check ---
  [PASS] No cross-domain joins in any SQL file

--- 10. Reference Integrity ---
  [PASS] 30 active agents in pipeline, 35 total in teams (pipeline=30, teams=35)
  [PASS] 7 products in pipeline (got 7)
  [PASS] GTXPro standardized to GTX Pro (GTXPro=0, GTX Pro=1480)

================================================================================
TOTAL: 70 PASSED, 0 FAILED out of 70 validation checks.
================================================================================
```

### Validation Categories

| Category | Checks | Result |
|----------|--------|--------|
| SQL file existence | 17 | 17/17 PASS |
| SQL execution | 17 | 17/17 PASS |
| Opportunity counts | 8 | 8/8 PASS |
| Win rate cross-check | 2 | 2/2 PASS |
| Revenue cross-check | 4 | 4/4 PASS |
| Sales cycle cross-check | 5 | 5/5 PASS |
| Customer churn cross-check | 6 | 6/6 PASS |
| NULL handling | 5 | 5/5 PASS |
| Duplicate check | 2 | 2/2 PASS |
| Cross-domain join check | 1 | 1/1 PASS |
| Reference integrity | 3 | 3/3 PASS |
| **Total** | **70** | **70/70 PASS** |

---

## 6. Important Findings

### Sales CRM

1. **Win rate is 63.15%** — consistent across products (60–65%), regions (62.6–63.9%), indicating systemic effectiveness rather than product-specific or region-specific factors.

2. **Revenue concentration** — 3 products (GTX Pro, GTX Plus Pro, MG Advanced) generate 83.5% of total won revenue. MG Special generates the most deals (793) but only 0.44% of revenue.

3. **Lost deals close faster** — median 14 days vs. 57 days for Won. Quick losses may indicate effective qualification.

4. **Mean-median deal size gap** — $2,361 mean vs. $1,117 median. Revenue distribution is positively skewed with some very large deals pulling the average up.

5. **5 agents with zero pipeline activity** — present in the teams table but have no opportunities. May be new hires, departed agents, or data extraction artifacts.

6. **1,425 NULL-account opportunities** — all in early stages (Prospecting/Engaging), consistent with CRM workflow where accounts are identified after initial contact.

7. **Monetary pipeline value unavailable** — open deals have NULL close_value, and no probability/expected value field exists. This is documented, not fabricated.

### Customer Intelligence

8. **Month-to-month contracts show 42.71% churn** — vs. 2.83% for two-year contracts. The strongest single attribute differentiator.

9. **New customers (0–6 months) churn at 52.94%** — the first 6 months is a critical retention window. Churn decreases monotonically with tenure.

10. **Electronic check payment method shows 45.29% churn** — nearly 3x the rate of automatic payment methods (~15–17%).

11. **Fiber optic service shows 41.89% churn** — vs. 18.96% for DSL and 7.40% for no internet.

12. **Senior citizens churn at 41.68%** — vs. 23.61% for non-seniors.

---

## 7. Limitations

| Limitation | Impact |
|-----------|--------|
| Sales data covers 14 months only | Year-over-year trends impossible |
| Snapshot data — open deals never close | True win rate may differ from 63.15% |
| No cost/profitability data | Revenue ≠ profit |
| No lead source data | Cannot analyze acquisition channels |
| Churn rate is snapshot, not time-based | Cannot compute monthly/annual churn |
| Customer data is California only | Geographic insights limited |
| No multi-touch opportunity tracking | Cannot analyze engagement patterns |
| Two domains are independent | Cannot link sales to customer data |
| All analysis is descriptive | Correlation ≠ causation |
| Source CLTV is target-derived | Cannot be used for independent prediction |

---

## 8. Anomalies Discovered

1. **GTK 500 low volume** — Only 25 closed deals (15 won) but $400,612 in revenue (4.00% of total). The highest-priced product ($26,768 catalog) has very few opportunities but significant per-deal revenue. Its 60.00% win rate is not statistically reliable with N=25.

2. **Large deal size variance** — Won deals range from $38 to $30,288, a 797x spread. The standard deviation ($2,544.48) exceeds the mean ($2,360.91), indicating high variance. This is driven by the product mix from $55 (MG Special) to $26,768 (GTK 500).

3. **Sales cycle maximum is 138 days** — consistent across Won and Lost. This aligns with a ~4.5 month maximum engagement window and appears to be a natural ceiling rather than an outlier.

4. **11 zero-tenure customers** — have total_charges = $0.00. These were handled in Phase 2 (imputed from blank strings) and are factually correct — customers who signed up and immediately churned.

---

## 9. Files Created & Modified

| File | Purpose |
|------|---------|
| `sql/analytics/01_pipeline_overview.sql` | Pipeline stage distribution |
| `sql/analytics/02_win_rate.sql` | Win rate by multiple dimensions |
| `sql/analytics/03_revenue_analysis.sql` | Won revenue with medians and time series |
| `sql/analytics/04_sales_cycle.sql` | Sales cycle with outlier investigation |
| `sql/analytics/05_agent_performance.sql` | Multi-metric agent scorecard |
| `sql/analytics/06_product_performance.sql` | Product performance dashboard |
| `sql/analytics/07_account_sector_analysis.sql` | Account and sector analysis |
| `sql/analytics/08_sales_funnel.sql` | Stage distribution (not cohort conversion) |
| `sql/analytics/09_sales_time_analysis.sql` | Monthly/quarterly trends |
| `sql/analytics/10_pipeline_value.sql` | Open pipeline counts (no fabricated $) |
| `sql/analytics/11_customer_overview.sql` | Customer base and churn snapshot |
| `sql/analytics/12_churn_analysis.sql` | Churn by 8 attributes |
| `sql/analytics/13_service_analysis.sql` | Service adoption and churn |
| `sql/analytics/14_billing_analysis.sql` | Billing patterns and churn |
| `sql/analytics/15_tenure_analysis.sql` | Tenure bands and churn |
| `sql/analytics/16_customer_value.sql` | Value quintiles and CLTV reference |
| `sql/analytics/17_geographic_analysis.sql` | Geographic distribution (CA only) |
| `docs/crm_kpi_definitions.md` | Formal KPI definitions |
| `docs/sql_analytics_guide.md` | SQL usage guide and design decisions |
| `docs/business_insights.md` | 13 descriptive insights |
| `tests/test_phase3_validation.py` | 70-check validation suite |
| `reports/PHASE_3_REPORT.md` | This report |

---

## 10. SQL Techniques Demonstrated

| Technique | Example Files |
|-----------|---------------|
| `INNER JOIN` | 02, 03, 04, 07, 09 |
| `LEFT JOIN` | 02, 05, 06, 07, 10 |
| `GROUP BY` | All 17 files |
| `CASE` expressions | 01, 08, 12, 14, 15, 16 |
| CTEs (`WITH`) | 04, 05, 08, 16, 17 |
| Window functions (`OVER`) | 03, 05, 06, 07, 09, 15 |
| `PERCENTILE_CONT` | 03, 04, 11, 14, 15, 16 |
| `NTILE` | 16 |
| Date functions (`DATE_TRUNC`, `EXTRACT`) | 03, 09 |
| Conditional aggregation (`FILTER`) | All files |
| `PERCENT_RANK` | 05 |
| `MODE()` | 16 |

---

## 11. Reproducibility

```bash
# Run all analytics SQL
for f in sql/analytics/*.sql; do psql -d crm_platform -f "$f"; done

# Run validation
python -m tests.test_phase3_validation
```

---

## Conclusion

Phase 3 is complete and fully validated. The SQL analytics layer provides a comprehensive, correct, and well-documented foundation for business analysis across both CRM domains. All KPIs are independently verified, NULL handling is explicit, no fabricated metrics exist, and business interpretations are appropriately cautious.

**Phase 3 status: PASSED. Awaiting instruction for Phase 4.**
