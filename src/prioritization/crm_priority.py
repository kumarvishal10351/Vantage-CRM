"""
Interpretable CRM Opportunity Prioritization Framework for Sales Operations.
Provides transparent, deterministic, rule-based operational prioritization for
active open sales opportunities (Prospecting + Engaging, N=2,089).

This is NOT a predictive win/loss model. It does not output win probabilities.
It provides a transparent CRM Priority Score (0-100) and Priority Tiers (Tier 1-3)
to guide sales-manager reviews and representative follow-up workflows.
"""

import os
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from config.settings import get_db_url

# Historical Snapshot Reference Date (Latest date in the dataset)
HISTORICAL_SNAPSHOT_DATE = pd.to_datetime('2017-12-31')

# Prohibited outcome variables that must NEVER influence priority scoring
PROHIBITED_OUTCOME_FIELDS = ['close_value', 'close_date']


def load_open_pipeline():
    """
    Loads currently active open opportunities (Prospecting and Engaging, N=2,089)
    joined with accounts, products, and sales teams.
    """
    engine = create_engine(get_db_url())
    
    query = """
    SELECT 
        sp.opportunity_id,
        sp.sales_agent,
        sp.product,
        sp.account,
        sp.deal_stage,
        sp.engage_date,
        a.sector,
        a.year_established,
        a.revenue AS account_revenue,
        a.employees AS account_employees,
        a.office_location AS account_office_location,
        a.subsidiary_of,
        p.series AS product_series,
        p.sales_price AS product_sales_price,
        st.manager AS agent_manager,
        st.regional_office AS agent_regional_office
    FROM crm_sales.sales_pipeline sp
    LEFT JOIN crm_sales.accounts a ON sp.account = a.account
    LEFT JOIN crm_sales.products p ON sp.product = p.product
    LEFT JOIN crm_sales.sales_teams st ON sp.sales_agent = st.sales_agent
    WHERE sp.deal_stage IN ('Prospecting', 'Engaging')
    ORDER BY sp.opportunity_id;
    """
    
    with engine.connect() as conn:
        df_open = pd.read_sql(query, conn)
    
    assert len(df_open) == 2089, f"Expected 2089 open opportunities, got {len(df_open)}"
    assert set(df_open['deal_stage'].unique()) == {'Prospecting', 'Engaging'}
    
    df_open['engage_date'] = pd.to_datetime(df_open['engage_date'])
    return df_open


def load_closed_pipeline_for_retrospective():
    """
    Loads historical closed opportunities (N=6,711) for retrospective validation only.
    """
    engine = create_engine(get_db_url())
    
    query = """
    SELECT 
        sp.opportunity_id,
        sp.sales_agent,
        sp.product,
        sp.account,
        sp.deal_stage,
        sp.engage_date,
        sp.close_date,
        sp.close_value,
        a.sector,
        a.year_established,
        a.revenue AS account_revenue,
        a.employees AS account_employees,
        a.office_location AS account_office_location,
        a.subsidiary_of,
        p.series AS product_series,
        p.sales_price AS product_sales_price,
        st.manager AS agent_manager,
        st.regional_office AS agent_regional_office
    FROM crm_sales.sales_pipeline sp
    LEFT JOIN crm_sales.accounts a ON sp.account = a.account
    LEFT JOIN crm_sales.products p ON sp.product = p.product
    LEFT JOIN crm_sales.sales_teams st ON sp.sales_agent = st.sales_agent
    WHERE sp.deal_stage IN ('Won', 'Lost')
    ORDER BY sp.opportunity_id;
    """
    
    with engine.connect() as conn:
        df_closed = pd.read_sql(query, conn)
    
    assert len(df_closed) == 6711
    df_closed['engage_date'] = pd.to_datetime(df_closed['engage_date'])
    df_closed['close_date'] = pd.to_datetime(df_closed['close_date'])
    return df_closed


