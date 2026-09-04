from typing import Optional, List, Tuple, Dict
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from backend.app.models.opportunity import Opportunity
from backend.app.models.account import Account
from backend.app.models.product import Product
from backend.app.models.sales_team import SalesTeam

class OpportunityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, opportunity_id: str) -> Optional[Dict]:
        row = (
            self.db.query(Opportunity, Account, Product, SalesTeam)
            .outerjoin(Account, Opportunity.account == Account.account)
            .join(Product, Opportunity.product == Product.product)
            .join(SalesTeam, Opportunity.sales_agent == SalesTeam.sales_agent)
            .filter(Opportunity.opportunity_id == opportunity_id)
            .first()
        )
        if not row:
            return None
        opp, acc, prod, st = row
        return self._format_opportunity_dict(opp, acc, prod, st)

    def _format_opportunity_dict(self, opp: Opportunity, acc: Optional[Account], prod: Product, st: SalesTeam) -> dict:
        is_open = opp.deal_stage in ("Prospecting", "Engaging")
        pipeline_status = "Open" if is_open else "Closed"

        # Calculate opportunity age
        # For closed deals: close_date - engage_date
        # For open deals: snapshot_date (2017-12-31) - engage_date (if available), else 0
        from datetime import date as dt_date
        snapshot = dt_date(2017, 12, 31)

        if opp.close_date and opp.engage_date:
            age_days = (opp.close_date - opp.engage_date).days
        elif opp.engage_date:
            age_days = max(0, (snapshot - opp.engage_date).days)
        else:
            age_days = 0

        return {
            "opportunity_id": opp.opportunity_id,
            "sales_agent": opp.sales_agent,
            "manager": st.manager if st else None,
            "regional_office": st.regional_office if st else None,
            "product": opp.product,
            "product_series": prod.series if prod else None,
            "product_sales_price": float(prod.sales_price) if prod else None,
            "account": opp.account,
            "sector": acc.sector if acc else None,
            "deal_stage": opp.deal_stage,
            "engage_date": opp.engage_date,
            "close_date": opp.close_date,
            "close_value": float(opp.close_value) if opp.close_value is not None else None,
            "pipeline_status": pipeline_status,
            "opportunity_age_days": age_days,
            "account_revenue": float(acc.revenue) if acc else None,
            "account_employees": int(acc.employees) if acc else None,
        }

    def list_opportunities(
        self,
        search: Optional[str] = None,
        account: Optional[str] = None,
        product: Optional[str] = None,
        sales_agent: Optional[str] = None,
        manager: Optional[str] = None,
        deal_stage: Optional[str] = None,
        pipeline_status: Optional[str] = None,
        regional_office: Optional[str] = None,
        min_close_value: Optional[float] = None,
        max_close_value: Optional[float] = None,
        engage_date_from: Optional[date] = None,
        engage_date_to: Optional[date] = None,
        close_date_from: Optional[date] = None,
        close_date_to: Optional[date] = None,
        sort_by: str = "opportunity_id",
        sort_desc: bool = False,
        page: int = 1,
        limit: int = 20,
    ) -> Tuple[List[Dict], int]:
        query = (
            self.db.query(Opportunity, Account, Product, SalesTeam)
            .outerjoin(Account, Opportunity.account == Account.account)
            .join(Product, Opportunity.product == Product.product)
            .join(SalesTeam, Opportunity.sales_agent == SalesTeam.sales_agent)
        )

        if search:
            s = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Opportunity.opportunity_id.ilike(s),
                    Opportunity.account.ilike(s),
                    Opportunity.sales_agent.ilike(s),
                    Opportunity.product.ilike(s),
                    SalesTeam.manager.ilike(s),
                    SalesTeam.regional_office.ilike(s),
                )
            )

        if account:
            query = query.filter(Opportunity.account.ilike(account.strip()))

        if product:
            query = query.filter(Opportunity.product.ilike(product.strip()))

        if sales_agent:
            query = query.filter(Opportunity.sales_agent.ilike(sales_agent.strip()))

        if manager:
            query = query.filter(SalesTeam.manager.ilike(manager.strip()))

        if regional_office:
            query = query.filter(SalesTeam.regional_office.ilike(regional_office.strip()))

        if deal_stage:
            query = query.filter(Opportunity.deal_stage.ilike(deal_stage.strip()))

        if pipeline_status:
            ps = pipeline_status.strip().capitalize()
            if ps == "Open":
                query = query.filter(Opportunity.deal_stage.in_(["Prospecting", "Engaging"]))
            elif ps == "Closed":
                query = query.filter(Opportunity.deal_stage.in_(["Won", "Lost"]))

        if min_close_value is not None:
            query = query.filter(Opportunity.close_value >= min_close_value)

        if max_close_value is not None:
            query = query.filter(Opportunity.close_value <= max_close_value)

        if engage_date_from:
            query = query.filter(Opportunity.engage_date >= engage_date_from)

        if engage_date_to:
            query = query.filter(Opportunity.engage_date <= engage_date_to)

        if close_date_from:
            query = query.filter(Opportunity.close_date >= close_date_from)

        if close_date_to:
            query = query.filter(Opportunity.close_date <= close_date_to)

        total = query.count()

        # Deterministic sorting
        sort_map = {
            "opportunity_id": Opportunity.opportunity_id,
            "deal_stage": Opportunity.deal_stage,
            "engage_date": Opportunity.engage_date,
            "close_date": Opportunity.close_date,
            "close_value": Opportunity.close_value,
            "sales_agent": Opportunity.sales_agent,
            "product": Opportunity.product,
            "account": Opportunity.account,
        }
        sort_col = sort_map.get(sort_by.lower(), Opportunity.opportunity_id)
        order_clause = desc(sort_col) if sort_desc else asc(sort_col)
        query = query.order_by(order_clause)

        offset = (page - 1) * limit
        rows = query.offset(offset).limit(limit).all()

        items = [self._format_opportunity_dict(opp, acc, prod, st) for opp, acc, prod, st in rows]
        return items, total

    def get_pipeline_summary(self) -> dict:
        """
        Reconciles exact figures:
        Total = 8,800
        Won = 4,238
        Lost = 2,473
        Prospecting = 500
        Engaging = 1,589
        Open = 2,089
        Closed = 6,711
        Win Rate = 63.15%
        Won Revenue = 10,005,534.0
        Avg Deal Size ≈ 2,360.91
        Avg Sales Cycle ≈ 47.99
        """
        all_opps = (
            self.db.query(Opportunity, Product.sales_price)
            .join(Product, Opportunity.product == Product.product)
            .all()
        )

        total = len(all_opps)
        won_count = sum(1 for o, _ in all_opps if o.deal_stage == "Won")
        lost_count = sum(1 for o, _ in all_opps if o.deal_stage == "Lost")
        prospecting_count = sum(1 for o, _ in all_opps if o.deal_stage == "Prospecting")
        engaging_count = sum(1 for o, _ in all_opps if o.deal_stage == "Engaging")

        open_count = prospecting_count + engaging_count
        closed_count = won_count + lost_count

        won_revenue = sum(float(o.close_value or 0.0) for o, _ in all_opps if o.deal_stage == "Won")
        open_pipeline_val = sum(float(price or 0.0) for o, price in all_opps if o.deal_stage in ("Prospecting", "Engaging"))

        win_rate = round((won_count / closed_count * 100.0), 2) if closed_count > 0 else 0.0
        avg_deal_size = round((won_revenue / won_count), 2) if won_count > 0 else 0.0

        # Cycle calculation on closed deals with both dates
        cycle_days = [
            (o.close_date - o.engage_date).days
            for o, _ in all_opps
            if o.deal_stage in ("Won", "Lost") and o.close_date and o.engage_date
        ]
        avg_cycle = round((sum(cycle_days) / len(cycle_days)), 2) if cycle_days else 0.0

        return {
            "total_opportunities": total,
            "open_opportunities": open_count,
            "prospecting_opportunities": prospecting_count,
            "engaging_opportunities": engaging_count,
            "won_opportunities": won_count,
            "lost_opportunities": lost_count,
            "closed_opportunities": closed_count,
            "pipeline_value": round(open_pipeline_val, 2),
            "won_revenue": round(won_revenue, 2),
            "win_rate": win_rate,
            "average_deal_size": avg_deal_size,
            "average_sales_cycle_days": avg_cycle,
        }

    def get_stage_breakdown(self) -> List[Dict]:
        opps = (
            self.db.query(Opportunity, Product.sales_price)
            .join(Product, Opportunity.product == Product.product)
            .all()
        )
        total = len(opps)
        stage_map = {
            "Prospecting": {"count": 0, "value": 0.0},
            "Engaging": {"count": 0, "value": 0.0},
            "Won": {"count": 0, "value": 0.0},
            "Lost": {"count": 0, "value": 0.0},
        }
        for o, price in opps:
            stg = o.deal_stage
            if stg in stage_map:
                stage_map[stg]["count"] += 1
                if stg == "Won":
                    stage_map[stg]["value"] += float(o.close_value or 0.0)
                elif stg in ("Prospecting", "Engaging"):
                    stage_map[stg]["value"] += float(price or 0.0)

        res = []
        for stg, data in stage_map.items():
            pct = round((data["count"] / total * 100.0), 2) if total > 0 else 0.0
            res.append({
                "deal_stage": stg,
                "opportunity_count": data["count"],
                "percentage_of_total": pct,
                "total_value": round(data["value"], 2),
            })
        return res

    def get_dimension_breakdown(self, dimension: str) -> List[Dict]:
        rows = (
            self.db.query(Opportunity, Product, Account, SalesTeam)
            .join(Product, Opportunity.product == Product.product)
            .outerjoin(Account, Opportunity.account == Account.account)
            .join(SalesTeam, Opportunity.sales_agent == SalesTeam.sales_agent)
            .all()
        )

        dim_agg = {}
        for opp, prod, acc, st in rows:
            if dimension == "product":
                dim_val = prod.product
            elif dimension == "sector":
                dim_val = acc.sector if acc else "Unassigned"
            elif dimension == "regional_office":
                dim_val = st.regional_office
            elif dimension == "sales_agent":
                dim_val = st.sales_agent
            elif dimension == "sales_manager":
                dim_val = st.manager
            else:
                dim_val = "Unknown"

            if dim_val not in dim_agg:
                dim_agg[dim_val] = {
                    "total": 0, "open": 0, "won": 0, "lost": 0,
                    "won_rev": 0.0, "open_val": 0.0
                }

            dim_agg[dim_val]["total"] += 1
            if opp.deal_stage in ("Prospecting", "Engaging"):
                dim_agg[dim_val]["open"] += 1
                dim_agg[dim_val]["open_val"] += float(prod.sales_price)
            elif opp.deal_stage == "Won":
                dim_agg[dim_val]["won"] += 1
                dim_agg[dim_val]["won_rev"] += float(opp.close_value or 0.0)
            elif opp.deal_stage == "Lost":
                dim_agg[dim_val]["lost"] += 1

        result = []
        for val, data in dim_agg.items():
            closed = data["won"] + data["lost"]
            wr = round((data["won"] / closed * 100.0), 2) if closed > 0 else 0.0
            avg_deal = round((data["won_rev"] / data["won"]), 2) if data["won"] > 0 else 0.0

            result.append({
                "dimension_name": dimension,
                "dimension_value": val,
                "total_opportunities": data["total"],
                "open_opportunities": data["open"],
                "won_opportunities": data["won"],
                "lost_opportunities": data["lost"],
                "won_revenue": round(data["won_rev"], 2),
                "open_pipeline_value": round(data["open_val"], 2),
                "win_rate": wr,
                "average_deal_size": avg_deal,
            })

        result.sort(key=lambda x: x["won_revenue"], reverse=True)
        return result
