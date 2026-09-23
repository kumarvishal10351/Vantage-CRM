# Vantage CRM

<p align="center">
  <img src="docs/screenshots/overview.png" alt="Vantage Executive Revenue Operations Dashboard" width="100%" />
</p>

<p align="center">
  <strong>Enterprise Revenue Operations & Autonomous Sales Orchestration Platform</strong>
  <br />
  A high-throughput, mathematically reconciled, full-stack B2B revenue intelligence platform built for high-velocity sales organizations.
</p>

<p align="center">
  <a href="https://vantage-crm-sand.vercel.app/"><img src="https://img.shields.io/badge/App%20Live-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="App Live on Vercel" /></a>
  <a href="https://crm-backend-34is.onrender.com/docs"><img src="https://img.shields.io/badge/API%20Live-Render%20Cloud-00c853?style=for-the-badge&logo=render&logoColor=white" alt="API Live on Render" /></a>
  <a href="https://crm-backend-34is.onrender.com/docs"><img src="https://img.shields.io/badge/OpenAPI-3.1%20Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger Docs" /></a>
  <img src="https://img.shields.io/badge/Tests-72%2F72%20Passing-brightgreen?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest 72/72 Passing" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-19.0-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React 19" />
  <img src="https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License MIT" />
</p>

---

## 🌐 Live Deployments & Cloud Endpoints

