"""
Business KPI Reconciliation Test Suite.
Verifies all 14 official checkpoints against both PostgreSQL database and backend services:
1. Total Opportunities = 8,800
2. Won Opportunities = 4,238
3. Lost Opportunities = 2,473
4. Prospecting = 500
5. Engaging = 1,589
6. Open Opportunities = 2,089
7. Closed Opportunities = 6,711
8. Win Rate = 63.15%
9. Won Revenue = $10,005,534.00
10. Average Deal Size ≈ $2,360.91
11. Average Sales Cycle ≈ 47.99 days
12. 30 active agents in pipeline, 35 total in sales team
13. 85 accounts, 7 products
14. Deterministic Prioritization: Tier 1 = 428, Tier 2 = 1,033, Tier 3 = 628, Total = 2,089
"""

import sys
import os
import psycopg2
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import get_db_params
from backend.app.core.database import SessionLocal
from backend.app.services.pipeline_service import PipelineService
from backend.app.services.prioritization_service import PrioritizationService

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()

def test_pipeline_counts_reconciliation(db_session):
    pipeline_service = PipelineService(db_session)
    summary = pipeline_service.get_summary()

    # 1. Total Opportunities = 8,800
    assert summary.total_opportunities == 8800

    # 2. Won Opportunities = 4,238
    assert summary.won_opportunities == 4238

    # 3. Lost Opportunities = 2,473
    assert summary.lost_opportunities == 2473

    # 4. Prospecting = 500
    assert summary.prospecting_opportunities == 500

    # 5. Engaging = 1,589
    assert summary.engaging_opportunities == 1589

    # 6. Open Opportunities = 2,089
    assert summary.open_opportunities == 2089
    assert summary.open_opportunities == summary.prospecting_opportunities + summary.engaging_opportunities

    # 7. Closed Opportunities = 6,711
    assert summary.closed_opportunities == 6711
    assert summary.closed_opportunities == summary.won_opportunities + summary.lost_opportunities

    # Total check
    assert summary.open_opportunities + summary.closed_opportunities == summary.total_opportunities

def test_pipeline_financial_kpis_reconciliation(db_session):
    pipeline_service = PipelineService(db_session)
    summary = pipeline_service.get_summary()

    # 8. Win Rate = 63.15%
    assert summary.win_rate == 63.15

    # 9. Won Revenue = $10,005,534
    assert summary.won_revenue == 10005534.0

    # 10. Average Deal Size ≈ $2,360.91
    assert abs(summary.average_deal_size - 2360.91) < 0.01

    # 11. Average Sales Cycle ≈ 47.99 days
    assert abs(summary.average_sales_cycle_days - 47.99) < 0.05

def test_master_entity_counts_reconciliation(db_session):
    conn = psycopg2.connect(**get_db_params())
    cur = conn.cursor()

    # 12. 30 active agents in pipeline, 35 total in sales team
    cur.execute("SELECT COUNT(DISTINCT sales_agent) FROM crm_sales.sales_pipeline")
    active_agents = cur.fetchone()[0]
    assert active_agents == 30

    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_teams")
    total_agents = cur.fetchone()[0]
    assert total_agents == 35

    # 13. 85 accounts, 7 products
    cur.execute("SELECT COUNT(*) FROM crm_sales.accounts")
    accounts_count = cur.fetchone()[0]
    assert accounts_count == 85

    cur.execute("SELECT COUNT(*) FROM crm_sales.products")
    products_count = cur.fetchone()[0]
    assert products_count == 7

    conn.close()

def test_prioritization_distribution_reconciliation(db_session):
    prio_service = PrioritizationService(db_session)
    summary = prio_service.get_summary()

    # Total open population
    assert summary.total_open_opportunities == 2089

    tier_map = {item.tier: item.count for item in summary.distribution}

    # 14. Prioritization: Tier 1 = 428, Tier 2 = 1,033, Tier 3 = 628, Total = 2,089
    assert tier_map["Tier 1 — High Priority"] == 428
    assert tier_map["Tier 2 — Medium Priority"] == 1033
    assert tier_map["Tier 3 — Lower Priority"] == 628
    assert sum(tier_map.values()) == 2089
