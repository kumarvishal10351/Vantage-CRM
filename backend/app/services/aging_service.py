from datetime import date
from sqlalchemy.orm import Session
from backend.app.models.opportunity import Opportunity
from backend.app.models.product import Product
from backend.app.models.account import Account
from backend.app.models.sales_team import SalesTeam
from backend.app.schemas.aging import (
    AgingSummaryResponse, AgingBandItem, DimensionAgingItem
)
from backend.app.services.opportunity_service import classify_engagement_age_band

SNAPSHOT_DATE = date(2017, 12, 31)

class AgingService:
    def __init__(self, db: Session):
        self.db = db

    def get_aging_summary(self) -> AgingSummaryResponse:
        # All opportunities
        opps = (
            self.db.query(Opportunity, Product, Account, SalesTeam)
            .join(Product, Opportunity.product == Product.product)
            .outerjoin(Account, Opportunity.account == Account.account)
            .join(SalesTeam, Opportunity.sales_agent == SalesTeam.sales_agent)
            .all()
        )

        open_deals = [row for row in opps if row[0].deal_stage in ("Prospecting", "Engaging")]
        closed_deals = [row for row in opps if row[0].deal_stage in ("Won", "Lost")]

        # Closed average cycle
        closed_cycles = [
            (r[0].close_date - r[0].engage_date).days
            for r in closed_deals
            if r[0].close_date and r[0].engage_date
        ]
        avg_closed_cycle = round(sum(closed_cycles) / len(closed_cycles), 2) if closed_cycles else 0.0

        # Open deal age
        open_ages = []
        band_counts = {
            "Recent (<= 90 days)": {"count": 0, "val": 0.0},
            "Aging (91-180 days)": {"count": 0, "val": 0.0},
            "Stalled / Critical (> 180 days)": {"count": 0, "val": 0.0},
            "Unengaged (Prospecting)": {"count": 0, "val": 0.0},
        }

        for opp, prod, acc, st in open_deals:
            if opp.deal_stage == "Engaging" and opp.engage_date:
                age = max(0, (SNAPSHOT_DATE - opp.engage_date).days)
            else:
                age = 0
            open_ages.append(age)
            band = classify_engagement_age_band(opp.deal_stage, age)
            band_counts[band]["count"] += 1
            band_counts[band]["val"] += float(prod.sales_price)

        total_open = len(open_deals)
        avg_open_age = round(sum(open_ages) / total_open, 2) if total_open > 0 else 0.0

        band_distribution = [
            AgingBandItem(
                aging_band=k,
                count=v["count"],
                percentage=round(v["count"] / total_open * 100.0, 2) if total_open > 0 else 0.0,
                total_pipeline_value=round(v["val"], 2),
            )
            for k, v in band_counts.items()
        ]

        # Aging by stage
        stages_data = []
        for stage in ["Prospecting", "Engaging"]:
            stage_opps = [o for o, p, a, s in open_deals if o.deal_stage == stage]
            if stage == "Engaging":
                s_ages = [(SNAPSHOT_DATE - o.engage_date).days for o in stage_opps if o.engage_date]
                s_avg = round(sum(s_ages) / len(s_ages), 2) if s_ages else 0.0
            else:
                s_avg = 0.0
            stages_data.append({
                "deal_stage": stage,
                "count": len(stage_opps),
                "average_age_days": s_avg,
            })

        # Helper for dimension breakdown
        def get_dim_aging(dim_extractor):
            groups = {}
            for opp, prod, acc, st in open_deals:
                dim_val = dim_extractor(opp, prod, acc, st)
                if dim_val not in groups:
                    groups[dim_val] = {"ages": [], "stalled": 0}
                if opp.deal_stage == "Engaging" and opp.engage_date:
                    age = max(0, (SNAPSHOT_DATE - opp.engage_date).days)
                else:
                    age = 0
                groups[dim_val]["ages"].append(age)
                if age > 180:
                    groups[dim_val]["stalled"] += 1

            result = []
            for d_name, d_info in groups.items():
                tot = len(d_info["ages"])
                avg_a = round(sum(d_info["ages"]) / tot, 2) if tot > 0 else 0.0
                result.append(
                    DimensionAgingItem(
                        dimension_value=d_name,
                        total_open_deals=tot,
                        average_age_days=avg_a,
                        stalled_deals_count=d_info["stalled"],
                    )
                )
            result.sort(key=lambda x: x.average_age_days, reverse=True)
            return result

        top_agents = get_dim_aging(lambda o, p, a, st: st.sales_agent)
        by_product = get_dim_aging(lambda o, p, a, st: p.product)
        by_sector = get_dim_aging(lambda o, p, a, st: a.sector if a else "Unassigned")

        return AgingSummaryResponse(
            reference_date=SNAPSHOT_DATE.strftime("%Y-%m-%d"),
            total_open_opportunities=total_open,
            average_open_age_days=avg_open_age,
            average_closed_cycle_days=avg_closed_cycle,
            band_distribution=band_distribution,
            aging_by_stage=stages_data,
            top_aging_agents=top_agents,
            aging_by_product=by_product,
            aging_by_sector=by_sector,
        )
