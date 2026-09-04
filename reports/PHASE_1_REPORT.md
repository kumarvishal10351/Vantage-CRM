# PHASE 1 REPORT — Data Audit, Data Contracts & Business Definitions

**Date:** 2026-08-30  
**Status:** PASSED (42/42 validation checks)

---

## 1. Executive Summary

Phase 1 performed a comprehensive, non-destructive audit of all datasets, established formal data dictionaries, documented business rules and KPI definitions, identified and documented all data quality issues with explicit decisions, completed a rigorous churn leakage audit, and defined analytical objectives for both modules.

**No raw data was modified.** All findings are documented in 8 formal documentation files.

---

## 2. Sales Audit Findings

### Dataset Summary

| Table | Rows | Columns | Primary Key | Status |
|-------|------|---------|-------------|--------|
| sales_pipeline | 8,800 | 8 | opportunity_id (unique) | Valid |
| accounts | 85 | 7 | account (unique) | Valid |
| products | 7 | 3 | product (unique) | Valid |
| sales_teams | 35 | 3 | sales_agent (unique) | Valid |

### Key Pipeline Metrics (Descriptive — Not Final KPIs)

| Metric | Value |
|--------|-------|
| Total opportunities | 8,800 |
| Closed deals | 6,711 (Won: 4,238 + Lost: 2,473) |
| Open deals | 2,089 (Prospecting: 500 + Engaging: 1,589) |
| Win rate (closed only) | 63.1% |
| Total Won revenue | Sum of close_value for Won deals |
| Average Won deal size | $2,360.91 |
| Average sales cycle (Won) | 51.8 days (median: 57) |
| Average sales cycle (Lost) | 41.5 days (median: 14) |
| Active agents | 30 of 35 |
| Date range | Oct 2016 – Dec 2017 |

### Referential Integrity

| Relationship | Status |
|-------------|--------|
| Pipeline agents -> Sales teams | VALID (all 30 exist) |
| Pipeline accounts -> Accounts | VALID (all 85 non-null exist) |
| Pipeline products -> Products | BROKEN ("GTXPro" vs "GTX Pro") — fixable |
| Subsidiary_of -> Accounts | VALID (all 15 parents exist) |

---

## 3. Customer Audit Findings

### Dataset Summary

| Attribute | Value |
|-----------|-------|
| Rows | 7,043 unique customers |
| Columns | 33 |
| Primary Key | CustomerID (unique) |
| Geography | California, United States only |
| Churn rate | 26.5% (1,869 churned / 5,174 retained) |
| Tenure range | 0–72 months |
| Monthly Charges | $18.25–$118.75 |

### Column Classification

| Category | Count | Columns |
|----------|-------|---------|
| Identifier | 1 | CustomerID |
| Demographic | 4 | Gender, Senior Citizen, Partner, Dependents |
| Service | 8 | Phone/Internet/Add-on services |
| Billing/Account | 6 | Tenure, Contract, Billing, Payment, Charges |
| Geographic | 4 | City, Zip Code, Latitude, Longitude |
| Target | 2 | Churn Label, Churn Value |
| Target-Derived | 3 | Churn Score, CLTV, Churn Reason |
| Redundant | 4 | Count, Country, State, Lat Long |

### Key Churn Patterns (Descriptive)

| Highest Churn Group | Churn Rate | Vs. Lowest Group | Churn Rate |
|---------------------|-----------|-------------------|------------|
| Month-to-month contract | 42.7% | Two year contract | 2.8% |
| Fiber optic internet | 41.9% | No internet | 7.4% |
| Electronic check payment | 45.3% | Credit card (auto) | 15.2% |
| 0-6 month tenure | 52.9% | 60-72 month tenure | 6.6% |
| Senior citizens | 41.7% | Non-seniors | 23.6% |
| No dependents | 32.6% | Has dependents | 6.5% |

---

## 4. Data Quality Issues — Complete Decision Log

### Sales Module

| # | Issue | Decision | Rationale |
|---|-------|----------|-----------|
| 1 | "technolgy" typo in sector | **Correct** | Obvious misspelling |
| 2 | "GTXPro" vs "GTX Pro" | **Correct** | Standardize to catalog name |
| 3 | "Philipines" in office_location | **Correct** | Misspelling of "Philippines" |
| 4 | 1,425 null accounts | **Retain** | Expected for early-stage deals |
| 5 | 5 inactive agents | **Retain** | Legitimate team members |
| 6 | 500 null engage_date | **Retain** | Correct for Prospecting stage |
| 7 | 2,089 null close_date/value | **Retain** | Correct for open deals |

### Customer Module

| # | Issue | Decision | Rationale |
|---|-------|----------|-----------|
| 1 | Count column (always 1) | **Drop** | Zero variance |
| 2 | Country column (always US) | **Drop** | Zero variance |
| 3 | State column (always CA) | **Drop** | Zero variance |
| 4 | Lat Long column | **Drop** | Redundant with Latitude/Longitude |
| 5 | Total Charges (11 blanks) | **Set to 0.0** | Zero-tenure customers; no billing has occurred |

---

## 5. Leakage Findings

| Column | Verdict | Correlation with Target | Evidence |
|--------|---------|------------------------|----------|
| **Churn Score** | DEFINITE LEAKAGE | r = 0.665 | IBM pre-computed propensity; mean 82.5 (churned) vs 50.1 (retained) |
| **Churn Reason** | DEFINITE LEAKAGE | Perfect | Non-null for 100% of churned, 0% of retained |
| **CLTV** | PRECAUTIONARY EXCLUDE | r = -0.128 | Weak correlation but unknown derivation; CLTV methods commonly use churn probability |
| **Churn Label** | TARGET DUPLICATE | 1:1 | String version of Churn Value |

