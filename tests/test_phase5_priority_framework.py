"""
Test Suite for Phase 5 Interpretable CRM Opportunity Prioritization.
Verifies:
1. Open opportunity population = 2,089
2. No Won/Lost records scored
3. No prohibited outcome fields used in scoring
4. Score range valid [25, 100]
5. Every record has exactly one priority tier
6. Re-running scoring produces deterministic identical results
7. Engagement age calculation correctness
8. Account tier calculation correctness
9. Product tier calculation correctness
"""

import os
import sys
import pytest
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.prioritization.crm_priority import (
    load_open_pipeline,
    classify_product_tier,
    classify_account_tier,
    calculate_crm_priority_score,
    prioritize_open_pipeline,
    run_retrospective_diagnostic,
    PROHIBITED_OUTCOME_FIELDS
)


def test_open_opportunity_population_count():
    """Verify open pipeline consists of exactly 2,089 records (500 Prospecting + 1,589 Engaging)."""
    df_open = load_open_pipeline()
    assert len(df_open) == 2089
    
    stage_counts = df_open['deal_stage'].value_counts().to_dict()
    assert stage_counts.get('Engaging') == 1589
    assert stage_counts.get('Prospecting') == 500


def test_no_closed_records_in_scoring():
    """Verify no Won or Lost records exist in the open scoring dataset."""
    df_open = load_open_pipeline()
    assert 'Won' not in df_open['deal_stage'].values
    assert 'Lost' not in df_open['deal_stage'].values


def test_no_prohibited_outcome_fields():
    """Verify prohibited outcome fields (close_date, close_value) never enter open scoring."""
    df_open = load_open_pipeline()
    for field in PROHIBITED_OUTCOME_FIELDS:
        assert field not in df_open.columns, f"Prohibited outcome field {field} found in open pipeline"


def test_priority_score_range_validity():
    """Verify all priority scores fall within valid bounds [25, 100] and contain no NaNs."""
    df_open = load_open_pipeline()
    scored = calculate_crm_priority_score(df_open)
    
    scores = scored['crm_priority_score']
    assert not scores.isnull().any(), "Found NULL priority scores"
    assert (scores >= 25).all(), f"Found score < 25: {scores.min()}"
    assert (scores <= 100).all(), f"Found score > 100: {scores.max()}"


def test_every_record_has_one_tier():
    """Verify every open record belongs to exactly one priority tier."""
    df_open = load_open_pipeline()
    scored = calculate_crm_priority_score(df_open)
    
    tiers = scored['priority_tier']
    assert not tiers.isnull().any(), "Found unassigned priority tiers"
    assert set(tiers.unique()) == {
        'Tier 1 — High Priority',
        'Tier 2 — Medium Priority',
        'Tier 3 — Lower Priority'
    }
    assert len(tiers) == 2089


def test_deterministic_scoring_reproducibility():
    """Verify that re-running scoring produces byte-identical results."""
    df_open1 = load_open_pipeline()
    scored1 = calculate_crm_priority_score(df_open1)
    
    df_open2 = load_open_pipeline()
    scored2 = calculate_crm_priority_score(df_open2)
    
    pd.testing.assert_frame_equal(
        scored1[['crm_priority_score', 'priority_tier']],
        scored2[['crm_priority_score', 'priority_tier']]
    )


def test_engagement_age_calculation():
    """Verify engagement age is non-negative and correctly references snapshot date."""
    df_open = load_open_pipeline()
    scored = calculate_crm_priority_score(df_open, snapshot_date=pd.to_datetime('2017-12-31'))
    
    ages = scored['engagement_age_days']
    assert (ages >= 0).all(), "Found negative engagement age"
    
    # Prospecting deals must have age = 0
    prospecting_ages = scored.loc[scored['deal_stage'] == 'Prospecting', 'engagement_age_days']
    assert (prospecting_ages == 0).all()
    
    # Engaging deals must have age > 0 based on engage_date
    engaging_deals = scored[scored['deal_stage'] == 'Engaging']
    for _, row in engaging_deals.head(20).iterrows():
        expected_age = (pd.to_datetime('2017-12-31') - pd.to_datetime(row['engage_date'])).days
        assert row['engagement_age_days'] == expected_age


def test_account_tier_calculation():
    """Verify account tier classification logic across enterprise, mid-market, small, and unassigned."""
    row_ent1 = pd.Series({'account': 'Test Corp', 'account_revenue': 3000.0, 'account_employees': 2000})
    row_ent2 = pd.Series({'account': 'Test Corp 2', 'account_revenue': 1000.0, 'account_employees': 6000})
    row_mid = pd.Series({'account': 'Test Mid', 'account_revenue': 1500.0, 'account_employees': 2500})
    row_small = pd.Series({'account': 'Test Small', 'account_revenue': 200.0, 'account_employees': 500})
    row_unassigned = pd.Series({'account': None, 'account_revenue': np.nan, 'account_employees': np.nan})
    
    assert classify_account_tier(row_ent1) == 'Enterprise'
    assert classify_account_tier(row_ent2) == 'Enterprise'
    assert classify_account_tier(row_mid) == 'Mid-Market'
    assert classify_account_tier(row_small) == 'Commercial / Small'
    assert classify_account_tier(row_unassigned) == 'Unassigned Account'


def test_product_tier_calculation():
    """Verify product tier classification logic across high, medium, and low catalog prices."""
    assert classify_product_tier(26768.0) == 'High Value'
    assert classify_product_tier(5482.0) == 'High Value'
    assert classify_product_tier(4821.0) == 'High Value'
    assert classify_product_tier(3393.0) == 'Medium Value'
    assert classify_product_tier(1096.0) == 'Medium Value'
    assert classify_product_tier(550.0) == 'Low Value'
    assert classify_product_tier(55.0) == 'Low Value'


def test_persisted_dataset_and_retrospective():
    """Verify that prioritize_open_pipeline generates valid CSV and retrospective diagnostic runs."""
    out_df = prioritize_open_pipeline()
    assert len(out_df) == 2089
    assert os.path.isfile(os.path.join('data', 'processed', 'crm_sales', 'prioritized_open_opportunities.csv'))
    
    retro_df = run_retrospective_diagnostic()
    assert len(retro_df) == 3
    assert retro_df['total_opportunities'].sum() == 6711

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
