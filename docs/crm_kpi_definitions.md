# CRM KPI Definitions

**Version:** 1.0
**Phase:** 3 — SQL Analytics & KPI Layer
**Database:** crm_platform (PostgreSQL)

---

## Sales CRM KPIs (Schema: crm_sales)

---

### 1. Win Rate

| Attribute | Detail |
|-----------|--------|
| **Business Definition** | The percentage of closed deals that resulted in a successful outcome (Won). |
| **SQL Formula** | `COUNT(*) FILTER (WHERE deal_stage = 'Won') * 100.0 / COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost'))` |
| **Denominator** | Total closed opportunities (Won + Lost). Open deals (Prospecting, Engaging) are excluded. |
| **Source Table** | `crm_sales.sales_pipeline` |
| **Why It Matters** | Win rate measures sales effectiveness. A declining win rate may indicate competitive pressure, poor qualification, or pricing issues. |
| **Limitations** | (1) Calculated on a dataset snapshot — the 2,089 open deals at extraction will never close in this dataset. (2) Does not account for deal quality, size, or effort. A 100% win rate on small deals may be less valuable than a 50% win rate on large deals. (3) Based on a 14-month window (Oct 2016 – Dec 2017). |

---

### 2. Won Revenue (Total)

| Attribute | Detail |
|-----------|--------|
| **Business Definition** | Total revenue from successfully closed deals. |
| **SQL Formula** | `SUM(close_value) WHERE deal_stage = 'Won'` |
| **Denominator** | N/A (this is a sum, not a rate). |
| **Source Table** | `crm_sales.sales_pipeline` (`close_value` column) |
| **Why It Matters** | Primary measure of sales output. Tracks total business generated. |
| **Limitations** | (1) Lost deals contribute $0 (correct, not a data issue). (2) Open deals have NULL close_value — their potential revenue is unknown. (3) No cost data is available, so profitability cannot be determined. |

---

### 3. Average Deal Size

| Attribute | Detail |
|-----------|--------|
| **Business Definition** | The average revenue per successfully closed deal. |
| **SQL Formula** | `AVG(close_value) WHERE deal_stage = 'Won'` |
| **Denominator** | Count of Won deals. |
| **Source Table** | `crm_sales.sales_pipeline` (`close_value` column) |
| **Why It Matters** | Indicates deal quality. A rising average deal size suggests movement upmarket or improved negotiation. |
| **Limitations** | (1) Sensitive to outliers — a few very large or small deals skew the mean. Use median for comparison. (2) Lost deals are excluded because their close_value = 0 by definition. (3) Does not account for product mix changes over time. |

---

### 4. Sales Cycle (Days)

| Attribute | Detail |
|-----------|--------|
| **Business Definition** | The number of calendar days from deal engagement to close. |
| **SQL Formula** | `close_date - engage_date` (in days), for closed deals where both dates exist. |
| **Denominator** | Count of eligible closed deals with non-NULL engage_date and close_date (6,711). |
| **Source Table** | `crm_sales.sales_pipeline` (`engage_date`, `close_date` columns) |
| **Why It Matters** | Measures the observed duration of sales engagement to deal resolution. |
| **Limitations & Rules** | (1) **This measures the observed engagement-to-close duration, NOT the complete lead-to-close sales cycle.** (2) Prospecting opportunities have NULL engage_date (500 deals) and are excluded — do not impute missing engage dates. (3) Do not imply that this is the total customer acquisition cycle. (4) Calendar days, not business days. Max observed = 138 days. |

---

### 5. Open Opportunity Count

| Attribute | Detail |
|-----------|--------|
| **Business Definition** | The number of deals currently in active pipeline stages (Prospecting + Engaging). |
| **SQL Formula** | `COUNT(*) WHERE deal_stage IN ('Prospecting', 'Engaging')` |
| **Denominator** | N/A (this is a count). |
| **Source Table** | `crm_sales.sales_pipeline` |
| **Why It Matters** | Indicates active pipeline volume. |
| **Limitations & Rules** | (1) **Monetary pipeline value is not directly available in the source dataset.** (2) Open opportunities have NULL `close_value`. (3) No probability or expected value field exists in the dataset. Product catalog prices must NOT be used as a proxy for open pipeline value. |

