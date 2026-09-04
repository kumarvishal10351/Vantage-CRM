from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class AccountBase(BaseModel):
    account: str
    sector: str
    year_established: int
    revenue: float
    employees: int
    office_location: str
    subsidiary_of: Optional[str] = None

class AccountRead(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    account_tier: str = Field(..., description="Enterprise, Mid-Market, Commercial / Small")

class AccountStats(BaseModel):
    total_opportunities: int
    open_opportunities: int
    won_opportunities: int
    lost_opportunities: int
    won_revenue: float
    open_pipeline_value: float
    win_rate: float

class AccountDetail(AccountRead):
    stats: AccountStats
    subsidiaries_list: List[str] = []

class AccountSummaryResponse(BaseModel):
    total_accounts: int
    total_corporate_revenue: float
    total_employees: int
    sectors_count: int
    tier_distribution: dict
    top_sectors_by_revenue: List[dict]
