"""
Comprehensive API Integration Test Suite.
Tests all endpoints using FastAPI TestClient:
- System & Health
- Auth (login, me, invalid credentials, unauthorized requests)
- Accounts (listing, filtering, pagination, search, sorting, detail, summary, 404 handling)
- Opportunities (listing, stage/agent/product/status filters, detail, 404 handling)
- Pipeline (KPI summary, stages, products, sectors, agents, managers, regions)
- Sales Agents (listing, detail, rankings)
- Sales Managers (listing, detail, team breakdowns)
- Products (listing, value tiers, detail)
- Opportunity Prioritization (deterministic listing, tier filters, summary)
- Opportunity Aging (summary, aging bands)
- Work Queues (summary, Tier 1 high priority, stalled deals, unassigned accounts)
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def auth_token(client):
    res = client.post("/api/v1/auth/login", json={"email": "admin@crm.local", "password": "AdminPass123!"})
    assert res.status_code == 200
    return res.json()["data"]["access_token"]

# --- System & Health ---
def test_root_endpoint(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "documentation" in data

def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["database"] == "healthy"

# --- Authentication ---
def test_auth_login_success(client):
    res = client.post("/api/v1/auth/login", json={"email": "admin@crm.local", "password": "AdminPass123!"})
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert "access_token" in body["data"]
    assert body["data"]["user"]["role"] == "Admin"

def test_auth_login_invalid_password(client):
    res = client.post("/api/v1/auth/login", json={"email": "admin@crm.local", "password": "WrongPassword"})
    assert res.status_code == 401
    body = res.json()
    assert body["success"] is False
    assert body["error"]["code"] == "UNAUTHORIZED"

def test_auth_me_with_token(client, auth_token):
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["email"] == "admin@crm.local"

def test_auth_me_without_token(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401

# --- Accounts ---
def test_list_accounts(client):
    res = client.get("/api/v1/accounts?limit=10&page=1")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data["items"]) == 10
    assert data["pagination"]["total_items"] == 85
    assert data["pagination"]["page"] == 1

def test_filter_accounts_by_sector(client):
    res = client.get("/api/v1/accounts?sector=technology")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["pagination"]["total_items"] == 12
    for item in data["items"]:
        assert item["sector"].lower() == "technology"

def test_get_account_summary(client):
    res = client.get("/api/v1/accounts/summary")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["total_accounts"] == 85
    assert data["sectors_count"] > 0
    assert "Enterprise" in data["tier_distribution"]

def test_get_account_detail(client):
    res = client.get("/api/v1/accounts/Acme Corporation")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["account"] == "Acme Corporation"
    assert "stats" in data
    assert "win_rate" in data["stats"]

def test_get_account_not_found(client):
    res = client.get("/api/v1/accounts/NonExistentAccount12345")
    assert res.status_code == 404
    assert res.json()["success"] is False

# --- Opportunities ---
def test_list_opportunities(client):
    res = client.get("/api/v1/opportunities?limit=25")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data["items"]) == 25
    assert data["pagination"]["total_items"] == 8800

def test_filter_opportunities_by_stage(client):
    res = client.get("/api/v1/opportunities?deal_stage=Won&limit=10")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["pagination"]["total_items"] == 4238
    for item in data["items"]:
        assert item["deal_stage"] == "Won"

def test_filter_opportunities_by_pipeline_status(client):
    res = client.get("/api/v1/opportunities?pipeline_status=Open&limit=10")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["pagination"]["total_items"] == 2089

    res_closed = client.get("/api/v1/opportunities?pipeline_status=Closed&limit=10")
    assert res_closed.status_code == 200
    assert res_closed.json()["data"]["pagination"]["total_items"] == 6711

def test_get_opportunity_detail(client):
    list_res = client.get("/api/v1/opportunities?limit=1")
    opp_id = list_res.json()["data"]["items"][0]["opportunity_id"]
    res = client.get(f"/api/v1/opportunities/{opp_id}")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["opportunity_id"] == opp_id
    assert "pipeline_status" in data

def test_get_opportunity_not_found(client):
    res = client.get("/api/v1/opportunities/INVALID_OPP_ID_999")
    assert res.status_code == 404

# --- Pipeline ---
def test_pipeline_summary_kpis(client):
    res = client.get("/api/v1/pipeline/summary")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["total_opportunities"] == 8800
    assert data["open_opportunities"] == 2089
    assert data["won_opportunities"] == 4238
    assert data["lost_opportunities"] == 2473
    assert data["win_rate"] == 63.15
    assert data["won_revenue"] == 10005534.0
    assert abs(data["average_deal_size"] - 2360.91) < 0.01

def test_pipeline_breakdowns(client):
    for endpoint in ["stages", "products", "sectors", "agents", "managers", "regions"]:
        res = client.get(f"/api/v1/pipeline/{endpoint}")
        assert res.status_code == 200
        data = res.json()["data"]
        assert len(data) > 0

# --- Sales Agents ---
def test_list_agents(client):
    res = client.get("/api/v1/agents")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) == 35

def test_get_agent_detail(client):
    list_res = client.get("/api/v1/agents")
    agent_name = list_res.json()["data"][0]["sales_agent"]
    res = client.get(f"/api/v1/agents/{agent_name}")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["sales_agent"] == agent_name
    assert "performance" in data
    assert "stage_breakdown" in data

# --- Sales Managers ---
def test_list_managers(client):
    res = client.get("/api/v1/managers")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) == 6

def test_get_manager_detail(client):
    list_res = client.get("/api/v1/managers")
    mgr_name = list_res.json()["data"][0]["manager"]
    res = client.get(f"/api/v1/managers/{mgr_name}")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["manager"] == mgr_name
    assert len(data["team_members"]) > 0

# --- Products ---
def test_list_products(client):
    res = client.get("/api/v1/products")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) == 7

def test_get_product_detail(client):
    res = client.get("/api/v1/products/GTX Pro")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["product"] == "GTX Pro"
    assert data["product_value_tier"] == "High Value"
    assert len(data["performance_by_sector"]) > 0

# --- Opportunity Prioritization ---
def test_prioritization_summary(client):
    res = client.get("/api/v1/prioritization/summary")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["total_open_opportunities"] == 2089
    dist = {d["tier"]: d["count"] for d in data["distribution"]}
    assert dist["Tier 1 — High Priority"] == 428
    assert dist["Tier 2 — Medium Priority"] == 1033
    assert dist["Tier 3 — Lower Priority"] == 628
    assert "governance_notice" in data

def test_list_prioritized_opportunities(client):
    res = client.get("/api/v1/prioritization?tier=Tier 1&limit=20")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["pagination"]["total_items"] == 428
    for item in data["items"]:
        assert "Tier 1" in item["priority_tier"]
        assert item["crm_priority_score"] >= 75

# --- Aging ---
def test_aging_summary(client):
    res = client.get("/api/v1/aging/summary")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["total_open_opportunities"] == 2089
    assert abs(data["average_closed_cycle_days"] - 47.99) < 0.05
    bands = {b["aging_band"]: b["count"] for b in data["band_distribution"]}
    assert sum(bands.values()) == 2089

# --- Work Queues ---
def test_work_queues_summary(client):
    res = client.get("/api/v1/work-queues/summary")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) == 3

def test_work_queues_endpoints(client):
    for q in ["high-priority", "stalled-deals", "unassigned-accounts"]:
        res = client.get(f"/api/v1/work-queues/{q}?limit=10")
        assert res.status_code == 200
        data = res.json()["data"]
        assert "pagination" in data
        assert "items" in data

# --- Comprehensive Edge Cases & Negative Scenarios ---
def test_auth_invalid_token(client):
    res = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer definitely_invalid_token_xyz"})
    assert res.status_code == 401
    body = res.json()
    assert "detail" in body

def test_accounts_sorting(client):
    res = client.get("/api/v1/accounts?sort_by=revenue&sort_desc=true&limit=5")
    assert res.status_code == 200
    items = res.json()["data"]["items"]
    assert len(items) == 5
    for i in range(len(items) - 1):
        assert items[i]["revenue"] >= items[i + 1]["revenue"]

def test_accounts_invalid_pagination(client):
    res_zero = client.get("/api/v1/accounts?page=0")
    assert res_zero.status_code == 422
    res_exceed = client.get("/api/v1/accounts?limit=500")
    assert res_exceed.status_code == 422

def test_opportunities_sorting(client):
    res = client.get("/api/v1/opportunities?deal_stage=Won&sort_by=close_value&sort_desc=true&limit=5")
    assert res.status_code == 200
    items = res.json()["data"]["items"]
    assert len(items) == 5
    for i in range(len(items) - 1):
        assert items[i]["close_value"] >= items[i + 1]["close_value"]

def test_opportunities_invalid_parameters(client):
    res = client.get("/api/v1/opportunities?page=-1")
    assert res.status_code == 422

def test_get_agent_not_found(client):
    res = client.get("/api/v1/agents/NonExistentAgent999")
    assert res.status_code == 404
    assert res.json()["success"] is False

def test_agents_sorting(client):
    res = client.get("/api/v1/agents?sort_by=win_rate&sort_desc=true")
    assert res.status_code == 200
    items = res.json()["data"]
    for i in range(len(items) - 1):
        assert items[i]["win_rate"] >= items[i + 1]["win_rate"]

def test_get_manager_not_found(client):
    res = client.get("/api/v1/managers/NonExistentManager999")
    assert res.status_code == 404
    assert res.json()["success"] is False

def test_get_product_not_found(client):
    res = client.get("/api/v1/products/NonExistentProduct999")
    assert res.status_code == 404
    assert res.json()["success"] is False

def test_products_filtering(client):
    res = client.get("/api/v1/products?series=GTX")
    assert res.status_code == 200
    items = res.json()["data"]
    assert len(items) > 0
    for p in items:
        assert p["series"] == "GTX"

def test_prioritization_invalid_tier_filter(client):
    res = client.get("/api/v1/prioritization?tier=Tier_NonExistent")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["pagination"]["total_items"] == 0
    assert len(data["items"]) == 0

def test_work_queues_pagination(client):
    res1 = client.get("/api/v1/work-queues/high-priority?page=1&limit=5")
    assert res1.status_code == 200
    data1 = res1.json()["data"]
    assert len(data1["items"]) == 5
    res2 = client.get("/api/v1/work-queues/high-priority?page=2&limit=5")
    assert res2.status_code == 200
    data2 = res2.json()["data"]
    assert len(data2["items"]) == 5
    ids1 = {i["opportunity_id"] for i in data1["items"]}
    ids2 = {i["opportunity_id"] for i in data2["items"]}
    assert len(ids1.intersection(ids2)) == 0

def test_work_queues_invalid_queue(client):
    res = client.get("/api/v1/work-queues/non-existent-queue-endpoint")
    assert res.status_code == 404

def test_database_failure_health_degraded(client):
    from backend.app.core.database import get_db
    from unittest.mock import MagicMock
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("Simulated DB failure")
    app.dependency_overrides[get_db] = lambda: mock_db
    try:
        res = client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "degraded"
        assert "unhealthy" in data["database"]
    finally:
        app.dependency_overrides.pop(get_db, None)

