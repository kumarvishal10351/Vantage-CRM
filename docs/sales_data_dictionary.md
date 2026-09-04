# Sales Module — Data Dictionary

**Module:** Sales CRM Analytics  
**Source Files:** `sales_pipeline.csv`, `accounts.csv`, `products.csv`, `sales_teams.csv`  
**Business Context:** B2B sales pipeline for a fictional technology products company  
**Date Range:** October 2016 — December 2017

---

## Table: sales_pipeline

**Purpose:** Records every sales opportunity from prospecting through to outcome (Won/Lost).  
**Grain:** One row per opportunity.  
**Row Count:** 8,800  
**Primary Key:** `opportunity_id`

| Column | Data Type | Nullable | Unique | Description |
|--------|-----------|----------|--------|-------------|
| opportunity_id | text | No | 8,800 (all unique) | Unique alphanumeric identifier for each sales opportunity. Confirmed unique — valid primary key. |
| sales_agent | text | No | 30 | Name of the sales agent who owns the opportunity. All 30 agents exist in `sales_teams`. |
| product | text | No | 7 | Product being sold. **Issue:** Uses `"GTXPro"` while `products.csv` uses `"GTX Pro"` (missing space). |
| account | text | **Yes** | 85 + NaN | Company name associated with the opportunity. **1,425 nulls** — all in Prospecting (337) or Engaging (1,088) stages. Zero nulls in Won/Lost. |
| deal_stage | text | No | 4 | Current pipeline stage: `Prospecting`, `Engaging`, `Won`, `Lost`. |
| engage_date | text (date) | **Yes** | — | Date the deal moved to the Engaging stage. **500 nulls** — all in the Prospecting stage (which has not yet engaged). Format: YYYY-MM-DD. Range: 2016-10-20 to 2017-12-27. |
| close_date | text (date) | **Yes** | — | Date the deal was Won or Lost. **2,089 nulls** — all in Prospecting (500) and Engaging (1,589) stages (open deals). Format: YYYY-MM-DD. Range: 2017-03-01 to 2017-12-31. |
| close_value | float64 | **Yes** | — | Revenue from the deal in USD. **2,089 nulls** — same pattern as close_date (open deals). Won deals: $38–$30,288. Lost deals: always 0.0. |

---

## Table: accounts

**Purpose:** Master list of B2B customer accounts (companies).  
**Grain:** One row per company.  
**Row Count:** 85  
**Primary Key:** `account`

| Column | Data Type | Nullable | Unique | Description |
|--------|-----------|----------|--------|-------------|
| account | text | No | 85 (all unique) | Company name. Valid primary key. Referenced by `sales_pipeline.account`. |
| sector | text | No | 10 | Industry sector. **Issue:** Contains `"technolgy"` (typo for `"technology"`). Sectors: retail (17), technology (12), medical (12), marketing (8), finance (8), software (7), entertainment (6), telecommunications (6), services (5), employment (4). |
| year_established | int64 | No | — | Year the company was founded. Range: 1979–2017. |
| revenue | float64 | No | — | Annual revenue in millions of USD. Range: $4.54M–$11,698.03M. |
| employees | int64 | No | — | Number of employees. Range: 9–34,288. |
| office_location | text | No | 15 | Country of headquarters. 71 accounts in United States. 14 international. |
| subsidiary_of | text | **Yes** | — | Parent company name (if subsidiary). 15 subsidiaries, 70 standalone. All parent names exist in the `account` column — referential integrity is intact. |

---

## Table: products

**Purpose:** Product catalog with list prices.  
**Grain:** One row per product.  
**Row Count:** 7  
**Primary Key:** `product`

| Column | Data Type | Nullable | Unique | Description |
|--------|-----------|----------|--------|-------------|
| product | text | No | 7 (all unique) | Product name. Valid primary key. **Note:** Uses `"GTX Pro"` (with space) while pipeline uses `"GTXPro"` (no space). |
| series | text | No | 3 | Product series/line: GTX (4 products), MG (2 products), GTK (1 product). |
| sales_price | int64 | No | 7 | Suggested retail price in USD. Range: $55 (MG Special) to $26,768 (GTK 500). 487x price spread. |

---

## Table: sales_teams

**Purpose:** Sales organization structure — agents, managers, regions.  
**Grain:** One row per sales agent.  
**Row Count:** 35  
**Primary Key:** `sales_agent`

| Column | Data Type | Nullable | Unique | Description |
|--------|-----------|----------|--------|-------------|
| sales_agent | text | No | 35 (all unique) | Sales agent name. Valid primary key. 30 of 35 agents have pipeline activity. **5 agents have zero pipeline deals.** |
| manager | text | No | 6 | Manager name. 6 managers, each managing 5–6 agents. Each manager belongs to exactly one region. |
| regional_office | text | No | 3 | Regional office: Central (11 agents), East (12 agents), West (12 agents). |

---

## Referential Integrity Summary

| Relationship | Type | Status |
|-------------|------|--------|
| `sales_pipeline.sales_agent` → `sales_teams.sales_agent` | Many-to-one | **Valid** — all 30 pipeline agents exist in sales_teams |
| `sales_pipeline.account` → `accounts.account` | Many-to-one | **Valid** — all 85 non-null accounts exist in accounts |
| `sales_pipeline.product` → `products.product` | Many-to-one | **Broken** — `"GTXPro"` does not match `"GTX Pro"` |
| `accounts.subsidiary_of` → `accounts.account` | Self-reference | **Valid** — all 15 parent names exist in account column |

---

## Data Dictionary Source File

The original `data_dictionary.csv` (21 entries) covers all four tables with correct field names and descriptions. Dictionary coverage is complete and consistent with actual columns.
