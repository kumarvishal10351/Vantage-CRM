from typing import List
from sqlalchemy.orm import Session
from backend.app.repositories.sales_team_repository import SalesTeamRepository
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.schemas.manager import ManagerPerformance, SalesManagerDetail
from backend.app.schemas.agent import AgentPerformance

class ManagerService:
    def __init__(self, db: Session):
        self.repo = SalesTeamRepository(db)

    def list_managers(self) -> List[ManagerPerformance]:
        managers_data = self.repo.list_managers()
        res = []
        for m in managers_data:
            mgr_name = m["manager"]
            metrics = self.repo.get_manager_metrics(mgr_name)
            res.append(
                ManagerPerformance(
                    manager=mgr_name,
                    team_size=metrics.get("team_size", m["team_size"]),
                    regional_offices=metrics.get("regional_offices", m["regional_offices"]),
                    total_opportunities=metrics.get("total_opportunities", 0),
                    open_opportunities=metrics.get("open_opportunities", 0),
                    won_opportunities=metrics.get("won_opportunities", 0),
                    lost_opportunities=metrics.get("lost_opportunities", 0),
                    open_pipeline_value=metrics.get("open_pipeline_value", 0.0),
                    won_revenue=metrics.get("won_revenue", 0.0),
                    win_rate=metrics.get("win_rate", 0.0),
                    average_deal_size=metrics.get("average_deal_size", 0.0),
                )
            )
        res.sort(key=lambda x: x.won_revenue, reverse=True)
        return res

    def get_manager_detail(self, manager_name: str) -> SalesManagerDetail:
        metrics = self.repo.get_manager_metrics(manager_name)
        if not metrics:
            raise EntityNotFoundException("Sales Manager", manager_name)

        team_perf = []
        for mem in metrics.get("team_members", []):
            team_perf.append(
                AgentPerformance(
                    sales_agent=mem["sales_agent"],
                    manager=mem["manager"],
                    regional_office=mem["regional_office"],
                    total_opportunities=mem["total_opportunities"],
                    open_opportunities=mem["open_opportunities"],
                    won_opportunities=mem["won_opportunities"],
                    lost_opportunities=mem["lost_opportunities"],
                    open_pipeline_value=mem["open_pipeline_value"],
                    won_revenue=mem["won_revenue"],
                    win_rate=mem["win_rate"],
                    average_deal_size=mem["average_deal_size"],
                    average_sales_cycle_days=mem["average_sales_cycle_days"],
                )
            )

        return SalesManagerDetail(
            manager=manager_name,
            team_size=metrics["team_size"],
            regional_offices=metrics["regional_offices"],
            total_opportunities=metrics["total_opportunities"],
            open_opportunities=metrics["open_opportunities"],
            won_opportunities=metrics["won_opportunities"],
            lost_opportunities=metrics["lost_opportunities"],
            open_pipeline_value=metrics["open_pipeline_value"],
            won_revenue=metrics["won_revenue"],
            win_rate=metrics["win_rate"],
            average_deal_size=metrics["average_deal_size"],
            team_members=team_perf,
            stage_breakdown=metrics.get("stage_breakdown", []),
        )
