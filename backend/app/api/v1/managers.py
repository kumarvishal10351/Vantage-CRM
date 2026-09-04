from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.manager import ManagerPerformance, SalesManagerDetail
from backend.app.schemas.common import ApiResponse
from backend.app.services.manager_service import ManagerService

router = APIRouter(prefix="/managers", tags=["Sales Managers"])

@router.get("", response_model=ApiResponse[List[ManagerPerformance]], summary="List all sales managers and aggregated team performance")
def list_managers(db: Session = Depends(get_db)):
    service = ManagerService(db)
    managers = service.list_managers()
    return ApiResponse(data=managers)

@router.get("/{manager_name}", response_model=ApiResponse[SalesManagerDetail], summary="Get manager team breakdown and representative metrics")
def get_manager(manager_name: str, db: Session = Depends(get_db)):
    service = ManagerService(db)
    detail = service.get_manager_detail(manager_name)
    return ApiResponse(data=detail)