**Safe ML features:** 18 columns (4 demographic + 8 service + 6 billing/account)  
**Geographic features:** 4 columns (safe but usefulness TBD during feature engineering)

---

## 6. Business Definitions

### Sales KPI Definitions

| KPI | Definition | Denominator |
|-----|-----------|-------------|
| Win Rate | Won / (Won + Lost) | Closed deals only |
| Sales Cycle | close_date - engage_date | Closed deals with both dates |
| Revenue | Sum of close_value | Won deals only |
| Average Deal Size | Mean of close_value | Won deals only |
| Pipeline (Open) | Count of open deals | Prospecting + Engaging |

### Customer KPI Definitions

| KPI | Definition | Notes |
|-----|-----------|-------|
| Churn Rate | Churned / Total customers | Dataset snapshot rate — not monthly/annual |
| Retention Rate | 1 - Churn Rate | Complement of churn rate |

### Segmentation Approach

Do NOT use RFM — the data does not support true Recency, Frequency, Monetary analysis. Use **Customer Behavioral Segmentation** based on demographics, service adoption, and billing characteristics.

---

## 7. Analytical Objectives

Defined 26+ business questions across both modules. See [analytical_objectives.md](file:///c:/Users/kumar/Desktop/CRM/docs/analytical_objectives.md) for the complete list.

**Sales Module:** Pipeline composition, win rates, revenue analysis, agent performance, product performance, sales cycle analysis, opportunity scoring

**Customer Module:** Churn analysis, service analysis, customer segmentation, churn prediction, retention intelligence

---

## 8. Data Contract Summary

### Sales Module — Future PostgreSQL Tables

| Table | Schema | Grain | PK | FKs |
|-------|--------|-------|----|----|
| accounts | crm_sales | One row per company | account | subsidiary_of -> accounts.account |
| products | crm_sales | One row per product | product | — |
| sales_teams | crm_sales | One row per agent | sales_agent | — |
| sales_pipeline | crm_sales | One row per opportunity | opportunity_id | sales_agent -> sales_teams, product -> products, account -> accounts |

### Customer Module — Future PostgreSQL Table

| Table | Schema | Grain | PK | FKs |
|-------|--------|-------|----|----|
| customers | customer_intelligence | One row per customer | customer_id | — |

**No cross-schema foreign keys.** The two modules are intentionally independent.

---

## 9. Files Created

| File | Size | Purpose |
|------|------|---------|
| [docs/sales_data_dictionary.md](file:///c:/Users/kumar/Desktop/CRM/docs/sales_data_dictionary.md) | 5,413 B | Complete sales module data dictionary |
| [docs/customer_data_dictionary.md](file:///c:/Users/kumar/Desktop/CRM/docs/customer_data_dictionary.md) | 6,809 B | Complete customer module data dictionary |
| [docs/sales_business_rules.md](file:///c:/Users/kumar/Desktop/CRM/docs/sales_business_rules.md) | 7,093 B | Sales pipeline business logic and KPI definitions |
| [docs/customer_business_rules.md](file:///c:/Users/kumar/Desktop/CRM/docs/customer_business_rules.md) | 5,676 B | Customer churn business rules |
| [docs/sales_data_quality.md](file:///c:/Users/kumar/Desktop/CRM/docs/sales_data_quality.md) | 6,192 B | Sales data quality decisions (7 issues) |
| [docs/customer_data_quality.md](file:///c:/Users/kumar/Desktop/CRM/docs/customer_data_quality.md) | 6,559 B | Customer data quality decisions (5 issues) |
| [docs/churn_leakage_audit.md](file:///c:/Users/kumar/Desktop/CRM/docs/churn_leakage_audit.md) | 9,602 B | Rigorous leakage audit for 5 columns |
| [docs/analytical_objectives.md](file:///c:/Users/kumar/Desktop/CRM/docs/analytical_objectives.md) | 5,409 B | 26+ business questions for both modules |
| [reports/PHASE_1_REPORT.md](file:///c:/Users/kumar/Desktop/CRM/reports/PHASE_1_REPORT.md) | — | This report |

---

## 10. Validation Results

```
=== PHASE 1 VALIDATION CHECKS ===

1. Row Counts:          5/5 PASSED
2. Column Counts:       5/5 PASSED
3. Primary Keys:        5/5 PASSED
4. Foreign Key Integrity: 4/4 PASSED
5. Data Quality Issues:  5/5 PASSED
6. Churn Target:        4/4 PASSED
7. Leakage Audit:       3/3 PASSED
8. Total Charges Blanks: 3/3 PASSED
9. Output Files:        8/8 PASSED

TOTAL: 42 PASSED, 0 FAILED out of 42 checks
PHASE 1 VALIDATION: ALL CHECKS PASSED
```

---

## 11. Discrepancies vs Phase 0

| Item | Phase 0 | Phase 1 | Resolution |
|------|---------|---------|------------|
| "Philipines" typo | Not identified | Identified in accounts.csv | Added to data quality decisions |
| Product mismatch detail | Noted as broken FK | Confirmed exactly 1 product affected ("GTXPro", 1,480 rows) | Consistent, more precise in Phase 1 |
| All other findings | Consistent | Confirmed with deeper evidence | No contradictions |

---

## 12. Unresolved Questions

None. All ambiguities have been resolved with documented decisions.

---

## Ready for Phase 2

Phase 1 audit is complete. All data quality issues are documented with explicit decisions. All business definitions are established. All leakage risks are identified and resolved.

**Awaiting instruction to proceed to Phase 2 — Data Cleaning & PostgreSQL Architecture.**
