from typing import Optional, List
from sqlalchemy.orm import Session
from backend.app.repositories.sales_team_repository import SalesTeamRepository
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.schemas.agent import AgentPerformance, SalesAgentDetail

class AgentService:
    def __init__(self, db: Session):
        self.repo = SalesTeamRepository(db)

    def list_agents(
        self,
        search: Optional[str] = None,
        manager: Optional[str] = None,
        regional_office: Optional[str] = None,
        sort_by: str = "won_revenue",
        sort_desc: bool = True,
    ) -> List[AgentPerformance]:
        agents = self.repo.list_agents(
            search=search,
            manager=manager,
            regional_office=regional_office,
        )

        performances = []
        for a in agents:
            m = self.repo.get_agent_metrics(a.sales_agent)
            performances.append(
                AgentPerformance(
                    sales_agent=a.sales_agent,
                    manager=a.manager,
                    regional_office=a.regional_office,
                    total_opportunities=m.get("total_opportunities", 0),
                    open_opportunities=m.get("open_opportunities", 0),
                    won_opportunities=m.get("won_opportunities", 0),
                    lost_opportunities=m.get("lost_opportunities", 0),
                    open_pipeline_value=m.get("open_pipeline_value", 0.0),
                    won_revenue=m.get("won_revenue", 0.0),
                    win_rate=m.get("win_rate", 0.0),
                    average_deal_size=m.get("average_deal_size", 0.0),
                    average_sales_cycle_days=m.get("average_sales_cycle_days", 0.0),
                )
            )

        # Sort performances
        def sort_key(item: AgentPerformance):
            val = getattr(item, sort_by.lower(), None)
            return val if val is not None else 0

        try:
            performances.sort(key=sort_key, reverse=sort_desc)
        except Exception:
            performances.sort(key=lambda x: x.won_revenue, reverse=True)

        # Assign performance rank based on won revenue
        by_rev = sorted(performances, key=lambda x: x.won_revenue, reverse=True)
        rank_map = {item.sales_agent: idx + 1 for idx, item in enumerate(by_rev)}
        for p in performances:
            p.performance_rank = rank_map.get(p.sales_agent)

        return performances

    def get_agent_detail(self, agent_name: str) -> SalesAgentDetail:
        agent = self.repo.get_agent(agent_name)
        if not agent:
            raise EntityNotFoundException("Sales Agent", agent_name)

        metrics = self.repo.get_agent_metrics(agent_name)
        perf = AgentPerformance(
            sales_agent=agent.sales_agent,
            manager=agent.manager,
            regional_office=agent.regional_office,
            total_opportunities=metrics.get("total_opportunities", 0),
            open_opportunities=metrics.get("open_opportunities", 0),
            won_opportunities=metrics.get("won_opportunities", 0),
            lost_opportunities=metrics.get("lost_opportunities", 0),
            open_pipeline_value=metrics.get("open_pipeline_value", 0.0),
            won_revenue=metrics.get("won_revenue", 0.0),
            win_rate=metrics.get("win_rate", 0.0),
            average_deal_size=metrics.get("average_deal_size", 0.0),
            average_sales_cycle_days=metrics.get("average_sales_cycle_days", 0.0),
        )

        return SalesAgentDetail(
            sales_agent=agent.sales_agent,
            manager=agent.manager,
            regional_office=agent.regional_office,
            performance=perf,
            stage_breakdown=metrics.get("stage_breakdown", []),
        )
