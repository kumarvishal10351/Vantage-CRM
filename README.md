# Vantage-CRM

## Enterprise Sales CRM & Pipeline Management Platform

A production-style, portfolio-grade B2B Sales Operations Platform featuring an audited **FastAPI backend** and a modern **React SPA frontend (Vantage CRM)** faithfully translated from Google Stitch designs.

This project manages and analyzes B2B corporate accounts, sales opportunities, pipeline conversion, product catalog performance, sales organizational hierarchy (representatives and managers), opportunity aging, deterministic deal prioritization, and operational work queues.

---

## Table of Contents

1. [Project Purpose](#1-project-purpose)
2. [CRM Capabilities](#2-crm-capabilities)
3. [System Architecture](#3-system-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Database Architecture](#5-database-architecture)
6. [API Catalog](#6-api-catalog)
7. [CRM Business Logic](#7-crm-business-logic)
8. [Opportunity Prioritization Framework](#8-opportunity-prioritization-framework)
9. [Testing & Quality Assurance](#9-testing--quality-assurance)
10. [Setup Instructions](#10-setup-instructions)
11. [Environment Variables](#11-environment-variables)
12. [API Usage Examples](#12-api-usage-examples)
13. [Data Integrity Decisions](#13-data-integrity-decisions)
14. [Known Limitations](#14-known-limitations)

---

## 1. Project Purpose

The primary objective of this platform is to provide a portfolio-grade Sales Operations and CRM backend platform for a high-velocity B2B sales organization. Rather than relying on generic machine learning predictions or synthetic customer linkages, the platform applies rigorous data engineering, deterministic sales prioritization, and high-performance REST APIs directly to genuine B2B sales data. (Note: This is a portfolio-grade backend platform, not a live commercial production deployment).

The system empowers:
- **Sales Representatives:** To sequence daily outreach using transparent priority scoring and actionable work queues.
- **Sales Managers:** To monitor team pipelines, identify stalled deals, evaluate win rates, and compare regional performance.
- **Executive Leadership:** To access real-time pipeline velocity, won revenue, deal size distributions, and product revenue concentration.

---

## 2. CRM Capabilities

- **Account Management:** Corporate accounts with industry sector, company revenue, employee count, global headquarters, parent-subsidiary hierarchies, and historical opportunity statistics.
- **Opportunity Lifecycle Tracking:** Full funnel tracking across validated stages: `Prospecting`, `Engaging`, `Won`, and `Lost`.
- **Sales Pipeline Analytics:** Comprehensive aggregation of open vs. closed deals, win rates, sales cycles, and multi-dimensional slicing by product, sector, sales agent, sales manager, and regional office.
- **Sales Organization Hierarchy:** Full sales team modeling across 30 active representatives, 6 managers, and 3 regional offices (Central, East, West).
- **Product Portfolio Performance:** Catalog metrics for 7 products across 3 series (`GTX`, `GTK`, `MG`) with list pricing and catalog value tiers.
- **Opportunity Aging & Velocity:** Categorization of in-flight deals into operational aging bands (`Recent`, `Aging`, `Stalled/Critical`, `Unengaged`) and calculation of historical sales cycle durations.
- **Deterministic Prioritization:** Transparent 100-point prioritization matrix segmenting open opportunities into Tier 1 (High Priority), Tier 2 (Medium Priority), and Tier 3 (Lower Priority) without post-outcome leakage.
- **CRM Work Queues:** Targeted operational queues for executive review (Tier 1 deals), intervention (stalled deals > 180 days), and data hygiene (unassigned accounts).

---

## 3. System Architecture

The backend follows clean layered architecture principles, decoupling routing, validation, domain services, database persistence, and security:

```
CRM/
├── backend/
│   └── app/
│       ├── api/               # API routes & dependency injection
│       │   ├── deps.py        # Database session and JWT auth dependencies
│       │   └── v1/            # Versioned API routes
│       │       ├── accounts.py
│       │       ├── agents.py
│       │       ├── aging.py
│       │       ├── auth.py
│       │       ├── managers.py
│       │       ├── opportunities.py
│       │       ├── pipeline.py
│       │       ├── prioritization.py
│       │       ├── products.py
│       │       ├── router.py
│       │       └── work_queues.py
│       ├── core/              # Configuration, database engine, error handling, security
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── exceptions.py
│       │   └── security.py
│       ├── models/            # SQLAlchemy 2.0 ORM models
│       │   └── crm.py
│       ├── schemas/           # Pydantic request/response schemas
│       │   ├── account.py
│       │   ├── agent.py
│       │   ├── aging.py
│       │   ├── auth.py
│       │   ├── common.py
│       │   ├── manager.py
│       │   ├── opportunity.py
│       │   ├── pipeline.py
│       │   ├── prioritization.py
│       │   ├── product.py
│       │   └── work_queue.py
│       ├── services/          # Pure business services
│       │   ├── account_service.py
│       │   ├── agent_service.py
│       │   ├── aging_service.py
│       │   ├── auth_service.py
│       │   ├── manager_service.py
│       │   ├── opportunity_service.py
│       │   ├── pipeline_service.py
│       │   ├── prioritization_service.py
│       │   ├── product_service.py
│       │   └── work_queue_service.py
│       └── main.py            # Application entrypoint & middleware configuration
├── config/                    # Global path and database configurations
│   └── settings.py
├── data/
│   ├── raw/                   # Immutable raw source CSVs
│   └── processed/             # Cleaned, standardized CRM CSV datasets
│       └── crm_sales/
├── docs/                      # Architectural documents, data dictionary & audit report
│   ├── FINAL_BACKEND_AUDIT.md
│   ├── crm_kpi_definitions.md
│   ├── crm_priority_framework.md
│   ├── database_schema.md
│   └── sales_business_rules.md
├── sql/
│   ├── ddl/                   # Database schemas (crm_sales, crm_auth)
│   └── analytics/             # 10 production SQL KPI queries
├── src/                       # ETL cleaning, PostgreSQL loading, and priority scoring scripts
│   ├── data_cleaning/clean_sales.py
│   ├── database/load_postgres.py
│   └── prioritization/crm_priority.py
├── tests/                     # Automated unit, integration & reconciliation test suites
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Production Python dependencies
└── .env.example               # Environment template
```

---

## 4. Technology Stack

- **Web Framework:** FastAPI 0.110+
- **ASGI Server:** Uvicorn 0.28+
- **Database ORM:** SQLAlchemy 2.0+
- **Database Driver:** Psycopg2-binary 2.9+
- **Database Engine:** PostgreSQL 15+
- **Data Validation & Settings:** Pydantic v2 & Pydantic-Settings
- **Security & Hashing:** Bcrypt & PyJWT (HS256)
- **Data Transformation:** Pandas 2.2+ & NumPy 1.26+
- **Test Automation:** Pytest 8.0+ & HTTPX TestClient

---

## 5. Database Architecture

The PostgreSQL database (`crm_platform`) is structured into two schemas:

### `crm_sales` (Business Domain)
- **`accounts` (85 rows):** Master corporate account directory with parent-subsidiary self-referencing foreign key.
- **`products` (7 rows):** Product catalog with series and list sales prices.
- **`sales_teams` (35 rows):** Sales representative directory mapped to managers and regional offices.
- **`sales_pipeline` (8,800 rows):** Opportunity transactions with stages, engagement dates, close dates, close values, and foreign keys.
- **`prioritized_open_opportunities` (2,089 rows):** Deterministic priority scores, tiers, and age bands for all open deals.

### `crm_auth` (Application Infrastructure)
- **`app_users`:** Role-Based Access Control (RBAC) supporting `Admin`, `Sales Manager`, and `Sales Agent`. Decoupled from sales pipeline records.

---

## 6. API Catalog

All endpoints are prefixed with `/api/v1`. Interactive Swagger documentation is accessible at `http://localhost:8000/docs`.

| Route Prefix | Method | Endpoint | Description |
|---|---|---|---|
| **System** | `GET` | `/` | Service status and metadata |
| | `GET` | `/health` | Live PostgreSQL connectivity health check |
| **Auth** | `POST` | `/api/v1/auth/login` | JWT authentication |
| | `GET` | `/api/v1/auth/me` | Authenticated user profile |
| **Accounts** | `GET` | `/api/v1/accounts` | Filtered, searchable, sorted, paginated accounts |
| | `GET` | `/api/v1/accounts/summary` | Portfolio summary & tier distribution |
| | `GET` | `/api/v1/accounts/{id}` | Account profile with opportunity statistics |
| **Opportunities** | `GET` | `/api/v1/opportunities` | Filtered & paginated opportunities |
| | `GET` | `/api/v1/opportunities/{id}` | Opportunity detail with computed duration |
| **Pipeline** | `GET` | `/api/v1/pipeline/summary` | Official reconciliation KPI summary |
| | `GET` | `/api/v1/pipeline/stages` | Stage volumes & counts |
| | `GET` | `/api/v1/pipeline/products` | Pipeline breakdown by product |
| | `GET` | `/api/v1/pipeline/sectors` | Pipeline breakdown by sector |
| | `GET` | `/api/v1/pipeline/agents` | Pipeline breakdown by representative |
| | `GET` | `/api/v1/pipeline/managers` | Pipeline breakdown by sales manager |
| | `GET` | `/api/v1/pipeline/regions` | Pipeline breakdown by regional office |
| **Sales Agents** | `GET` | `/api/v1/agents` | Agent performance rankings |
| | `GET` | `/api/v1/agents/{name}` | Agent details, win rate & stage breakdown |
| **Sales Managers** | `GET` | `/api/v1/managers` | Manager list & team aggregate metrics |
| | `GET` | `/api/v1/managers/{name}` | Manager team member comparison |
| **Products** | `GET` | `/api/v1/products` | Product catalog with CRM performance |
| | `GET` | `/api/v1/products/{name}` | Product breakdown by sector & agent |
| **Prioritization** | `GET` | `/api/v1/prioritization` | Deterministic open opportunity ranking |
| | `GET` | `/api/v1/prioritization/summary` | Priority tier distribution |
| **Opportunity Aging** | `GET` | `/api/v1/aging/summary` | Operational aging band distributions |
| **Work Queues** | `GET` | `/api/v1/work-queues/summary` | Overview of all active CRM queues |
| | `GET` | `/api/v1/work-queues/high-priority` | Tier 1 high-priority review queue |
| | `GET` | `/api/v1/work-queues/stalled-deals` | Stalled active deals (> 180 days) queue |
| | `GET` | `/api/v1/work-queues/unassigned-accounts` | In-flight deals missing accounts queue |

---

## 7. CRM Business Logic

The platform strictly enforces the following mathematical and business definitions:

- **Pipeline Status:**
  - `Open`: Deal stage is `Prospecting` or `Engaging` (Total: 2,089).
  - `Closed`: Deal stage is `Won` or `Lost` (Total: 6,711).
- **Win Rate:**
  $$\text{Win Rate} = \frac{\text{Won}}{\text{Won} + \text{Lost}} \times 100\% = \frac{4,238}{4,238 + 2,473} \times 100\% = 63.15\%$$
- **Won Revenue:**
  $$\text{Won Revenue} = \sum \text{close\_value for Won opportunities} = \$10,005,534.00$$
- **Average Deal Size:**
  $$\text{Average Deal Size} = \frac{\$10,005,534.00}{4,238} = \$2,360.91$$
- **Average Sales Cycle:**
  $$\text{Average Sales Cycle} = \text{mean}(\text{close\_date} - \text{engage\_date}) = 47.99 \text{ days}$$

---

## 8. Opportunity Prioritization Framework

The platform implements an **interpretable, deterministic scoring system** for all 2,089 active open opportunities (`Prospecting`: 500, `Engaging`: 1,589).

> [!IMPORTANT]
> **Governance Notice:** This is an operational resource prioritization score (0–100 index) to sequence sales follow-ups and manager reviews. It is **NOT** a predictive win probability model and excludes all post-outcome variables (`close_date`, `close_value`).

### Prioritization Point Matrix (Max 100 Points):
1. **Lifecycle Stage (Max 30 pts):**
   - `Engaging`: 30 pts
   - `Prospecting`: 10 pts
2. **Product Catalog Value Tier (Max 30 pts):**
   - `High Value` ($\ge \$4,000$ list price): 30 pts (`GTK 500`, `GTX Plus Pro`, `GTX Pro`)
   - `Medium Value` ($\$1,000 - \$3,999$): 20 pts (`MG Advanced`, `GTX Plus Basic`)
   - `Low Value` ($< \$1,000$): 10 pts (`GTX Basic`, `MG Special`)
3. **Strategic Account Scale Tier (Max 25 pts):**
   - `Enterprise` (Revenue $\ge \$2,500\text{M}$ OR Employees $\ge 5,000$): 25 pts
   - `Mid-Market` (Revenue $\$500\text{M}-\$2,500\text{M}$ OR Employees $1,000-5,000$): 15 pts
   - `Commercial / Small` (Revenue $< \$500\text{M}$ AND Employees $< 1,000$): 10 pts
   - `Unassigned Account`: 5 pts
4. **Engagement Age & Urgency (Max 15 pts):**
   - `Recent (<= 90 days)`: 15 pts
   - `Aging (91 - 180 days)`: 10 pts
   - `Stalled / Critical (> 180 days)`: 5 pts
   - `Unengaged (Prospecting)`: 5 pts

### Priority Tiers:
- **Tier 1 — High Priority ($\ge 75$ pts):** 428 deals (Executive sponsor review, top reps)
- **Tier 2 — Medium Priority ($55 - 74$ pts):** 1,033 deals (Standard rep pipeline cadence)
- **Tier 3 — Lower Priority ($< 55$ pts):** 628 deals (Routine lead qualification/monitoring)
- **Total Open Population:** 2,089 deals

---

## 9. Testing & Quality Assurance

The project includes an automated test suite verifying business logic, database integrity, and REST API contracts.

### Executing Tests:
```bash
# Run the complete test suite
pytest

# Run tests with verbose output
pytest -v

# Run business reconciliation checkpoints specifically
pytest tests/test_business_reconciliation.py -v
```

### Verified Checkpoints:
All 65 automated tests pass cleanly with 100% precision:
- Total Opportunities: 8,800
- Won Opportunities: 4,238
- Lost Opportunities: 2,473
- Prospecting Deals: 500
- Engaging Deals: 1,589
- Open Opportunities: 2,089
- Closed Opportunities: 6,711
- Win Rate: 63.15%
- Won Revenue: $10,005,534.00
- Average Deal Size: $2,360.91
- Average Sales Cycle: 47.99 days
- Active Pipeline Agents: 30 / Total Team Agents: 35
- Accounts: 85 / Products: 7
- Priority Distribution: Tier 1 (428), Tier 2 (1,033), Tier 3 (628), Total = 2,089

---

## 10. Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ running locally or in a container

### 1. Clone & Navigate
```bash
cd CRM
```

### 2. Configure Environment
Copy the `.env.example` file to `.env` and fill in your database credentials:
```bash
cp .env.example .env
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Data Ingestion (Optional if already loaded)
```bash
# 1. Clean raw data
python src/data_cleaning/clean_sales.py

# 2. Compute opportunity priority scores
python src/prioritization/crm_priority.py

# 3. Ingest cleaned tables into PostgreSQL
python src/database/load_postgres.py
```

### 5. Launch the Backend Server
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
The API is now live at `http://127.0.0.1:8000`.

---

## 11. Environment Variables

Configure these settings in your `.env` file:

| Variable | Default | Description |
|---|---|---|
| `DB_HOST` | `localhost` | PostgreSQL host address |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `crm_platform` | PostgreSQL database name |
| `DB_USER` | `postgres` | Database username |
| `DB_PASSWORD` | `""` | Database password |
| `JWT_SECRET_KEY` | `crm-super-secret-production-key-change-in-env-2026` | Secret key for JWT signing |

---

## 12. API Usage Examples

### 1. Health Check
```bash
curl http://127.0.0.1:8000/health
```
```json
{
  "project": "Sales CRM & Pipeline Management Platform",
  "status": "healthy",
  "database": "healthy"
}
```

### 2. User Authentication
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@crm.local", "password": "AdminPass123!"}'
```

### 3. Retrieve Pipeline KPI Summary
```bash
curl http://127.0.0.1:8000/api/v1/pipeline/summary
```

### 4. Query Prioritized Open Opportunities (Tier 1)
```bash
curl "http://127.0.0.1:8000/api/v1/prioritization?tier=Tier%201&limit=5"
```

### 5. Access Stalled Deals Work Queue (> 180 Days)
```bash
curl "http://127.0.0.1:8000/api/v1/work-queues/stalled-deals?limit=10"
```

---

## 13. Data Integrity Decisions

1. **Strict Domain Isolation:** The platform models the B2B CRM sales dataset exclusively. No foreign domains (such as consumer telecom records) are linked.
2. **Zero Synthetic Records:** No fake customer records, contacts, sales calls, emails, or meetings are fabricated.
3. **Preservation of Legitimate Nulls:**
   - 1,425 open opportunities have `NULL` accounts representing early unassigned prospects.
   - 500 `Prospecting` opportunities have `NULL` engage dates.
   - Open opportunities have `NULL` close values.
4. **Transparent Data Corrections:** Documented standardizations (`GTXPro` $\rightarrow$ `GTX Pro`, `technolgy` $\rightarrow$ `technology`, `Philipines` $\rightarrow$ `Philippines`) are applied deterministically via script.

---

## 14. Known Limitations

1. **Snapshot Dataset:** The underlying sales data spans October 2016 through December 2017. In-flight deals remain static.
2. **Account-Level Granularity:** Opportunities are mapped to companies; individual stakeholder personas are not present in source records.
3. **Open Pipeline Valuation:** Open opportunities do not feature estimated values; open pipeline is measured by count, list price, and priority tier.
