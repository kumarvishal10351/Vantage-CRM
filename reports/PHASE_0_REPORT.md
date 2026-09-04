# PHASE 0 REPORT — Environment & Project Inspection

**Date:** 2026-08-30  
**Status:** ✅ PASSED

---

## 1. Workspace Summary

**Location:** `c:\Users\kumar\Desktop\CRM`

The workspace is a flat directory containing 6 raw data files and no existing code, subdirectories, or configuration files.

| File | Size | Description |
|------|------|-------------|
| `Telco_customer_churn.xlsx` | 1.34 MB | IBM Telco Customer Churn dataset |
| `sales_pipeline.csv` | 623 KB | CRM sales pipeline opportunities |
| `accounts.csv` | 4.6 KB | B2B account/company data |
| `sales_teams.csv` | 1.3 KB | Sales agents and managers |
| `products.csv` | 171 B | Product catalog (7 products) |
| `data_dictionary.csv` | 996 B | Field descriptions for CRM tables |

**Git Status:** Repository exists (parent-level Desktop repo). The CRM directory is currently untracked. A project-level `.gitignore` will be needed.

---

## 2. Dataset Summary

### MODULE 1 — CRM Sales Pipeline Dataset

Four related CSV files forming a normalized B2B sales dataset.

#### sales_pipeline.csv (8,800 rows × 8 columns)

| Column | Dtype | Missing | Notes |
|--------|-------|---------|-------|
| opportunity_id | object | 0 | Unique identifier (8,800 unique) |
| sales_agent | object | 0 | 30 unique agents |
| product | object | 0 | 7 unique products |
| account | object | **1,425** | Missing for some Prospecting/Engaging deals |
| deal_stage | object | 0 | Prospecting (500), Engaging (1,589), Won (4,238), Lost (2,473) |
| engage_date | object | **500** | Missing for Prospecting stage only |
| close_date | object | **2,089** | Missing for Prospecting + Engaging (open deals) |
| close_value | float64 | **2,089** | Missing for open deals; **Lost deals = 0.0** |

**Key Observations:**
- Date range: Oct 2016 → Dec 2017
- Won deals: mean close_value = $2,361, range $38–$30,288
- Lost deals: close_value = 0 for all (confirmed — revenue is 0 for lost deals)
- 1,425 missing accounts occur in Prospecting (337) and Engaging (1,088) stages — these are deals without a confirmed account

#### accounts.csv (85 rows × 7 columns)

| Column | Dtype | Missing | Notes |
|--------|-------|---------|-------|
| account | object | 0 | Company name (unique) |
| sector | object | 0 | 10 sectors — **TYPO: "technolgy" (12 rows)** |
| year_established | int64 | 0 | Range: 1979–2017 |
| revenue | float64 | 0 | $4.54M–$11,698.03M |
| employees | int64 | 0 | 9–34,288 |
| office_location | object | 0 | 15 countries (71 in US) |
| subsidiary_of | object | **70** | 15 are subsidiaries, 70 are standalone |

#### products.csv (7 rows × 3 columns)

| Product | Series | Sales Price |
|---------|--------|-------------|
| GTX Basic | GTX | $550 |
| GTX Pro | GTX | $4,821 |
| GTX Plus Basic | GTX | $1,096 |
| GTX Plus Pro | GTX | $5,482 |
| GTK 500 | GTK | $26,768 |
| MG Special | MG | $55 |
| MG Advanced | MG | $3,393 |

#### sales_teams.csv (35 rows × 3 columns)

- 35 sales agents, 6 managers, 3 regional offices (Central: 11, East: 12, West: 12)
- All 30 pipeline agents are present in sales_teams
- **5 agents in sales_teams have NO deals in pipeline** (Elizabeth Anderson, Carol Thompson, Carl Lin, Mei-Mei Johns, Natalya Ivanova)

#### Referential Integrity Issues Found

| Check | Result |
|-------|--------|
| Pipeline agents ↔ Sales teams | ✅ All 30 pipeline agents exist in sales_teams |
| Pipeline accounts ↔ Accounts | ✅ All 85 non-null pipeline accounts exist in accounts.csv |
| Pipeline products ↔ Products | ⚠️ **"GTXPro" in pipeline vs "GTX Pro" in products.csv** — naming mismatch (missing space) |
| Sales teams agents → Pipeline | ⚠️ 5 agents have zero pipeline activity |

