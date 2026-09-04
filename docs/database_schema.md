# Database Schema Documentation

**Database Name:** `crm_platform`  
**RDBMS:** PostgreSQL  
**Architecture:** B2B Sales CRM Architecture (`crm_sales` Schema)  
**Date:** 2026-09-04

---

## 1. Architectural Design

The platform uses the `crm_sales` schema within the `crm_platform` database, modeling the full sales operations domain:

```
crm_platform (Database)
└── crm_sales (Schema)
    ├── accounts
    ├── products
    ├── sales_teams
    ├── sales_pipeline
    └── app_users (Application Auth Infrastructure)
```

**Key Architectural Rules:**
1. **Source Data Decoupling:** Master CRM business entities (`accounts`, `products`, `sales_teams`, `sales_pipeline`) are driven exclusively by the genuine B2B CRM sales dataset.
2. **Infrastructure Separation:** Application authentication accounts (`crm_sales.app_users`) provide role-based access control (Admin, Sales Manager, Sales Agent) and are kept strictly decoupled from business records.
3. **Strict Referential Integrity:** Foreign keys enforce valid relationships between sales pipeline deals, sales agents, products, and target accounts.
4. **Domain & Check Constraints:** Database-level checks enforce logical date ordering, non-negative monetary figures, valid lifecycle stages, and stage-specific close value constraints.
5. **Targeted Performance Indexing:** Indexes are placed on foreign keys, analytical filtering dimensions (`deal_stage`, `sales_agent`, `product`, `account`), and date ranges (`engage_date`, `close_date`).

---

## 2. Master & Transactional Tables

### 2.1 Table: `crm_sales.accounts`

Master company directory for B2B target corporate accounts.

- **Grain:** One row per company account.
- **Row Count:** 85

| Column | Type | Constraints | Description |
|---|---|---|---|
| `account` | `VARCHAR(100)` | `PRIMARY KEY` | Company name |
| `sector` | `VARCHAR(50)` | `NOT NULL` | Industry classification (10 distinct sectors) |
| `year_established` | `INTEGER` | `NOT NULL`, `CHECK (year_established BETWEEN 1800 AND 2100)` | Year company founded |
| `revenue` | `NUMERIC(12, 2)` | `NOT NULL`, `CHECK (revenue >= 0)` | Annual corporate revenue (Millions USD) |
| `employees` | `INTEGER` | `NOT NULL`, `CHECK (employees >= 0)` | Total employee headcount |
| `office_location` | `VARCHAR(100)` | `NOT NULL` | Global headquarters country / territory |
| `subsidiary_of` | `VARCHAR(100)` | `NULLABLE`, `FK -> crm_sales.accounts(account)` | Parent company for corporate hierarchies |

**Indexes:**
- `idx_accounts_sector` on `sector`
- `idx_accounts_location` on `office_location`

---

### 2.2 Table: `crm_sales.products`

Master product catalog listing series and catalog prices.

- **Grain:** One row per product.
- **Row Count:** 7

| Column | Type | Constraints | Description |
|---|---|---|---|
| `product` | `VARCHAR(50)` | `PRIMARY KEY` | Product commercial name |
| `series` | `VARCHAR(20)` | `NOT NULL` | Product hardware/software line (`GTX`, `GTK`, `MG`) |
| `sales_price` | `NUMERIC(10, 2)` | `NOT NULL`, `CHECK (sales_price >= 0)` | Catalog list price in USD |

**Indexes:**
- `idx_products_series` on `series`

---

### 2.3 Table: `crm_sales.sales_teams`

Sales organizational hierarchy mapping agents to managers and regional offices.

- **Grain:** One row per sales representative.
- **Row Count:** 35

| Column | Type | Constraints | Description |
|---|---|---|---|
| `sales_agent` | `VARCHAR(100)` | `PRIMARY KEY` | Representative full name |
| `manager` | `VARCHAR(100)` | `NOT NULL` | Reporting sales manager (6 distinct managers) |
| `regional_office` | `VARCHAR(50)` | `NOT NULL` | Regional division (`Central`, `East`, `West`) |

**Indexes:**
- `idx_sales_teams_manager` on `manager`
- `idx_sales_teams_region` on `regional_office`

---

### 2.4 Table: `crm_sales.sales_pipeline`

Core transactional deal pipeline capturing lifecycle progression and financial outcomes.

- **Grain:** One row per sales opportunity.
- **Row Count:** 8,800

| Column | Type | Constraints | Description |
|---|---|---|---|
| `opportunity_id` | `VARCHAR(50)` | `PRIMARY KEY` | Unique opportunity identifier |
| `sales_agent` | `VARCHAR(100)` | `NOT NULL`, `FK -> crm_sales.sales_teams(sales_agent)` | Assigned sales representative |
| `product` | `VARCHAR(50)` | `NOT NULL`, `FK -> crm_sales.products(product)` | Target product being pitched |
| `account` | `VARCHAR(100)` | `NULLABLE`, `FK -> crm_sales.accounts(account)` | Prospect company (1,425 NULLs in early stage) |
| `deal_stage` | `VARCHAR(20)` | `NOT NULL`, `CHECK IN ('Prospecting', 'Engaging', 'Won', 'Lost')` | Pipeline lifecycle stage |
| `engage_date` | `DATE` | `NULLABLE` | Date sales engagement commenced (500 NULLs for Prospecting) |
| `close_date` | `DATE` | `NULLABLE` | Date deal was closed (2,089 NULLs for open deals) |
| `close_value` | `NUMERIC(12, 2)` | `NULLABLE` | Final transaction value (2,089 NULLs, 0 for Lost, >0 for Won) |

**Table-Level Business Constraints:**
- `chk_prospecting_no_engage`: Ensures Prospecting stage has `engage_date IS NULL`.
- `chk_open_no_close_date`: Ensures Prospecting and Engaging have `close_date IS NULL`.
- `chk_open_no_close_value`: Ensures Prospecting and Engaging have `close_value IS NULL`.
- `chk_lost_zero_value`: Enforces `close_value = 0.0` for all 2,473 Lost deals.
- `chk_won_positive_value`: Enforces `close_value > 0.0` for all 4,238 Won deals.
- `chk_date_order`: Enforces `close_date >= engage_date` across all closed deals.

**Indexes:**
- `idx_pipeline_stage` on `deal_stage`
- `idx_pipeline_agent` on `sales_agent`
- `idx_pipeline_product` on `product`
- `idx_pipeline_account` on `account`
- `idx_pipeline_engage_dt` on `engage_date`
- `idx_pipeline_close_dt` on `close_date`

---

## 3. Application Authentication & Authorization

### 3.1 Table: `crm_sales.app_users`

Infrastructure authentication table managing system logins and roles.

- **Grain:** One row per application user account.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `SERIAL` | `PRIMARY KEY` | Internal user ID |
| `email` | `VARCHAR(100)` | `UNIQUE`, `NOT NULL` | Login email address |
| `hashed_password` | `VARCHAR(255)` | `NOT NULL` | Bcrypt hashed password |
| `full_name` | `VARCHAR(100)` | `NOT NULL` | User display name |
| `role` | `VARCHAR(20)` | `NOT NULL`, `CHECK IN ('Admin', 'Sales Manager', 'Sales Agent')` | Authorization role |
| `is_active` | `BOOLEAN` | `NOT NULL DEFAULT TRUE` | Active account status |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | `DEFAULT CURRENT_TIMESTAMP` | Account creation timestamp |

**Indexes:**
- `idx_app_users_email` on `email`
- `idx_app_users_role` on `role`
