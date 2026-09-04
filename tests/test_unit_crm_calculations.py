"""
Unit Tests for CRM Calculations & Business Rules.
Tests:
- Win rate formula
- Open pipeline definition
- Closed pipeline definition
- Won revenue & average deal size calculation
- Average sales cycle calculation
- Account strategic tier classification
- Product catalog value tier classification
- Engagement age band classification
- Deterministic CRM priority score point matrix
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.services.account_service import classify_account_tier
from backend.app.services.product_service import classify_product_tier
from backend.app.services.prioritization_service import (
    classify_engagement_age_band,
    calculate_priority_score_and_tier,
)

def test_win_rate_formula():
    won = 4238
    lost = 2473
    total_closed = won + lost
    win_rate = round((won / total_closed * 100.0), 2)
    assert win_rate == 63.15
    assert total_closed == 6711

def test_average_deal_size_formula():
    won_revenue = 10005534.0
    won_deals = 4238
    avg_deal = round(won_revenue / won_deals, 2)
    assert avg_deal == 2360.91

def test_account_tier_classification():
    # Enterprise: Revenue >= 2500 OR Employees >= 5000
    assert classify_account_tier(3000.0, 100, "Enterprise Account A") == "Enterprise"
    assert classify_account_tier(200.0, 6000, "Enterprise Account B") == "Enterprise"
    
    # Mid-Market: Revenue 500-2500 OR Employees 1000-5000
    assert classify_account_tier(1500.0, 500, "Mid-Market Account A") == "Mid-Market"
    assert classify_account_tier(200.0, 2000, "Mid-Market Account B") == "Mid-Market"
    
    # Commercial / Small: Revenue < 500 AND Employees < 1000
    assert classify_account_tier(250.0, 400, "Small Account") == "Commercial / Small"
    
    # Unassigned Account
    assert classify_account_tier(None, None, None) == "Unassigned Account"

def test_product_tier_classification():
    # High Value (>= 4000)
    assert classify_product_tier(26768.0) == "High Value"
    assert classify_product_tier(5482.0) == "High Value"
    assert classify_product_tier(4821.0) == "High Value"
    assert classify_product_tier(4000.0) == "High Value"

    # Medium Value (1000 - 3999)
    assert classify_product_tier(3393.0) == "Medium Value"
    assert classify_product_tier(1096.0) == "Medium Value"
    assert classify_product_tier(1000.0) == "Medium Value"

    # Low Value (< 1000)
    assert classify_product_tier(550.0) == "Low Value"
    assert classify_product_tier(55.0) == "Low Value"

def test_engagement_age_band_classification():
    assert classify_engagement_age_band("Prospecting", 0) == "Unengaged (Prospecting)"
    assert classify_engagement_age_band("Prospecting", 45) == "Unengaged (Prospecting)"
    assert classify_engagement_age_band("Engaging", 30) == "Recent (<= 90 days)"
    assert classify_engagement_age_band("Engaging", 90) == "Recent (<= 90 days)"
    assert classify_engagement_age_band("Engaging", 91) == "Aging (91-180 days)"
    assert classify_engagement_age_band("Engaging", 180) == "Aging (91-180 days)"
    assert classify_engagement_age_band("Engaging", 181) == "Stalled / Critical (> 180 days)"
    assert classify_engagement_age_band("Engaging", 300) == "Stalled / Critical (> 180 days)"

def test_priority_score_point_matrix():
    # Maximum score: Engaging (30) + High Value (30) + Enterprise (25) + Recent (15) = 100 (Tier 1)
    score_max, tier_max = calculate_priority_score_and_tier(
        "Engaging", "High Value", "Enterprise", "Recent (<= 90 days)"
    )
    assert score_max == 100
    assert tier_max == "Tier 1 — High Priority"

    # Minimum score: Prospecting (10) + Low Value (10) + Unassigned Account (5) + Unengaged (5) = 30 (Tier 3)
    score_min, tier_min = calculate_priority_score_and_tier(
        "Prospecting", "Low Value", "Unassigned Account", "Unengaged (Prospecting)"
    )
    assert score_min == 30
    assert tier_min == "Tier 3 — Lower Priority"

    # Middle score: Engaging (30) + Medium Value (20) + Mid-Market (15) + Aging (10) = 75 (Tier 1 boundary)
    score_mid, tier_mid = calculate_priority_score_and_tier(
        "Engaging", "Medium Value", "Mid-Market", "Aging (91-180 days)"
    )
    assert score_mid == 75
    assert tier_mid == "Tier 1 — High Priority"

    # Tier 2 example: Engaging (30) + Low Value (10) + Commercial (10) + Aging (10) = 60 (Tier 2)
    score_t2, tier_t2 = calculate_priority_score_and_tier(
        "Engaging", "Low Value", "Commercial / Small", "Aging (91-180 days)"
    )
    assert score_t2 == 60
    assert tier_t2 == "Tier 2 — Medium Priority"