---

### MODULE 2 — IBM Telco Customer Churn Dataset

#### Telco_customer_churn.xlsx (7,043 rows × 33 columns)

| Column | Dtype | Unique | Missing | Notes |
|--------|-------|--------|---------|-------|
| CustomerID | object | 7,043 | 0 | Unique identifier |
| Count | int64 | 1 | 0 | Always 1 — **redundant, drop** |
| Country | object | 1 | 0 | Always "United States" — **redundant, drop** |
| State | object | 1 | 0 | Always "California" — **redundant, drop** |
| City | object | 1,129 | 0 | California cities |
| Zip Code | int64 | 1,652 | 0 | CA zip codes |
| Lat Long | object | 1,652 | 0 | Combined string — **redundant (Lat + Long exist), drop** |
| Latitude | float64 | 1,652 | 0 | 32.56–41.96 |
| Longitude | float64 | 1,651 | 0 | -124.30 to -114.19 |
| Gender | object | 2 | 0 | Male/Female |
| Senior Citizen | object | 2 | 0 | Yes/No |
| Partner | object | 2 | 0 | Yes/No |
| Dependents | object | 2 | 0 | Yes/No |
| Tenure Months | int64 | 73 | 0 | 0–72 months |
| Phone Service | object | 2 | 0 | Yes/No |
| Multiple Lines | object | 3 | 0 | Yes/No/No phone service |
| Internet Service | object | 3 | 0 | DSL/Fiber optic/No |
| Online Security | object | 3 | 0 | Yes/No/No internet service |
| Online Backup | object | 3 | 0 | Yes/No/No internet service |
| Device Protection | object | 3 | 0 | Yes/No/No internet service |
| Tech Support | object | 3 | 0 | Yes/No/No internet service |
| Streaming TV | object | 3 | 0 | Yes/No/No internet service |
| Streaming Movies | object | 3 | 0 | Yes/No/No internet service |
| Contract | object | 3 | 0 | Month-to-month/One year/Two year |
| Paperless Billing | object | 2 | 0 | Yes/No |
| Payment Method | object | 4 | 0 | 4 payment types |
| Monthly Charges | float64 | 1,585 | 0 | $18.25–$118.75 |
| Total Charges | **object** | 6,531 | 0 | ⚠️ **11 rows are empty strings** (dtype is object, not numeric) |
| Churn Label | object | 2 | 0 | Yes/No |
| Churn Value | int64 | 2 | 0 | 0/1 — **TARGET VARIABLE** |
| Churn Score | int64 | 85 | 0 | ⛔ **LEAKAGE — see audit below** |
| CLTV | int64 | 3,438 | 0 | ⚠️ **Requires leakage audit** |
| Churn Reason | object | 20 | **5,174** | ⛔ **LEAKAGE — only populated for churned customers** |

#### Churn Distribution

| Churn Label | Count | Percentage |
|-------------|-------|------------|
| No | 5,174 | 73.5% |
| Yes | 1,869 | 26.5% |

**Class imbalance:** Moderate (26.5% positive class). Manageable with `class_weight='balanced'` or stratified sampling. SMOTE not strictly necessary.

#### Total Charges Issue

- 11 rows have empty string `Total Charges` (not NaN — stored as whitespace)
- All 11 have `Tenure Months = 0` (brand new customers)
- All 11 are `Churn Label = No` (non-churners)
- **Decision needed:** Coerce to 0.0 (logical — zero tenure means zero total charges)

#### Target Leakage Audit

| Column | Leakage Risk | Evidence | Decision |
|--------|-------------|----------|----------|
| **Churn Score** | ⛔ **DEFINITE LEAKAGE** | Mean for churned = 82.5, retained = 50.1. This is IBM's pre-computed propensity score derived from the target. | **EXCLUDE from ML features** |
| **Churn Reason** | ⛔ **DEFINITE LEAKAGE** | Only populated for churned customers (1,869/1,869). NaN for all retained. Perfectly reveals the target. | **EXCLUDE from ML features** (useful for post-hoc analysis only) |
| **CLTV** | ⚠️ **MODERATE RISK** | Mean for churned = 4,149 vs retained = 4,491. This is IBM's pre-computed Customer Lifetime Value. It may incorporate churn probability in its calculation. | **EXCLUDE from ML features** (use for business analysis only) |
| **Churn Label** | ⛔ **TARGET ITSELF** | String version of Churn Value | **EXCLUDE** — use Churn Value (0/1) as target |

