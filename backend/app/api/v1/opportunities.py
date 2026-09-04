from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.opportunity import OpportunityRead, OpportunityDetail
from backend.app.schemas.common import PaginatedResponse, ApiResponse
from backend.app.services.opportunity_service import OpportunityService

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])

@router.get("", response_model=ApiResponse[PaginatedResponse[OpportunityRead]], summary="List and filter sales opportunities")
def list_opportunities(
    search: Optional[str] = Query(None, description="Search opportunity ID, account, agent, product"),
    account: Optional[str] = Query(None, description="Filter by account"),
    product: Optional[str] = Query(None, description="Filter by product name"),
    sales_agent: Optional[str] = Query(None, description="Filter by sales agent"),
    manager: Optional[str] = Query(None, description="Filter by sales manager"),
    deal_stage: Optional[str] = Query(None, description="Filter by stage: Prospecting, Engaging, Won, Lost"),
    pipeline_status: Optional[str] = Query(None, description="Filter by pipeline status: Open, Closed"),
    regional_office: Optional[str] = Query(None, description="Filter by regional office: Central, East, West"),
    min_close_value: Optional[float] = Query(None, description="Minimum close value"),
    max_close_value: Optional[float] = Query(None, description="Maximum close value"),
    engage_date_from: Optional[date] = Query(None, description="Engage date on or after"),
    engage_date_to: Optional[date] = Query(None, description="Engage date on or before"),
    close_date_from: Optional[date] = Query(None, description="Close date on or after"),
    close_date_to: Optional[date] = Query(None, description="Close date on or before"),
    sort_by: str = Query("opportunity_id", description="Sort field: opportunity_id, deal_stage, engage_date, close_date, close_value"),
    sort_desc: bool = Query(False, description="Sort descending"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Page size limit"),
    db: Session = Depends(get_db),
):
    service = OpportunityService(db)
    result = service.list_opportunities(
        search=search,
        account=account,
        product=product,
        sales_agent=sales_agent,
        manager=manager,
        deal_stage=deal_stage,
        pipeline_status=pipeline_status,
        regional_office=regional_office,
        min_close_value=min_close_value,
        max_close_value=max_close_value,
        engage_date_from=engage_date_from,
        engage_date_to=engage_date_to,
        close_date_from=close_date_from,
        close_date_to=close_date_to,
        sort_by=sort_by,
        sort_desc=sort_desc,
        page=page,
        limit=limit,
    )
    return ApiResponse(data=result)

@router.get("/{opportunity_id}", response_model=ApiResponse[OpportunityDetail], summary="Get opportunity detail")
def get_opportunity(opportunity_id: str, db: Session = Depends(get_db)):
    service = OpportunityService(db)
    detail = service.get_opportunity_detail(opportunity_id)
    return ApiResponse(data=detail)
