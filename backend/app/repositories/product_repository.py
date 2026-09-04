from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from backend.app.models.product import Product
from backend.app.models.opportunity import Opportunity
from backend.app.models.account import Account
from backend.app.models.sales_team import SalesTeam

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_name: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.product == product_name).first()

    def list_products(
        self,
        search: Optional[str] = None,
        series: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: str = "product",
        sort_desc: bool = False,
    ) -> List[Product]:
        query = self.db.query(Product)

        if search:
            s = f"%{search.strip()}%"
            query = query.filter(or_(Product.product.ilike(s), Product.series.ilike(s)))

        if series:
            query = query.filter(Product.series.ilike(series.strip()))

        if min_price is not None:
            query = query.filter(Product.sales_price >= min_price)

        if max_price is not None:
            query = query.filter(Product.sales_price <= max_price)

        sort_map = {
            "product": Product.product,
            "series": Product.series,
            "sales_price": Product.sales_price,
        }
        sort_col = sort_map.get(sort_by.lower(), Product.product)
        order_clause = desc(sort_col) if sort_desc else asc(sort_col)
        return query.order_by(order_clause).all()

    def get_product_metrics(self, product_name: str) -> dict:
        prod = self.get_by_id(product_name)
        if not prod:
            return {}

        opps = (
            self.db.query(Opportunity, Account.sector, SalesTeam.sales_agent)
            .outerjoin(Account, Opportunity.account == Account.account)
            .join(SalesTeam, Opportunity.sales_agent == SalesTeam.sales_agent)
            .filter(Opportunity.product == product_name)
            .all()
        )

        total_opps = len(opps)
        won_opps = sum(1 for o, _, _ in opps if o.deal_stage == "Won")
        lost_opps = sum(1 for o, _, _ in opps if o.deal_stage == "Lost")
        open_opps = sum(1 for o, _, _ in opps if o.deal_stage in ("Prospecting", "Engaging"))
        won_revenue = sum(float(o.close_value or 0.0) for o, _, _ in opps if o.deal_stage == "Won")
        open_pipeline_val = open_opps * float(prod.sales_price)

        closed = won_opps + lost_opps
        win_rate = round((won_opps / closed * 100.0), 2) if closed > 0 else 0.0
        avg_deal_size = round((won_revenue / won_opps), 2) if won_opps > 0 else 0.0

        # Performance by sector
        sector_agg = {}
        for o, sector, _ in opps:
            sec = sector or "Unassigned"
            if sec not in sector_agg:
                sector_agg[sec] = {"total": 0, "won": 0, "lost": 0, "revenue": 0.0}
            sector_agg[sec]["total"] += 1
            if o.deal_stage == "Won":
                sector_agg[sec]["won"] += 1
                sector_agg[sec]["revenue"] += float(o.close_value or 0.0)
            elif o.deal_stage == "Lost":
                sector_agg[sec]["lost"] += 1

        sector_list = []
        for s_name, data in sector_agg.items():
            c = data["won"] + data["lost"]
            wr = round((data["won"] / c * 100.0), 2) if c > 0 else 0.0
            sector_list.append({
                "sector": s_name,
                "total_opportunities": data["total"],
                "won_opportunities": data["won"],
                "won_revenue": round(data["revenue"], 2),
                "win_rate": wr,
            })
        sector_list.sort(key=lambda x: x["won_revenue"], reverse=True)

        # Performance by agent
        agent_agg = {}
        for o, _, agent in opps:
            if agent not in agent_agg:
                agent_agg[agent] = {"total": 0, "won": 0, "lost": 0, "revenue": 0.0}
            agent_agg[agent]["total"] += 1
            if o.deal_stage == "Won":
                agent_agg[agent]["won"] += 1
                agent_agg[agent]["revenue"] += float(o.close_value or 0.0)
            elif o.deal_stage == "Lost":
                agent_agg[agent]["lost"] += 1

        agent_list = []
        for a_name, data in agent_agg.items():
            c = data["won"] + data["lost"]
            wr = round((data["won"] / c * 100.0), 2) if c > 0 else 0.0
            agent_list.append({
                "sales_agent": a_name,
                "total_opportunities": data["total"],
                "won_opportunities": data["won"],
                "won_revenue": round(data["revenue"], 2),
                "win_rate": wr,
            })
        agent_list.sort(key=lambda x: x["won_revenue"], reverse=True)

        return {
            "total_opportunities": total_opps,
            "open_opportunities": open_opps,
            "won_opportunities": won_opps,
            "lost_opportunities": lost_opps,
            "open_pipeline_value": round(open_pipeline_val, 2),
            "won_revenue": round(won_revenue, 2),
            "win_rate": win_rate,
            "average_deal_size": avg_deal_size,
            "performance_by_sector": sector_list,
            "performance_by_agent": agent_list,
        }
