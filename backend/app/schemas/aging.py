from typing import List, Dict
from pydantic import BaseModel

class AgingBandItem(BaseModel):
    aging_band: str
    count: int
    percentage: float
    total_pipeline_value: float

class DimensionAgingItem(BaseModel):
    dimension_value: str
    total_open_deals: int
    average_age_days: float
    stalled_deals_count: int

class AgingSummaryResponse(BaseModel):
    reference_date: str
    total_open_opportunities: int
    average_open_age_days: float
    average_closed_cycle_days: float
    band_distribution: List[AgingBandItem]
    aging_by_stage: List[Dict]
    top_aging_agents: List[DimensionAgingItem]
    aging_by_product: List[DimensionAgingItem]
    aging_by_sector: List[DimensionAgingItem]