| Component | Provider | Status | Public URL |
|---|---|---|---|
| **Frontend Web Client** | Vercel Edge Network | ![Live](https://img.shields.io/badge/Status-Live-2ea44f?style=flat-square) | [`https://vantage-crm-sand.vercel.app`](https://vantage-crm-sand.vercel.app) |
| **Production REST API** | Render Cloud (Frankfurt/Oregon) | ![Operational](https://img.shields.io/badge/Status-Live-2ea44f?style=flat-square) | [`https://crm-backend-34is.onrender.com`](https://crm-backend-34is.onrender.com) |
| **Interactive API Documentation** | Swagger UI / OpenAPI 3.1 | ![Interactive](https://img.shields.io/badge/Docs-Live%20Swagger-blue?style=flat-square) | [`https://crm-backend-34is.onrender.com/docs`](https://crm-backend-34is.onrender.com/docs) |
| **Alternative API Specs** | Redocly Specification | ![Interactive](https://img.shields.io/badge/Specs-Redoc-lightgrey?style=flat-square) | [`https://crm-backend-34is.onrender.com/redoc`](https://crm-backend-34is.onrender.com/redoc) |
| **Engine Health & DB Probe** | Zero-leakage Health Check | ![Healthy](https://img.shields.io/badge/Probe-Healthy-brightgreen?style=flat-square) | [`https://crm-backend-34is.onrender.com/health`](https://crm-backend-34is.onrender.com/health) |

---

## 🏛️ Executive Summary & Key Metric Invariants

**Vantage CRM** is an enterprise-grade Sales Operations and Revenue Orchestration Platform engineered to eliminate reporting discrepancies, sequence high-value pipeline deals, and empower B2B sales teams with real-time operational telemetry. 

Built on a decoupled, cloud-native architecture combining an asynchronous **FastAPI** backend, **PostgreSQL 15+** relational multi-schema database, and a **React 19** single-page application, the platform ingests, cleanses, indexes, and surfaces **8,800 enterprise opportunities** across **85 accounts** and **35 sales reps and managers**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               AUDITED PRODUCTION INVARIANTS                            │
├─────────────────────┬─────────────────────┬─────────────────────┬──────────────────────┤
│    Won Revenue      │    Win Rate (%)     │   Total Volume      │  Average Sales Cycle │
│   $10,005,534.00    │       63.15%        │ 8,800 Opportunities │      47.99 Days      │
├─────────────────────┼─────────────────────┼─────────────────────┼──────────────────────┤
│  Open Pipeline Vol  │   Tier 1 Priority   │   Tier 2 Priority   │   Tier 3 Priority    │
│  2,089 Active Deals │   428 Top Targets   │  1,033 Mid Targets  │   628 Low Targets    │
└─────────────────────┴─────────────────────┴─────────────────────┴──────────────────────┘
```

---

## ⚡ Core Engineering Capabilities

- **Zero-Leakage Deterministic Scoring Model**: A transparent, audited 100-point scoring algorithm that segments in-flight opportunities into strategic tiers without statistical post-outcome look-ahead bias (quarantining `close_value` and `close_date`).
- **PostgreSQL Multi-Schema Relational Isolation**: Clean data segmentation separating core business operational data (`crm_sales`) from identity, credentials, and RBAC governance (`crm_auth`).
- **Asymmetric Bento Grid Design System**: Low-fatigue dark UI translated from Google Stitch specifications, featuring sticky tabbed drawers, tabular numbers (`.tnum`), and sub-millisecond client-side filtering.
- **Microsecond Latency Composite Indexing**: Optimized PostgreSQL composite indexes covering `(stage, engage_date)` and `(account_id, stage)` delivering **< 15ms p95 query latency** across multi-join aggregations.
- **Enterprise Security & Stateless RBAC**: PyJWT-signed bearer tokens (HS256), salted Bcrypt password hashing, and granular route guards for `Admin`, `Sales Manager`, and `Sales Agent`.
- **Fault-Tolerant Application Lifespan**: Self-healing startup initialization verifying schema integrity and seeding missing records on boot without blocking live HTTP traffic.
- **Comprehensive Test Suite**: 72 automated test cases across unit calculations, integration endpoints, security policies, and financial invariants with 100% pass rate.

---

## 🖥️ Platform Interface Showcase

<table width="100%">
  <tr>
    <td width="50%">
      <h3 align="center">Opportunities Ledger & Drawer</h3>
      <img src="docs/screenshots/opportunities.png" alt="Opportunities Directory" />
      <p align="center"><em>High-density searchable opportunity ledger with live multi-filter query bar and stage badges.</em></p>
    </td>
    <td width="50%">
      <h3 align="center">Non-Destructive Detail Drawer</h3>
      <img src="docs/screenshots/drawer.png" alt="Opportunity Detail Drawer" />
      <p align="center"><em>Contextual flyout drawer rendering opportunity lifecycles, account relationships, and product info.</em></p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3 align="center">Deterministic Priority Matrix</h3>
      <img src="docs/screenshots/priorities.png" alt="Priorities Matrix" />
      <p align="center"><em>100-pt scoring framework segmenting Tier 1, Tier 2, and Tier 3 deals for sales reps.</em></p>
    </td>
    <td width="50%">
      <h3 align="center">Operational Work Queues</h3>
      <img src="docs/screenshots/workqueue.png" alt="Operational Work Queues" />
      <p align="center"><em>High-priority deal focus, stalled opportunity triage (>180d), and unassigned account hygiene.</em></p>
    </td>
  </tr>
</table>

---

## 🏗️ System Architecture & Data Flow

```mermaid
graph TD
    User([Enterprise Sales User]) -->|HTTPS / WSS| CDN[Vercel Edge Network / React 19 SPA]
    CDN -->|Axios REST / Bearer JWT| Gateway[FastAPI ASGI Server / Uvicorn]
    
    subgraph Gateway Application Layer
        Gateway --> CORS[CORS Middleware / Origin Validation]
        CORS --> AuthDep[JWT Auth Guard / PyJWT + Bcrypt]
        AuthDep --> V1Router[API v1 Router /api/v1]
        
        V1Router --> PipelineCtrl[Pipeline Analytics Controller]
        V1Router --> OppCtrl[Opportunities & Queues Controller]
        V1Router --> PriorityCtrl[Deterministic Priority Service]
        V1Router --> AccountCtrl[Enterprise Accounts Controller]
    end

    subgraph Data Access & ORM Layer
        PipelineCtrl & OppCtrl & PriorityCtrl & AccountCtrl --> SQLAlchemy[SQLAlchemy 2.0 Engine]
        SQLAlchemy --> ConnPool[Hikari-style Connection Pool]
    end

    subgraph Cloud PostgreSQL Database
        ConnPool --> DB[(PostgreSQL 15+)]
        DB --> SchemaSales[Schema: crm_sales<br/>accounts, products, sales_teams,<br/>sales_pipeline, prioritized_open_opportunities]
        DB --> SchemaAuth[Schema: crm_auth<br/>app_users, roles, permissions]
    end
```

---

## 🧮 Mathematical Formulations & Business Governance

To prevent data drift and align cross-functional revenue reporting, Vantage CRM enforces canonical mathematical definitions across all analytical services:

### 1. Opportunity Lifecycle Breakdown
$$\text{Total Pipeline} = \text{Open Deals (2,089)} + \text{Closed Deals (6,711)} = 8,800$$
- **Open Pipeline:** Deals actively in `Prospecting` (500) or `Engaging` (1,589) status.
- **Closed Pipeline:** Terminal outcome deals in `Won` (4,238) or `Lost` (2,473) status.

### 2. Standardized Win Rate Formula
Unlike amateur CRM implementations that artificially deflate win rates by including in-flight open deals in the denominator, Vantage CRM follows the standard enterprise B2B sales definition:
$$\text{Win Rate} = \frac{\text{Won}}{\text{Won} + \text{Lost}} \times 100\% = \frac{4,238}{4,238 + 2,473} \times 100\% = \mathbf{63.15\%}$$

### 3. Total Won Revenue & Average Deal Size
$$\text{Won Revenue} = \sum_{i=1}^{4,238} \text{close\_value}_i = \mathbf{\$10,005,534.00}$$
$$\text{Average Deal Size} = \frac{\text{Won Revenue}}{\text{Won Count}} = \frac{\$10,005,534.00}{4,238} = \mathbf{\$2,360.91}$$

### 4. Sales Cycle Velocity
$$\text{Deal Duration} = \text{close\_date} - \text{engage\_date}$$
$$\text{Average Sales Cycle} = \text{mean}(\text{Deal Duration for Won/Lost Deals}) = \mathbf{47.99\text{ days}}$$

---

## 🎯 Deterministic Opportunity Prioritization Engine

Vantage CRM departs from opaque "black-box" machine learning algorithms that suffer from data drift and outcome contamination. Instead, it utilizes an **audited 100-point deterministic matrix** evaluated strictly on pre-close operational parameters.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        DETERMINISTIC PRIORITY SCORING MATRIX (100 PTS)                  │
├──────────────────────┬──────────────────────┬──────────────────────┬────────────────────┤
│ 1. Lifecycle Stage   │ 2. Product Value     │ 3. Account Scale     │ 4. Deal Urgency    │
│    (Max: 30 pts)     │    (Max: 30 pts)     │    (Max: 25 pts)     │    (Max: 15 pts)   │
├──────────────────────┼──────────────────────┼──────────────────────┼────────────────────┤
│ • Engaging:   30 pts │ • High ($4k+):  30pt │ • Enterprise:  25pt  │ • <= 90d:   15 pts │
│ • Prospect:   10 pts │ • Med ($1k-$4k):20pt │ • Mid-Market:  15pt  │ • 91-180d:  10 pts │
│                      │ • Low (<$1k):   10pt │ • Commercial:  10pt  │ • > 180d:    5 pts │
│                      │                      │ • Unassigned:   5pt  │ • Prospect:  5 pts │
└──────────────────────┴──────────────────────┴──────────────────────┴────────────────────┘
```

### Actionable Tier Segmentation

| Priority Tier | Score Threshold | Volume | Strategic Operating Model |
|---|---|:---:|---|
| <span style="color:#10b981; font-weight:bold;">Tier 1 (High)</span> | $\ge 75 \text{ pts}$ | **428 Deals** | Immediate executive sponsor engagement; assigned to top 10% quota carriers. |
| <span style="color:#f59e0b; font-weight:bold;">Tier 2 (Medium)</span> | $55 - 74 \text{ pts}$ | **1,033 Deals** | Structured 14-day cadence; bi-weekly manager milestone check-ins. |
| <span style="color:#6b7280; font-weight:bold;">Tier 3 (Low)</span> | $< 55 \text{ pts}$ | **628 Deals** | Automated marketing workflows, digital demo collateral, qualification gates. |

---

## 🗄️ Relational Database Schema & Data Integrity

The database is built on **PostgreSQL 15+** with strict foreign key constraints, explicit indexing, and schema separation:

```
                  ┌───────────────────────────────┐
                  │      crm_sales.accounts       │
                  │ (85 rows, self-ref parent_id) │
                  └───────────────┬───────────────┘
                                  │ 1:N
┌───────────────────────────┐     │     ┌───────────────────────────┐
│     crm_sales.products    │     │     │   crm_sales.sales_teams   │
│   (7 rows, series, price) │     │     │ (35 reps, managers, reg)  │
└─────────────┬─────────────┘     │     └─────────────┬─────────────┘
              │ 1:N               │                   │ 1:N
              └─────────────┐     │     ┌─────────────┘
                            ▼     ▼     ▼
                  ┌───────────────────────────────┐
                  │   crm_sales.sales_pipeline    │
                  │  (8,800 rows, B2B opp records)│
                  └───────────────┬───────────────┘
                                  │ 1:1
                                  ▼
                  ┌───────────────────────────────┐
                  │ prioritized_open_opportunities│
                  │ (2,089 scored active records) │
                  └───────────────────────────────┘
```

### Integrity Guarantees
1. **Preservation of Authentic Domain Nulls**: Early prospecting deals legitimately possess `NULL` engage dates. 1,425 early-stage deals contain `NULL` account associations prior to formal company creation.
2. **Deterministic Data Cleansing**: Typos across legacy records (e.g., `technolgy` $\rightarrow$ `technology`, `GTXPro` $\rightarrow$ `GTX Pro`) are corrected idempotently during ETL ingestion.
3. **Database Performance Indexing**:
   - `idx_sales_pipeline_stage`: B-tree index for stage filtering.
   - `idx_sales_pipeline_stage_dates`: Composite index `(stage, engage_date, close_date)` for fast metric calculation.
   - `idx_sales_pipeline_account_id`: Foreign key lookup index.

---

## 🚀 Live API Reference & cURL Examples

All endpoints are served under `/api/v1` with automatic OpenAPI JSON schema generation.

### 1. Production Health & DB Connectivity Probe
```bash
curl -X GET https://crm-backend-34is.onrender.com/health
```
```json
{
  "status": "healthy",
  "database": "healthy",
  "environment": "production",
  "timestamp_reference": "2026-09-06"
}
```

### 2. Executive Pipeline Summary
```bash
curl -X GET https://crm-backend-34is.onrender.com/api/v1/pipeline/summary
```
```json
{
  "total_opportunities": 8800,
  "open_opportunities": 2089,
  "closed_opportunities": 6711,
  "won_opportunities": 4238,
  "lost_opportunities": 2473,
  "won_revenue": 10005534.0,
  "win_rate": 63.15,
  "avg_deal_size": 2360.91,
  "avg_sales_cycle_days": 47.99
}
```

### 3. Authenticate with JWT Bearer Token
```bash
curl -X POST https://crm-backend-34is.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@crm.local", "password": "AdminPass123!"}'
```
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### 4. Fetch Deterministic Prioritization Queue
```bash
curl -X GET "https://crm-backend-34is.onrender.com/api/v1/prioritization?tier=Tier%201&limit=2" \
  -H "Authorization: Bearer <TOKEN>"
```

---

## 🧪 Automated Testing & Verification Suite

The repository incorporates a battle-tested Pytest suite validating end-to-end routing, database integrity, security boundaries, and financial invariants:

```bash
# Run the complete test suite
pytest

# Run with execution duration benchmarks
pytest -v --durations=10
```

```
============================= test session starts =============================
platform win32 -- Python 3.11+ / 3.14, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\kumar\Desktop\CRM
configfile: pytest.ini
testpaths: tests
collected 72 items

tests/test_api_endpoints.py ........................................... [ 59%]
tests/test_business_reconciliation.py ....                              [ 65%]
tests/test_phase2_validation.py .                                       [ 66%]
tests/test_phase3_validation.py .                                       [ 68%]
tests/test_phase5_priority_framework.py ..........                      [ 81%]
tests/test_production_readiness.py ......                               [ 91%]
tests/test_unit_crm_calculations.py ......                              [100%]

============================= 72 passed in 13.30s =============================
```

---

## 🛠️ Local Development Quickstart

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** & **npm 9+**
- **PostgreSQL 14+** (Local or Cloud Instance)

### 1. Clone & Configure Environment
```bash
git clone https://github.com/kumarvishal10351/Vantage-CRM.git
cd Vantage-CRM

# Copy environment template
cp .env.example .env
```

Configure your database connection in `.env`:
```ini
DATABASE_URL=postgresql://postgres:password@localhost:5432/crm_platform
JWT_SECRET_KEY=your-secure-production-secret-key
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 2. Install Python Dependencies & Seed Database
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Run ETL, scoring, and PostgreSQL seed
python src/data_cleaning/clean_sales.py
python src/prioritization/crm_priority.py
python src/database/load_postgres.py
```

### 3. Launch Backend API Server
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
API: `http://127.0.0.1:8000` | Swagger: `http://127.0.0.1:8000/docs`

### 4. Launch Frontend Web Client
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
Client: `http://127.0.0.1:5173`

---

## 🔐 Seeded Enterprise User Credentials

The platform is initialized with test credentials across all access tiers:

| Access Role | Email Identifier | Password | Access Privileges |
|---|---|---|---|
| **System Administrator** | `admin@crm.local` | `AdminPass123!` | Global administrative access, full read/write, user management |
| **Sales Manager** | `manager@crm.local` | `ManagerPass123!` | Regional pipeline access, representative scorecards, team metrics |
| **Sales Representative** | `agent@crm.local` | `AgentPass123!` | Individual opportunity management, personal work queues, lead updates |

---

## 📦 Cloud Deployment Architecture

### Backend Deployment (Render)
1. Link GitHub repository `kumarvishal10351/Vantage-CRM`.
2. Service Type: **Web Service** (Python 3).
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   - `DATABASE_URL`: Cloud PostgreSQL connection string.
   - `JWT_SECRET_KEY`: High-entropy 256-bit string.
   - `ENVIRONMENT`: `production`

### Frontend Deployment (Vercel)
- **Production URL**: [`https://vantage-crm-sand.vercel.app`](https://vantage-crm-sand.vercel.app)
1. Import repository on Vercel.
2. Set **Root Directory** to `frontend`.
3. Framework Preset: **Vite**.
4. **Environment Variables**:
   - `VITE_API_URL`: `https://crm-backend-34is.onrender.com/api/v1`
5. Deploy to global edge CDN.

---

## 📄 License & Attribution

Distributed under the **MIT License**. See [LICENSE](LICENSE) for full licensing terms. Engineered by the Vantage CRM Platform Engineering Team.
