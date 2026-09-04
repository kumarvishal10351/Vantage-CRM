from typing import List
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    product: str
    series: str
    sales_price: float

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_value_tier: str = Field(..., description="'High Value' (>= $4k), 'Medium Value' ($1k-$4k), 'Low Value' (< $1k)")

class ProductPerformance(ProductRead):
    total_opportunities: int
    open_opportunities: int
    won_opportunities: int
    lost_opportunities: int
    open_pipeline_value: float
    won_revenue: float
    win_rate: float
    average_deal_size: float

class ProductDetail(ProductPerformance):
    performance_by_sector: List[dict] = []
    performance_by_agent: List[dict] = []
