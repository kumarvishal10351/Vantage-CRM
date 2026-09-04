from pydantic import BaseModel, Field

class PipelineSummary(BaseModel):
    total_opportunities: int
    open_opportunities: int
    prospecting_opportunities: int
    engaging_opportunities: int
    won_opportunities: int
    lost_opportunities: int
    closed_opportunities: int
    pipeline_value: float = Field(..., description="Potential revenue of open opportunities (product list price)")
    won_revenue: float = Field(..., description="Actual closed revenue for Won deals")
    win_rate: float = Field(..., description="Won / (Won + Lost) * 100")
    average_deal_size: float = Field(..., description="Won revenue / Won opportunities")
    average_sales_cycle_days: float = Field(..., description="Average days from engage to close for closed deals")

class StageBreakdownItem(BaseModel):
    deal_stage: str
    opportunity_count: int
    percentage_of_total: float
    total_value: float

class PipelineDimensionItem(BaseModel):
    dimension_name: str
    dimension_value: str
    total_opportunities: int
    open_opportunities: int
    won_opportunities: int
    lost_opportunities: int
    won_revenue: float
    open_pipeline_value: float
    win_rate: float
    average_deal_size: float
