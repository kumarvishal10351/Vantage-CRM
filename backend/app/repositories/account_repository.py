from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from backend.app.models.account import Account
from backend.app.models.opportunity import Opportunity
from backend.app.models.product import Product

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, account_id: str) -> Optional[Account]:
        return self.db.query(Account).filter(Account.account == account_id).first()

    def get_subsidiaries(self, account_id: str) -> List[str]:
        rows = self.db.query(Account.account).filter(Account.subsidiary_of == account_id).all()
        return [r[0] for r in rows]

    def list_accounts(
        self,
        search: Optional[str] = None,
        sector: Optional[str] = None,
        office_location: Optional[str] = None,
        min_revenue: Optional[float] = None,
        max_revenue: Optional[float] = None,
        has_subsidiary: Optional[bool] = None,
        sort_by: str = "account",
        sort_desc: bool = False,
        page: int = 1,
        limit: int = 20,
    ) -> Tuple[List[Account], int]:
        query = self.db.query(Account)

        if search:
            s = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Account.account.ilike(s),
                    Account.sector.ilike(s),
                    Account.office_location.ilike(s),
                    Account.subsidiary_of.ilike(s),
                )
            )

        if sector:
            query = query.filter(Account.sector.ilike(sector.strip()))

        if office_location:
            query = query.filter(Account.office_location.ilike(office_location.strip()))

        if min_revenue is not None:
            query = query.filter(Account.revenue >= min_revenue)

        if max_revenue is not None:
            query = query.filter(Account.revenue <= max_revenue)

        if has_subsidiary is True:
            subquery = self.db.query(Account.subsidiary_of).filter(Account.subsidiary_of.isnot(None)).distinct()
            query = query.filter(Account.account.in_(subquery))
        elif has_subsidiary is False:
            subquery = self.db.query(Account.subsidiary_of).filter(Account.subsidiary_of.isnot(None)).distinct()
            query = query.filter(~Account.account.in_(subquery))

        total = query.count()

        # Deterministic sorting
        sort_column_map = {
            "account": Account.account,
            "revenue": Account.revenue,
            "employees": Account.employees,
            "year_established": Account.year_established,
            "sector": Account.sector,
            "office_location": Account.office_location,
        }
        sort_col = sort_column_map.get(sort_by.lower(), Account.account)
        order_clause = desc(sort_col) if sort_desc else asc(sort_col)
        query = query.order_by(order_clause)

        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()

        return items, total

    def get_account_opportunity_stats(self, account_id: str) -> dict:
        """Computes opportunity statistics for a specific account."""
        opps = (
            self.db.query(Opportunity, Product.sales_price)
            .join(Product, Opportunity.product == Product.product)
            .filter(Opportunity.account == account_id)
            .all()
        )

        total_opps = len(opps)
        won_opps = sum(1 for o, _ in opps if o.deal_stage == "Won")
        lost_opps = sum(1 for o, _ in opps if o.deal_stage == "Lost")
        open_opps = sum(1 for o, _ in opps if o.deal_stage in ("Prospecting", "Engaging"))
        won_rev = sum(float(o.close_value or 0.0) for o, _ in opps if o.deal_stage == "Won")
        open_val = sum(float(price or 0.0) for o, price in opps if o.deal_stage in ("Prospecting", "Engaging"))

        closed_total = won_opps + lost_opps
        win_rate = round((won_opps / closed_total * 100.0), 2) if closed_total > 0 else 0.0

        return {
            "total_opportunities": total_opps,
            "open_opportunities": open_opps,
            "won_opportunities": won_opps,
            "lost_opportunities": lost_opps,
            "won_revenue": round(won_rev, 2),
            "open_pipeline_value": round(open_val, 2),
            "win_rate": win_rate,
        }

    def get_overall_summary(self) -> dict:
        """Summary aggregates across all 85 accounts."""
        accounts = self.db.query(Account).all()
        total_accounts = len(accounts)
        total_revenue = sum(float(a.revenue) for a in accounts)
        total_employees = sum(int(a.employees) for a in accounts)
        sectors = set(a.sector for a in accounts)

        # Sectors revenue
        sector_rev = {}
        for a in accounts:
            sector_rev[a.sector] = sector_rev.get(a.sector, 0.0) + float(a.revenue)

        top_sectors = [
            {"sector": s, "total_revenue": round(rev, 2)}
            for s, rev in sorted(sector_rev.items(), key=lambda x: x[1], reverse=True)
        ]

        return {
            "total_accounts": total_accounts,
            "total_corporate_revenue": round(total_revenue, 2),
            "total_employees": total_employees,
            "sectors_count": len(sectors),
            "top_sectors_by_revenue": top_sectors,
        }
