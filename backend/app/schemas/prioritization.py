from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

GOVERNANCE_STATEMENT = (
    "CRM Priority Score is an operational prioritization index, not a predicted probability of winning. "
    "It is a deterministic rule-based framework for resource allocation and management review."
)

class PrioritizedOpportunityItem(BaseModel):
    opportunity_id: str
    sales_agent: str
    manager: Optional[str] = None
    regional_office: Optional[str] = None
    product: str
    product_series: str
    product_sales_price: float
    product_value_tier: str
    account: Optional[str] = None
    sector: Optional[str] = None
    account_revenue: Optional[float] = None
    account_employees: Optional[int] = None
    account_tier: str
    deal_stage: str
    engage_date: Optional[date] = None
    engagement_age_days: int
    engagement_age_band: str
    crm_priority_score: int
    priority_tier: str

class TierWorkloadItem(BaseModel):
    tier: str
    count: int
    percentage: float
    description: str

class AgentWorkloadItem(BaseModel):
    sales_agent: str
    manager: str
    regional_office: str
    total_open: int
    tier_1_count: int
    tier_2_count: int
    tier_3_count: int

class ProductWorkloadItem(BaseModel):
    product: str
    series: str
    sales_price: float
    total_open: int
    tier_1_count: int
    tier_2_count: int
    tier_3_count: int

class PrioritizationSummaryResponse(BaseModel):
    governance_notice: str = Field(default=GOVERNANCE_STATEMENT)
    total_open_opportunities: int
    distribution: List[TierWorkloadItem]
    top_agents_by_tier1: List[AgentWorkloadItem]
    products_workload: List[ProductWorkloadItem]
