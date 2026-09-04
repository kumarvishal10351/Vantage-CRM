from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class AgentBase(BaseModel):
    sales_agent: str
    manager: str
    regional_office: str

class SalesAgentRead(AgentBase):
    model_config = ConfigDict(from_attributes=True)

class AgentPerformance(AgentBase):
    total_opportunities: int
    open_opportunities: int
    won_opportunities: int
    lost_opportunities: int
    open_pipeline_value: float
    won_revenue: float
    win_rate: float
    average_deal_size: float
    average_sales_cycle_days: float
    performance_rank: Optional[int] = None

class SalesAgentDetail(SalesAgentRead):
    performance: AgentPerformance
    stage_breakdown: List[dict] = []
