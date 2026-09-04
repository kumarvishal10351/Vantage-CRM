from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, ConfigDict

class OpportunityBase(BaseModel):
    opportunity_id: str
    sales_agent: str
    product: str
    account: Optional[str] = None
    deal_stage: str
    engage_date: Optional[date] = None
    close_date: Optional[date] = None
    close_value: Optional[float] = None

class OpportunityRead(OpportunityBase):
    model_config = ConfigDict(from_attributes=True)

    pipeline_status: str = Field(..., description="'Open' (Prospecting, Engaging) or 'Closed' (Won, Lost)")
    manager: Optional[str] = None
    regional_office: Optional[str] = None
    sector: Optional[str] = None
    product_series: Optional[str] = None
    product_sales_price: Optional[float] = None
    opportunity_age_days: int = 0
    priority_score: Optional[int] = None
    priority_tier: Optional[str] = None

class OpportunityDetail(OpportunityRead):
    account_revenue: Optional[float] = None
    account_employees: Optional[int] = None
    account_tier: Optional[str] = None
    product_value_tier: Optional[str] = None
    aging_band: Optional[str] = None