**Safe features for churn prediction** (16 features):
- Demographics: Gender, Senior Citizen, Partner, Dependents
- Service subscriptions: Phone Service, Multiple Lines, Internet Service, Online Security, Online Backup, Device Protection, Tech Support, Streaming TV, Streaming Movies
- Account: Contract, Paperless Billing, Payment Method, Tenure Months, Monthly Charges, Total Charges (after cleaning)

---

## 3. Environment Summary

### Python

| Component | Version |
|-----------|---------|
| Python | 3.14.3 |
| pandas | 2.3.3 |
| numpy | 2.4.4 |
| scikit-learn | 1.8.0 |
| xgboost | 3.2.0 |
| matplotlib | 3.10.8 |
| seaborn | 0.13.2 |
| scipy | 1.17.1 |
| shap | 0.52.0 |
| psycopg2 | 2.9.12 |
| SQLAlchemy | 2.0.48 |
| openpyxl | 3.1.5 |
| joblib | 1.5.3 |

**Missing (optional):** imbalanced-learn — not critical; `class_weight='balanced'` in sklearn models is sufficient.

### Git
- Version: 2.51.2.windows.1
- Repository exists at Desktop level (parent). CRM directory is untracked.

---

## 4. PostgreSQL Status

| Item | Value |
|------|-------|
| Version | PostgreSQL 18.1 (x86_64-windows, msvc-19.44) |
| Installation | `C:\Program Files\PostgreSQL\18\` |
| Service | `postgresql-x64-18` — **Running** |
| Port | 5432 (default) |
| Authentication | scram-sha-256 |
| Connection Test | ✅ **PASSED** (`postgres` user) |
| Existing Databases | `postgres`, `customer_behavior`, `job_market_db` |
| psql Location | `C:\Program Files\PostgreSQL\18\bin\psql.exe` (not in PATH) |

**PostgreSQL is fully operational and will be used as the project database.**

---

## 5. Power BI Status

| Item | Value |
|------|-------|
| Installation | Microsoft Store (Microsoft.MicrosoftPowerBIDesktop) |
| Version | 2.155.756.0 |
| Report Builder | Also installed (15.7.1819.0) |

**Power BI Desktop is available for report creation.**

---

## 6. Recommended Project Structure

```
CRM/
├── .gitignore                          # Python/data/credentials exclusions
├── .env                                # DB credentials (gitignored)
├── requirements.txt                    # Pinned dependencies
├── README.md                           # Project documentation
├── config/
│   └── settings.py                     # Paths, seeds, constants
├── data/
│   ├── raw/                            # Original datasets (copied, never modified)
│   │   ├── Telco_customer_churn.xlsx
│   │   ├── sales_pipeline.csv
│   │   ├── accounts.csv
│   │   ├── products.csv
│   │   ├── sales_teams.csv
│   │   └── data_dictionary.csv
│   └── processed/                      # Cleaned datasets
│       ├── crm_sales/                  # Module 1 cleaned data
│       └── customer_intelligence/      # Module 2 cleaned data
├── sql/
│   ├── ddl/                            # Table definitions
│   │   ├── crm_sales_schema.sql
│   │   └── customer_intelligence_schema.sql
│   ├── dml/                            # Data loading
│   └── analytics/                      # Analytical queries
│       ├── crm_sales_queries.sql
│       └── customer_intelligence_queries.sql
├── src/
│   ├── data_cleaning/                  # Phase 2
│   ├── analytics/                      # Phase 3, 7, 8
│   ├── models/                         # Phase 4, 5, 6
│   └── utils/                          # Shared utilities
├── reports/                            # Phase reports
│   └── PHASE_0_REPORT.md
├── powerbi/                            # Phase 8
│   ├── exports/                        # Analysis-ready CSVs for Power BI
│   └── documentation/                  # DAX, data model docs
└── tests/                              # Validation scripts
```

### Database Architecture

Two PostgreSQL schemas under a single database (`crm_platform`):

```
crm_platform (database)
├── crm_sales (schema)               ── MODULE 1
│   ├── accounts
│   ├── products
│   ├── sales_teams
│   └── sales_pipeline
└── customer_intelligence (schema)   ── MODULE 2
    └── customers
