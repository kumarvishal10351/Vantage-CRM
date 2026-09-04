from typing import List
from pydantic import BaseModel
from backend.app.schemas.agent import AgentPerformance

class SalesManagerRead(BaseModel):
    manager: str
    regional_offices: List[str]
    team_size: int

class ManagerPerformance(BaseModel):
    manager: str
    team_size: int
    regional_offices: List[str]
    total_opportunities: int
    open_opportunities: int
    won_opportunities: int
    lost_opportunities: int
    open_pipeline_value: float
    won_revenue: float
    win_rate: float
    average_deal_size: float

class SalesManagerDetail(ManagerPerformance):
    team_members: List[AgentPerformance] = []
    stage_breakdown: List[dict] = []
