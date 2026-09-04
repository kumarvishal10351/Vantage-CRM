from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.aging import AgingSummaryResponse
from backend.app.schemas.common import ApiResponse
from backend.app.services.aging_service import AgingService

router = APIRouter(prefix="/aging", tags=["Opportunity Aging"])

@router.get("/summary", response_model=ApiResponse[AgingSummaryResponse], summary="Opportunity aging and cycle analysis")
def get_aging_summary(db: Session = Depends(get_db)):
    """
    Computes opportunity aging across 4 operational bands:
    - Recent (<= 90 days)
    - Aging (91-180 days)
    - Stalled / Critical (> 180 days)
    - Unengaged (Prospecting)
    Includes historical closed sales cycle metrics and breakdown by representative, product, and sector.
    """
    service = AgingService(db)
    summary = service.get_aging_summary()
    return ApiResponse(data=summary)
