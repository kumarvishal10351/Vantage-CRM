from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.prioritization import (
    PrioritizedOpportunityItem, PrioritizationSummaryResponse
)
from backend.app.schemas.common import PaginatedResponse, ApiResponse
from backend.app.services.prioritization_service import PrioritizationService

router = APIRouter(prefix="/prioritization", tags=["Opportunity Prioritization"])

@router.get("", response_model=ApiResponse[PaginatedResponse[PrioritizedOpportunityItem]], summary="Retrieve deterministically prioritized open opportunities")
def list_prioritized_opportunities(
    tier: Optional[str] = Query(None, description="Filter by priority tier: Tier 1, Tier 2, Tier 3"),
    sales_agent: Optional[str] = Query(None, description="Filter by sales agent"),
    product: Optional[str] = Query(None, description="Filter by product name"),
    account: Optional[str] = Query(None, description="Filter by account"),
    sector: Optional[str] = Query(None, description="Filter by account sector"),
    deal_stage: Optional[str] = Query(None, description="Filter by stage: Prospecting or Engaging"),
    sort_by: str = Query("crm_priority_score", description="Sort field: crm_priority_score, engagement_age_days, product_sales_price"),
    sort_desc: bool = Query(True, description="Sort descending"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Page size limit"),
    db: Session = Depends(get_db),
):
    """
    Returns open opportunities (Prospecting + Engaging, N=2,089) scored using the Phase 5 deterministic CRM Priority Score.
    Notice: CRM Priority Score is an operational prioritization index, not a predicted probability of winning.
    """
    service = PrioritizationService(db)
    result = service.list_prioritized_opportunities(
        tier=tier,
        sales_agent=sales_agent,
        product=product,
        account=account,
        sector=sector,
        deal_stage=deal_stage,
        sort_by=sort_by,
        sort_desc=sort_desc,
        page=page,
        limit=limit,
    )
    return ApiResponse(data=result)

@router.get("/summary", response_model=ApiResponse[PrioritizationSummaryResponse], summary="Summary distribution and operational workload across priority tiers")
def get_prioritization_summary(db: Session = Depends(get_db)):
    """
    Returns aggregate workload distribution across Tier 1, Tier 2, and Tier 3,
    along with representative and product level concentrations.
    """
    service = PrioritizationService(db)
    summary = service.get_summary()
    return ApiResponse(data=summary)