---

### 6. Open Pipeline Potential Value

| Attribute | Detail |
|-----------|--------|
| **Business Definition** | Estimated potential value of active open opportunities based on product catalog sales price. |
| **SQL Formula** | `SUM(p.sales_price) FROM crm_sales.sales_pipeline sp JOIN crm_sales.products p ON sp.product = p.product WHERE sp.deal_stage IN ('Prospecting', 'Engaging')` |
| **Denominator** | N/A (sum across open opportunities). |
| **Source Table** | `crm_sales.sales_pipeline` joined with `crm_sales.products` |
| **Why It Matters** | Represents total catalog potential value in flight. |
| **Limitations & Rules** | Product catalog prices represent baseline list price; actual closing deal value will be established upon closing. |

---

### 7. CRM Priority Score & Priority Tiers

| Attribute | Detail |
|-----------|--------|
| **Business Definition** | Deterministic, interpretable 0-100 composite index guiding management review and rep follow-up workflows for active open opportunities. |
| **Calculation Formula** | `Stage Pts (10-30) + Product Tier Pts (10-30) + Account Scale Pts (5-25) + Aging Band Pts (5-15)` |
| **Tiers** | Tier 1 — High Priority (>=75 pts, 428 deals), Tier 2 — Medium Priority (55-74 pts, 1,033 deals), Tier 3 — Lower Priority (<55 pts, 628 deals). |
| **Source Tables** | `crm_sales.sales_pipeline`, `accounts`, `products`, `sales_teams` |
| **Why It Matters** | Prevents deal neglect, prioritizes manager attention and rep follow-up without uninterpretable black-box bias. |
| **Governance Rule** | **"The CRM Priority Score is an operational prioritization index, not a predicted probability of winning."** Closed deal outcome information (close_date, close_value) is strictly quarantined and excluded. |

---

## KPI Quick Reference Table

| # | KPI | Domain | Formula / Method | Validated Value |
|---|-----|--------|------------------|-----------------|
| 1 | Win Rate | Sales CRM | Won / (Won + Lost) | 63.15% |
| 2 | Won Revenue | Sales CRM | SUM(close_value) for Won | $10,005,534.00 |
| 3 | Avg Deal Size | Sales CRM | Won Revenue / Won Deals | $2,360.91 |
| 4 | Avg Sales Cycle | Sales CRM | AVG(close_date - engage_date) | 47.99 days |
| 5 | Open Opportunities | Sales CRM | Prospecting (500) + Engaging (1,589) | 2,089 |
| 6 | Closed Opportunities | Sales CRM | Won (4,238) + Lost (2,473) | 6,711 |
| 7 | Total Opportunities | Sales CRM | Total Records in Pipeline | 8,800 |
| 8 | Open Pipeline Value | Sales CRM | SUM(product catalog sales_price) for Open | $4,966,215.00 |
| 9 | Active Sales Agents | Sales CRM | Agents with deals in pipeline | 30 agents (35 total team) |
| 10 | Strategic Accounts | Sales CRM | Total accounts in accounts catalog | 85 accounts |
| 11 | Products Catalog | Sales CRM | Total products in product catalog | 7 products |
| 12 | Tier 1 Priority Deals | Sales CRM | Open deals with Priority Score >= 75 | 428 deals (20.49%) |
| 13 | Tier 2 Priority Deals | Sales CRM | Open deals with Priority Score 55-74 | 1,033 deals (49.45%) |
| 14 | Tier 3 Priority Deals | Sales CRM | Open deals with Priority Score < 55 | 628 deals (30.06%) |
