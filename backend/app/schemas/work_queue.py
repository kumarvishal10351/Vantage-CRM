from typing import Optional
from datetime import date
from pydantic import BaseModel

class WorkQueueOpportunityItem(BaseModel):
    opportunity_id: str
    sales_agent: str
    manager: str
    regional_office: str
    product: str
    product_sales_price: float
    account: Optional[str] = None
    sector: Optional[str] = None
    deal_stage: str
    engage_date: Optional[date] = None
    engagement_age_days: int
    crm_priority_score: Optional[int] = None
    priority_tier: Optional[str] = None
    action_needed: str

class WorkQueueSummaryItem(BaseModel):
    queue_name: str
    description: str
    item_count: int
    total_value: float
    recommended_owner_role: str
