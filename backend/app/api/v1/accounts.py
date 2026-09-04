from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.account import AccountRead, AccountDetail, AccountSummaryResponse
from backend.app.schemas.common import PaginatedResponse, ApiResponse
from backend.app.services.account_service import AccountService

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("", response_model=ApiResponse[PaginatedResponse[AccountRead]], summary="List, search, and filter CRM accounts")
def list_accounts(
    search: Optional[str] = Query(None, description="Search account name, sector, location"),
    sector: Optional[str] = Query(None, description="Filter by account industry sector"),
    office_location: Optional[str] = Query(None, description="Filter by office country/location"),
    tier: Optional[str] = Query(None, description="Filter by strategic tier: Enterprise, Mid-Market, Commercial / Small"),
    min_revenue: Optional[float] = Query(None, description="Minimum corporate revenue in millions"),
    max_revenue: Optional[float] = Query(None, description="Maximum corporate revenue in millions"),
    has_subsidiary: Optional[bool] = Query(None, description="Filter by whether account has child subsidiaries"),
    sort_by: str = Query("account", description="Sort field: account, revenue, employees, year_established, sector"),
    sort_desc: bool = Query(False, description="Sort in descending order"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Page size limit"),
    db: Session = Depends(get_db),
):
    service = AccountService(db)
    result = service.list_accounts(
        search=search,
        sector=sector,
        office_location=office_location,
        tier=tier,
        min_revenue=min_revenue,
        max_revenue=max_revenue,
        has_subsidiary=has_subsidiary,
        sort_by=sort_by,
        sort_desc=sort_desc,
        page=page,
        limit=limit,
    )
    return ApiResponse(data=result)

@router.get("/summary", response_model=ApiResponse[AccountSummaryResponse], summary="Get overall account portfolio summary")
def get_account_summary(db: Session = Depends(get_db)):
    service = AccountService(db)
    summary = service.get_account_summary()
    return ApiResponse(data=summary)

@router.get("/{account_id}", response_model=ApiResponse[AccountDetail], summary="Get account detail with opportunity statistics")
def get_account(account_id: str, db: Session = Depends(get_db)):
    service = AccountService(db)
    detail = service.get_account_detail(account_id)
    return ApiResponse(data=detail)
