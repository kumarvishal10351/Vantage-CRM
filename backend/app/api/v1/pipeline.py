from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.pipeline import (
    PipelineSummary, StageBreakdownItem, PipelineDimensionItem
)
from backend.app.schemas.common import ApiResponse
from backend.app.services.pipeline_service import PipelineService

router = APIRouter(prefix="/pipeline", tags=["Pipeline & Revenue"])

@router.get("/summary", response_model=ApiResponse[PipelineSummary], summary="Pipeline KPI overview and reconciliation figures")
def get_pipeline_summary(db: Session = Depends(get_db)):
    service = PipelineService(db)
    summary = service.get_summary()
    return ApiResponse(data=summary)

@router.get("/stages", response_model=ApiResponse[List[StageBreakdownItem]], summary="Opportunity counts and volume by deal stage")
def get_pipeline_stages(db: Session = Depends(get_db)):
    service = PipelineService(db)
    stages = service.get_stages()
    return ApiResponse(data=stages)

@router.get("/products", response_model=ApiResponse[List[PipelineDimensionItem]], summary="Pipeline performance grouped by product")
def get_pipeline_by_product(db: Session = Depends(get_db)):
    service = PipelineService(db)
    items = service.get_dimension_breakdown("product")
    return ApiResponse(data=items)

@router.get("/sectors", response_model=ApiResponse[List[PipelineDimensionItem]], summary="Pipeline performance grouped by industry sector")
def get_pipeline_by_sector(db: Session = Depends(get_db)):
    service = PipelineService(db)
    items = service.get_dimension_breakdown("sector")
    return ApiResponse(data=items)

@router.get("/agents", response_model=ApiResponse[List[PipelineDimensionItem]], summary="Pipeline performance grouped by sales agent")
def get_pipeline_by_agent(db: Session = Depends(get_db)):
    service = PipelineService(db)
    items = service.get_dimension_breakdown("sales_agent")
    return ApiResponse(data=items)

@router.get("/managers", response_model=ApiResponse[List[PipelineDimensionItem]], summary="Pipeline performance grouped by sales manager")
def get_pipeline_by_manager(db: Session = Depends(get_db)):
    service = PipelineService(db)
    items = service.get_dimension_breakdown("sales_manager")
    return ApiResponse(data=items)

@router.get("/regions", response_model=ApiResponse[List[PipelineDimensionItem]], summary="Pipeline performance grouped by regional office")
def get_pipeline_by_region(db: Session = Depends(get_db)):
    service = PipelineService(db)
    items = service.get_dimension_breakdown("regional_office")
    return ApiResponse(data=items)