def classify_product_tier(price: float) -> str:
    """
    Classifies product catalog list price into business value tiers.
    - High Value (>= $4,000): GTK 500 ($26,768), GTX Plus Pro ($5,482), GTX Pro ($4,821)
    - Medium Value ($1,000 - $3,999): MG Advanced ($3,393), GTX Plus Basic ($1,096)
    - Low Value (< $1,000): GTX Basic ($550), MG Special ($55)
    """
    if pd.isna(price) or price <= 0:
        return 'Low Value'
    elif price >= 4000:
        return 'High Value'
    elif price >= 1000:
        return 'Medium Value'
    else:
        return 'Low Value'


def classify_account_tier(row: pd.Series) -> str:
    """
    Classifies accounts into strategic corporate scale tiers based on revenue and headcount.
    - Enterprise: Revenue >= $2,500M OR Employees >= 5,000 (Top quartile scale)
    - Mid-Market: Revenue $500M - $2,500M OR Employees 1,000 - 5,000
    - Commercial / Small: Revenue < $500M AND Employees < 1,000
    - Unassigned Account: No account linked (early-stage / prospecting)
    """
    if pd.isna(row.get('account')) or row.get('account') is None:
        return 'Unassigned Account'
    
    rev = row.get('account_revenue', np.nan)
    emp = row.get('account_employees', np.nan)
    
    if pd.isna(rev) and pd.isna(emp):
        return 'Unassigned Account'
        
    rev_val = float(rev) if pd.notna(rev) else 0.0
    emp_val = float(emp) if pd.notna(emp) else 0.0
    
    if rev_val >= 2500 or emp_val >= 5000:
        return 'Enterprise'
    elif rev_val >= 500 or emp_val >= 1000:
        return 'Mid-Market'
    else:
        return 'Commercial / Small'


def classify_engagement_age_band(stage: str, age_days: int) -> str:
    """
    Classifies engagement age into operational urgency bands.
    - Recent (<= 90 days): Fresh, active momentum
    - Aging (91 - 180 days): Approaching/exceeding standard cycle (avg 48 days)
    - Stalled / Critical (> 180 days): Pipeline clutter / high-risk aging
    - Unengaged (Prospecting): Lead not yet in active engagement
    """
    if stage == 'Prospecting' or pd.isna(age_days) or age_days == 0:
        return 'Unengaged (Prospecting)'
    elif age_days <= 90:
        return 'Recent (<= 90 days)'
    elif age_days <= 180:
        return 'Aging (91-180 days)'
    else:
        return 'Stalled / Critical (> 180 days)'