```

**No cross-schema foreign keys.** The modules are intentionally independent.

---

## 7. Data Quality Issues Requiring Resolution (Phase 2)

| # | Issue | Severity | Dataset | Proposed Resolution |
|---|-------|----------|---------|---------------------|
| 1 | `Total Charges` is dtype object with 11 empty strings | Medium | Telco | Coerce to numeric, set 0 for 0-tenure customers |
| 2 | `"technolgy"` typo in accounts.csv sector | Low | CRM | Correct to `"technology"` |
| 3 | `"GTXPro"` in pipeline vs `"GTX Pro"` in products | Medium | CRM | Standardize to `"GTX Pro"` (match products.csv) |
| 4 | 5 agents in sales_teams with zero pipeline deals | Low | CRM | Document as-is (they may be new/inactive agents) |
| 5 | 1,425 opportunities with no account | Expected | CRM | Expected for early-stage deals — document pattern |
| 6 | Redundant Telco columns (Count, Country, State, Lat Long) | Low | Telco | Drop during cleaning |
| 7 | `Churn Score`, `CLTV`, `Churn Reason` leakage risk | **Critical** | Telco | Exclude from ML features; use for analysis only |

---

## 8. Blockers

**None.** All required infrastructure is operational:
- ✅ Python 3.14 with all critical packages
- ✅ PostgreSQL 18.1 running and connectable
- ✅ Power BI Desktop installed
- ✅ Git available
- ✅ Both datasets present and readable

---

## 9. Assumptions & Decisions Log

| Decision | Rationale |
|----------|-----------|
| Two independent modules, no artificial join | Datasets have no legitimate relationship |
| PostgreSQL as primary database | Installed, running, connectable |
| `Churn Value` (0/1) as ML target | Binary, clean, directly usable |
| Exclude Churn Score, CLTV, Churn Reason from features | Confirmed leakage through statistical audit |
| `class_weight='balanced'` over SMOTE | 26.5% minority is moderate; no need for synthetic oversampling |
| Use `crm_sales` and `customer_intelligence` schemas | Enforces logical separation at DB level |

---

## 10. Validation Summary

| Check | Result |
|-------|--------|
| Workspace inspected | ✅ |
| All 6 data files readable | ✅ |
| Telco dataset profiled (7,043 × 33) | ✅ |
| CRM dataset profiled (4 tables) | ✅ |
| Referential integrity checked | ✅ (2 issues found, documented) |
| Target leakage audit completed | ✅ (3 columns flagged) |
| Python environment verified | ✅ (all critical packages present) |
| PostgreSQL connectivity confirmed | ✅ (v18.1, running, authenticated) |
| Power BI availability confirmed | ✅ (v2.155, Store install) |
| Git availability confirmed | ✅ (v2.51.2) |
| No files modified | ✅ |
| No data generated | ✅ |

---

## 11. Files Created

| File | Purpose |
|------|---------|
| `reports/PHASE_0_REPORT.md` | This report |

## 12. Commands Used

| Command | Purpose |
|---------|---------|
| `pd.read_excel('Telco_customer_churn.xlsx')` | Load and profile Telco dataset |
| `pd.read_csv(...)` | Load and profile all CRM CSVs |
| `pg_isready.exe` | Check PostgreSQL service status |
| `psycopg2.connect(...)` | Verify PostgreSQL authentication |
| `pip list` | Inventory installed Python packages |
| `Get-Service postgresql*` | Verify Windows service |
| `Get-AppxPackage *powerbi*` | Check Power BI installation |

---

## Ready for Phase 1

Phase 0 inspection is complete. All infrastructure is confirmed operational. Waiting for instruction to proceed to **Phase 1 — Dataset Audit**.
