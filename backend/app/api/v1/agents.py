from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.agent import AgentPerformance, SalesAgentDetail
from backend.app.schemas.common import ApiResponse
from backend.app.services.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["Sales Agents"])

@router.get("", response_model=ApiResponse[List[AgentPerformance]], summary="List all sales agents with performance metrics and ranking")
def list_agents(
    search: Optional[str] = Query(None, description="Search sales agent, manager, or regional office"),
    manager: Optional[str] = Query(None, description="Filter by manager"),
    regional_office: Optional[str] = Query(None, description="Filter by regional office"),
    sort_by: str = Query("won_revenue", description="Sort field: won_revenue, win_rate, total_opportunities, open_pipeline_value"),
    sort_desc: bool = Query(True, description="Sort descending"),
    db: Session = Depends(get_db),
):
    service = AgentService(db)
    agents = service.list_agents(
        search=search,
        manager=manager,
        regional_office=regional_office,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )
    return ApiResponse(data=agents)

@router.get("/{agent_name}", response_model=ApiResponse[SalesAgentDetail], summary="Get sales agent performance details and stage breakdown")
def get_agent(agent_name: str, db: Session = Depends(get_db)):
    service = AgentService(db)
    detail = service.get_agent_detail(agent_name)
    return ApiResponse(data=detail)