def calculate_crm_priority_score(
    df: pd.DataFrame,
    snapshot_date: pd.Timestamp = HISTORICAL_SNAPSHOT_DATE,
    is_retrospective: bool = False
) -> pd.DataFrame:
    """
    Computes deterministic CRM Priority Score (0-100) and Priority Tiers (Tier 1-3)
    using only observable pre-outcome CRM dimensions.
    """
    res = df.copy()
    
    # 1. Engagement Age Calculation
    if is_retrospective:
        # In retrospective closed deals, age is total cycle duration
        res['engagement_age_days'] = (res['close_date'] - res['engage_date']).dt.days.fillna(0).astype(int)
    else:
        res['engagement_age_days'] = np.where(
            res['engage_date'].notna(),
            (snapshot_date - res['engage_date']).dt.days,
            0
        ).astype(int)
    
    # 2. Product Value Tier
    res['product_value_tier'] = res['product_sales_price'].apply(classify_product_tier)
    
    # 3. Account Strategic Tier
    res['account_tier'] = res.apply(classify_account_tier, axis=1)
    
    # 4. Engagement Age Band
    res['engagement_age_band'] = res.apply(
        lambda r: classify_engagement_age_band(r['deal_stage'], r['engagement_age_days']),
        axis=1
    )
    
    # 5. Additive Score Weighting (Max 100 Points):
    # Dimension A: Deal Lifecycle Stage (Max 30 pts)
    stage_pts = np.where(res['deal_stage'] == 'Engaging', 30, 10)
    
    # Dimension B: Product Catalog Value Tier (Max 30 pts)
    prod_map = {'High Value': 30, 'Medium Value': 20, 'Low Value': 10}
    prod_pts = res['product_value_tier'].map(prod_map).fillna(10).astype(int)
    
    # Dimension C: Account Strategic Scale Tier (Max 25 pts)
    acc_map = {
        'Enterprise': 25,
        'Mid-Market': 15,
        'Commercial / Small': 10,
        'Unassigned Account': 5
    }
    acc_pts = res['account_tier'].map(acc_map).fillna(5).astype(int)
    
    # Dimension D: Engagement Age & Urgency (Max 15 pts)
    age_map = {
        'Recent (<= 90 days)': 15,
        'Aging (91-180 days)': 10,
        'Stalled / Critical (> 180 days)': 5,
        'Unengaged (Prospecting)': 5
    }
    age_pts = res['engagement_age_band'].map(age_map).fillna(5).astype(int)
    
    # Total Composite Priority Score (Range: 25 - 100)
    res['crm_priority_score'] = stage_pts + prod_pts + acc_pts + age_pts
    
    # 6. Priority Tiers
    # Tier 1 — High Priority (>= 75 pts): Executive & Manager Attention
    # Tier 2 — Medium Priority (55 - 74 pts): Standard Rep Follow-up
    # Tier 3 — Lower Priority (< 55 pts): Routine Monitoring / Qualification
    res['priority_tier'] = pd.cut(
        res['crm_priority_score'],
        bins=[0, 54, 74, 100],
        labels=['Tier 3 — Lower Priority', 'Tier 2 — Medium Priority', 'Tier 1 — High Priority']
    )
    
    return res


def prioritize_open_pipeline():
    """
    Executes prioritization scoring on the 2,089 active open opportunities
    and persists output to data/processed/crm_sales/prioritized_open_opportunities.csv.
    """
    df_open = load_open_pipeline()
    scored = calculate_crm_priority_score(df_open, snapshot_date=HISTORICAL_SNAPSHOT_DATE, is_retrospective=False)
    
    # Output Schema
    output_cols = [
        'opportunity_id',
        'sales_agent',
        'product',
        'product_series',
        'account',
        'sector',
        'account_revenue',
        'account_employees',
        'deal_stage',
        'engage_date',
        'engagement_age_days',
        'account_tier',
        'product_value_tier',
        'engagement_age_band',
        'crm_priority_score',
        'priority_tier'
    ]
    
    out_df = scored[output_cols].copy()
    
    out_dir = os.path.join('data', 'processed', 'crm_sales')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'prioritized_open_opportunities.csv')
    out_df.to_csv(out_file, index=False)
    print(f"Persisted {len(out_df)} prioritized open opportunities to {out_file}")
    
    return out_df


def run_retrospective_diagnostic():
    """
    Applies the scoring rules to the 6,711 closed deals to evaluate historical win rates
    across priority tiers (Diagnostic check only; not predictive validation).
    """
    df_closed = load_closed_pipeline_for_retrospective()
    scored_closed = calculate_crm_priority_score(df_closed, is_retrospective=True)
    scored_closed['is_won'] = (scored_closed['deal_stage'] == 'Won').astype(int)
    
    retro_summary = scored_closed.groupby('priority_tier', observed=False).agg(
        total_opportunities=('is_won', 'count'),
        won_opportunities=('is_won', 'sum'),
        lost_opportunities=('is_won', lambda x: (x == 0).sum()),
        retrospective_win_rate=('is_won', lambda x: round(float(x.mean() * 100), 2))
    ).reset_index()
    
    return retro_summary

if __name__ == '__main__':
    prioritize_open_pipeline()
    print("\nRetrospective Diagnostic Summary:")
    print(run_retrospective_diagnostic().to_string(index=False))
