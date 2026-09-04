from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from backend.app.models.sales_team import SalesTeam
from backend.app.models.opportunity import Opportunity
from backend.app.models.product import Product

class SalesTeamRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_agent(self, agent_name: str) -> Optional[SalesTeam]:
        return self.db.query(SalesTeam).filter(SalesTeam.sales_agent == agent_name).first()

    def list_agents(
        self,
        search: Optional[str] = None,
        manager: Optional[str] = None,
        regional_office: Optional[str] = None,
        sort_by: str = "sales_agent",
        sort_desc: bool = False,
    ) -> List[SalesTeam]:
        query = self.db.query(SalesTeam)

        if search:
            s = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    SalesTeam.sales_agent.ilike(s),
                    SalesTeam.manager.ilike(s),
                    SalesTeam.regional_office.ilike(s),
                )
            )

        if manager:
            query = query.filter(SalesTeam.manager.ilike(manager.strip()))

        if regional_office:
            query = query.filter(SalesTeam.regional_office.ilike(regional_office.strip()))

        sort_map = {
            "sales_agent": SalesTeam.sales_agent,
            "manager": SalesTeam.manager,
            "regional_office": SalesTeam.regional_office,
        }
        sort_col = sort_map.get(sort_by.lower(), SalesTeam.sales_agent)
        order_clause = desc(sort_col) if sort_desc else asc(sort_col)
        return query.order_by(order_clause).all()

    def get_agent_metrics(self, agent_name: str) -> dict:
        agent = self.get_agent(agent_name)
        if not agent:
            return {}

        opps = (
            self.db.query(Opportunity, Product.sales_price)
            .join(Product, Opportunity.product == Product.product)
            .filter(Opportunity.sales_agent == agent_name)
            .all()
        )

        total_opps = len(opps)
        won_opps = sum(1 for o, _ in opps if o.deal_stage == "Won")
        lost_opps = sum(1 for o, _ in opps if o.deal_stage == "Lost")
        open_opps = sum(1 for o, _ in opps if o.deal_stage in ("Prospecting", "Engaging"))
        won_revenue = sum(float(o.close_value or 0.0) for o, _ in opps if o.deal_stage == "Won")
        open_pipeline_val = sum(float(price or 0.0) for o, price in opps if o.deal_stage in ("Prospecting", "Engaging"))

        closed = won_opps + lost_opps
        win_rate = round((won_opps / closed * 100.0), 2) if closed > 0 else 0.0
        avg_deal_size = round((won_revenue / won_opps), 2) if won_opps > 0 else 0.0

        # Cycle days
        cycle_days = [
            (o.close_date - o.engage_date).days
            for o, _ in opps
            if o.deal_stage in ("Won", "Lost") and o.close_date and o.engage_date
        ]
        avg_cycle = round(sum(cycle_days) / len(cycle_days), 2) if cycle_days else 0.0

        # Stage breakdown
        stages = {}
        for o, price in opps:
            stg = o.deal_stage
            if stg not in stages:
                stages[stg] = {"count": 0, "value": 0.0}
            stages[stg]["count"] += 1
            if stg == "Won":
                stages[stg]["value"] += float(o.close_value or 0.0)
            elif stg in ("Prospecting", "Engaging"):
                stages[stg]["value"] += float(price or 0.0)

        stage_breakdown = [
            {"deal_stage": k, "opportunity_count": v["count"], "total_value": round(v["value"], 2)}
            for k, v in stages.items()
        ]

        return {
            "sales_agent": agent.sales_agent,
            "manager": agent.manager,
            "regional_office": agent.regional_office,
            "total_opportunities": total_opps,
            "open_opportunities": open_opps,
            "won_opportunities": won_opps,
            "lost_opportunities": lost_opps,
            "open_pipeline_value": round(open_pipeline_val, 2),
            "won_revenue": round(won_revenue, 2),
            "win_rate": win_rate,
            "average_deal_size": avg_deal_size,
            "average_sales_cycle_days": avg_cycle,
            "stage_breakdown": stage_breakdown,
        }

    def list_managers(self) -> List[Dict]:
        """Lists distinct managers with team sizes and regional offices."""
        teams = self.db.query(SalesTeam).all()
        managers_map = {}
        for t in teams:
            if t.manager not in managers_map:
                managers_map[t.manager] = {"regions": set(), "agents": []}
            managers_map[t.manager]["regions"].add(t.regional_office)
            managers_map[t.manager]["agents"].append(t.sales_agent)

        res = []
        for mgr, data in managers_map.items():
            res.append({
                "manager": mgr,
                "team_size": len(data["agents"]),
                "regional_offices": sorted(list(data["regions"])),
            })
        res.sort(key=lambda x: x["manager"])
        return res

    def get_manager_metrics(self, manager_name: str) -> dict:
        """Aggregates metrics for all agents reporting to this manager."""
        agents = self.db.query(SalesTeam).filter(SalesTeam.manager == manager_name).all()
        if not agents:
            return {}

        agent_names = [a.sales_agent for a in agents]
        regions = sorted(list(set(a.regional_office for a in agents)))

        opps = (
            self.db.query(Opportunity, Product.sales_price, SalesTeam.sales_agent)
            .join(Product, Opportunity.product == Product.product)
            .join(SalesTeam, Opportunity.sales_agent == SalesTeam.sales_agent)
            .filter(SalesTeam.manager == manager_name)
            .all()
        )

        total_opps = len(opps)
        won_opps = sum(1 for o, _, _ in opps if o.deal_stage == "Won")
        lost_opps = sum(1 for o, _, _ in opps if o.deal_stage == "Lost")
        open_opps = sum(1 for o, _, _ in opps if o.deal_stage in ("Prospecting", "Engaging"))
        won_revenue = sum(float(o.close_value or 0.0) for o, _, _ in opps if o.deal_stage == "Won")
        open_pipeline_val = sum(float(price or 0.0) for o, price, _ in opps if o.deal_stage in ("Prospecting", "Engaging"))

        closed = won_opps + lost_opps
        win_rate = round((won_opps / closed * 100.0), 2) if closed > 0 else 0.0
        avg_deal_size = round((won_revenue / won_opps), 2) if won_opps > 0 else 0.0

        # Team member individual performance
        team_members = [self.get_agent_metrics(a_name) for a_name in agent_names]
        team_members.sort(key=lambda x: x.get("won_revenue", 0.0), reverse=True)

        # Stage breakdown
        stages = {}
        for o, price, _ in opps:
            stg = o.deal_stage
            if stg not in stages:
                stages[stg] = {"count": 0, "value": 0.0}
            stages[stg]["count"] += 1
            if stg == "Won":
                stages[stg]["value"] += float(o.close_value or 0.0)
            elif stg in ("Prospecting", "Engaging"):
                stages[stg]["value"] += float(price or 0.0)

        stage_breakdown = [
            {"deal_stage": k, "opportunity_count": v["count"], "total_value": round(v["value"], 2)}
            for k, v in stages.items()
        ]

        return {
            "manager": manager_name,
            "team_size": len(agents),
            "regional_offices": regions,
            "total_opportunities": total_opps,
            "open_opportunities": open_opps,
            "won_opportunities": won_opps,
            "lost_opportunities": lost_opps,
            "open_pipeline_value": round(open_pipeline_val, 2),
            "won_revenue": round(won_revenue, 2),
            "win_rate": win_rate,
            "average_deal_size": avg_deal_size,
            "team_members": team_members,
            "stage_breakdown": stage_breakdown,
        }
