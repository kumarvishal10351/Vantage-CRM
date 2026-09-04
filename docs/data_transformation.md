# Data Transformation & Cleaning Specifications

**Date:** 2026-08-30  
**Phase:** Phase 2 — Data Cleaning, Transformation & PostgreSQL Implementation  
**Status:** Completed & Validated

---

## 1. Overview & Principles

Data transformations adhere strictly to the following principles:
1. **Raw Data Immutability:** Raw source files in `data/raw/` are untouched and preserved in their original state.
2. **Deterministic Processing:** All transformations are executed via modular, reproducible Python scripts in `src/data_cleaning/`.
3. **Strict Domain Focus:** The platform models the B2B Sales CRM domain (`crm_sales`) exclusively, using genuine source data with zero fabricated entities.
4. **Preservation of Legitimate Nulls:** No synthetic values or arbitrary imputations are injected into open deal stages or missing operational fields.

---

## 2. Module 1: Sales CRM Transformations

**Target Directory:** `data/processed/crm_sales/`  
**Execution Script:** `src/data_cleaning/clean_sales.py`

### 2.1 `accounts.csv` (85 rows, 7 columns)

| Column | Raw State | Transformation Applied | Cleaned State | Rationale |
|---|---|---|---|---|
| `account` | `object` | Strip leading/trailing whitespace | `VARCHAR(100)` | Primary key standardization |
| `sector` | `object` (12 rows with `"technolgy"`) | String replacement: `"technolgy"` → `"technology"` | `VARCHAR(50)` | Correction of confirmed data entry typo |
| `year_established` | `int64` | Cast to integer | `INTEGER` | Standard numerical type |
| `revenue` | `float64` | Cast to float, retain precision | `NUMERIC(12, 2)` | Financial metrics (in millions USD) |
| `employees` | `int64` | Cast to integer | `INTEGER` | Count of employees |
| `office_location` | `object` (1 row with `"Philipines"`) | String replacement: `"Philipines"` → `"Philippines"` | `VARCHAR(100)` | Correction of geographical typo |
| `subsidiary_of` | `object` (70 NULLs, 15 parents) | Preserve NULLs for standalone accounts; validate parent names against `account` | `VARCHAR(100)` | Self-referencing FK hierarchy |

### 2.2 `products.csv` (7 rows, 3 columns)

| Column | Raw State | Transformation Applied | Cleaned State | Rationale |
|---|---|---|---|---|
| `product` | `object` | Strip whitespace | `VARCHAR(50)` | Primary key |
| `series` | `object` | Strip whitespace | `VARCHAR(20)` | Product line grouping (GTX, MG, GTK) |
| `sales_price` | `int64` | Cast to float/decimal | `NUMERIC(10, 2)` | Suggested retail price |

### 2.3 `sales_teams.csv` (35 rows, 3 columns)

| Column | Raw State | Transformation Applied | Cleaned State | Rationale |
|---|---|---|---|---|
| `sales_agent` | `object` | Strip whitespace | `VARCHAR(100)` | Primary key |
| `manager` | `object` | Strip whitespace | `VARCHAR(100)` | Sales manager name |
| `regional_office` | `object` | Strip whitespace | `VARCHAR(50)` | Regional grouping (Central, East, West) |

### 2.4 `sales_pipeline.csv` (8,800 rows, 8 columns)

| Column | Raw State | Transformation Applied | Cleaned State | Rationale |
|---|---|---|---|---|
| `opportunity_id` | `object` | Strip whitespace, validate uniqueness | `VARCHAR(50)` | Unique primary key |
| `sales_agent` | `object` | Strip whitespace, validate FK to `sales_teams` | `VARCHAR(100)` | Foreign key |
| `product` | `object` (1,480 rows with `"GTXPro"`) | Standardize `"GTXPro"` → `"GTX Pro"` | `VARCHAR(50)` | Resolves referential integrity mismatch with product catalog |
| `account` | `object` (1,425 NULLs) | Retain NULLs for Prospecting (337) and Engaging (1,088); strip whitespace on non-nulls | `VARCHAR(100)` | Unidentified accounts in early pipeline stages are legitimate business states |
| `deal_stage` | `object` | Strip whitespace | `VARCHAR(20)` | Validated domain: Prospecting, Engaging, Won, Lost |
| `engage_date` | `object` (500 NULLs) | Parse to standard ISO `YYYY-MM-DD` DATE format | `DATE` | Prospecting deals have no engagement date; others are verified valid dates |
| `close_date` | `object` (2,089 NULLs) | Parse to standard ISO `YYYY-MM-DD` DATE format | `DATE` | Open deals (Prospecting/Engaging) have no close date; closed deals have verified `close_date >= engage_date` |
| `close_value` | `float64` (2,089 NULLs, 2,473 zeros) | Retain NULLs for open deals; retain 0.0 for Lost deals; retain positive values for Won deals | `NUMERIC(12, 2)` | Distinct semantic difference between unresolved open deals (NULL) and lost deals ($0) |

---

## 3. Verification Summary

Every transformation was verified across:
- CSV input/output shape checks
- Automated assertion testing in Python
- SQL validation queries post-load
- Strict foreign key referential integrity in PostgreSQL (`crm_sales` schema)

