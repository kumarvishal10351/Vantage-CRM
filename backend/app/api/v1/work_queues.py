from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.work_queue import (
    WorkQueueOpportunityItem, WorkQueueSummaryItem
)
from backend.app.schemas.common import PaginatedResponse, ApiResponse
from backend.app.services.work_queue_service import WorkQueueService

router = APIRouter(prefix="/work-queues", tags=["CRM Work Queues"])

@router.get("/summary", response_model=ApiResponse[List[WorkQueueSummaryItem]], summary="Overview of all CRM operational work queues")
def get_work_queues_summary(db: Session = Depends(get_db)):
    service = WorkQueueService(db)
    summary = service.get_queues_summary()
    return ApiResponse(data=summary)

@router.get("/high-priority", response_model=ApiResponse[PaginatedResponse[WorkQueueOpportunityItem]], summary="Tier 1 High-Priority Executive / Manager Review Queue")
def get_tier1_review_queue(
    sales_agent: Optional[str] = Query(None, description="Filter by representative"),
    manager: Optional[str] = Query(None, description="Filter by manager"),
    product: Optional[str] = Query(None, description="Filter by product"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = WorkQueueService(db)
    result = service.get_tier1_review_queue(
        sales_agent=sales_agent, manager=manager, product=product, page=page, limit=limit
    )
    return ApiResponse(data=result)

@router.get("/stalled-deals", response_model=ApiResponse[PaginatedResponse[WorkQueueOpportunityItem]], summary="Stalled Deals Queue (active engaging deals > 180 days)")
def get_stalled_deals_queue(
    sales_agent: Optional[str] = Query(None, description="Filter by representative"),
    manager: Optional[str] = Query(None, description="Filter by manager"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = WorkQueueService(db)
    result = service.get_stalled_deals_queue(
        sales_agent=sales_agent, manager=manager, page=page, limit=limit
    )
    return ApiResponse(data=result)

@router.get("/unassigned-accounts", response_model=ApiResponse[PaginatedResponse[WorkQueueOpportunityItem]], summary="Unassigned Accounts Queue (open pipeline deals without account)")
def get_unassigned_accounts_queue(
    sales_agent: Optional[str] = Query(None, description="Filter by representative"),
    manager: Optional[str] = Query(None, description="Filter by manager"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = WorkQueueService(db)
    result = service.get_unassigned_accounts_queue(
        sales_agent=sales_agent, manager=manager, page=page, limit=limit
    )
    return ApiResponse(data=result)
