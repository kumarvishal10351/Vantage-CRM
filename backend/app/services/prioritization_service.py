import math
from datetime import date
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.app.models.opportunity import Opportunity
from backend.app.models.account import Account
from backend.app.models.product import Product
from backend.app.models.sales_team import SalesTeam
from backend.app.schemas.prioritization import (
    PrioritizedOpportunityItem, PrioritizationSummaryResponse,
    TierWorkloadItem, AgentWorkloadItem, ProductWorkloadItem,
    GOVERNANCE_STATEMENT
)
from backend.app.schemas.common import PaginatedResponse, PaginationMeta

SNAPSHOT_DATE = date(2017, 12, 31)

def classify_product_tier(price: float) -> str:
    if price is None or price <= 0:
        return "Low Value"
    elif price >= 4000:
        return "High Value"
    elif price >= 1000:
        return "Medium Value"
    else:
        return "Low Value"

def classify_account_tier(account_name: Optional[str], revenue: Optional[float], employees: Optional[int]) -> str:
    if not account_name or (revenue is None and employees is None):
        return "Unassigned Account"
    rev = float(revenue) if revenue is not None else 0.0
    emp = int(employees) if employees is not None else 0
    if rev >= 2500 or emp >= 5000:
        return "Enterprise"
    elif rev >= 500 or emp >= 1000:
        return "Mid-Market"
    else:
        return "Commercial / Small"

def classify_engagement_age_band(stage: str, age_days: int) -> str:
    if stage == "Prospecting" or age_days <= 0:
        return "Unengaged (Prospecting)"
    elif age_days <= 90:
        return "Recent (<= 90 days)"
    elif age_days <= 180:
        return "Aging (91-180 days)"
    else:
        return "Stalled / Critical (> 180 days)"

def calculate_priority_score_and_tier(stage: str, prod_tier: str, acc_tier: str, age_band: str) -> Tuple[int, str]:
    # Stage pts (Max 30)
    stage_pts = 30 if stage == "Engaging" else 10

    # Product pts (Max 30)
    prod_map = {"High Value": 30, "Medium Value": 20, "Low Value": 10}
    prod_pts = prod_map.get(prod_tier, 10)

    # Account pts (Max 25)
    acc_map = {
        "Enterprise": 25,
        "Mid-Market": 15,
        "Commercial / Small": 10,
        "Unassigned Account": 5,
    }
    acc_pts = acc_map.get(acc_tier, 5)

    # Age pts (Max 15)
    age_map = {
        "Recent (<= 90 days)": 15,
        "Aging (91-180 days)": 10,
        "Stalled / Critical (> 180 days)": 5,
        "Unengaged (Prospecting)": 5,
    }
    age_pts = age_map.get(age_band, 5)

    total_score = stage_pts + prod_pts + acc_pts + age_pts

    if total_score >= 75:
        tier = "Tier 1 — High Priority"
    elif total_score >= 55:
        tier = "Tier 2 — Medium Priority"
    else:
        tier = "Tier 3 — Lower Priority"

    return total_score, tier

class PrioritizationService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_scored_open_opportunities(self) -> List[PrioritizedOpportunityItem]:
        """Loads and deterministically scores all 2,089 open opportunities."""
        rows = (
            self.db.query(Opportunity, Account, Product, SalesTeam)
            .outerjoin(Account, Opportunity.account == Account.account)
            .join(Product, Opportunity.product == Product.product)
            .join(SalesTeam, Opportunity.sales_agent == SalesTeam.sales_agent)
            .filter(Opportunity.deal_stage.in_(["Prospecting", "Engaging"]))
            .order_by(Opportunity.opportunity_id)
            .all()
        )

        scored_items = []
        for opp, acc, prod, st in rows:
            # 1. Age
            if opp.deal_stage == "Engaging" and opp.engage_date:
                age_days = max(0, (SNAPSHOT_DATE - opp.engage_date).days)
            else:
                age_days = 0

            # 2. Product Tier
            prod_price = float(prod.sales_price)
            prod_tier = classify_product_tier(prod_price)

            # 3. Account Tier
            acc_name = opp.account
            acc_rev = float(acc.revenue) if acc and acc.revenue is not None else None
            acc_emp = int(acc.employees) if acc and acc.employees is not None else None
            acc_tier = classify_account_tier(acc_name, acc_rev, acc_emp)

            # 4. Age band
            age_band = classify_engagement_age_band(opp.deal_stage, age_days)

            # 5. Composite Score & Tier
            score, tier = calculate_priority_score_and_tier(opp.deal_stage, prod_tier, acc_tier, age_band)

            scored_items.append(
                PrioritizedOpportunityItem(
                    opportunity_id=opp.opportunity_id,
                    sales_agent=opp.sales_agent,
                    manager=st.manager,
                    regional_office=st.regional_office,
                    product=opp.product,
                    product_series=prod.series,
                    product_sales_price=prod_price,
                    product_value_tier=prod_tier,
                    account=opp.account,
                    sector=acc.sector if acc else None,
                    account_revenue=acc_rev,
                    account_employees=acc_emp,
                    account_tier=acc_tier,
                    deal_stage=opp.deal_stage,
                    engage_date=opp.engage_date,
                    engagement_age_days=age_days,
                    engagement_age_band=age_band,
                    crm_priority_score=score,
                    priority_tier=tier,
                )
            )

        return scored_items

    def list_prioritized_opportunities(
        self,
        tier: Optional[str] = None,
        sales_agent: Optional[str] = None,
        product: Optional[str] = None,
        account: Optional[str] = None,
        sector: Optional[str] = None,
        deal_stage: Optional[str] = None,
        sort_by: str = "crm_priority_score",
        sort_desc: bool = True,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[PrioritizedOpportunityItem]:
        all_items = self.get_all_scored_open_opportunities()

        filtered = all_items
        if tier:
            t_lower = tier.lower().strip()
            filtered = [
                i for i in filtered
                if t_lower in i.priority_tier.lower() or t_lower in i.priority_tier.split("—")[0].strip().lower()
            ]

        if sales_agent:
            filtered = [i for i in filtered if sales_agent.lower().strip() in i.sales_agent.lower()]

        if product:
            filtered = [i for i in filtered if product.lower().strip() in i.product.lower()]

        if account:
            filtered = [i for i in filtered if i.account and account.lower().strip() in i.account.lower()]

        if sector:
            filtered = [i for i in filtered if i.sector and sector.lower().strip() in i.sector.lower()]

        if deal_stage:
            filtered = [i for i in filtered if deal_stage.lower().strip() == i.deal_stage.lower()]

        # Sort
        def sort_fn(item: PrioritizedOpportunityItem):
            val = getattr(item, sort_by.lower(), None)
            return val if val is not None else 0

        try:
            filtered.sort(key=sort_fn, reverse=sort_desc)
        except Exception:
            filtered.sort(key=lambda x: x.crm_priority_score, reverse=True)

        total = len(filtered)
        total_pages = math.ceil(total / limit) if limit > 0 else 1
        offset = (page - 1) * limit
        paged_items = filtered[offset : offset + limit]

        return PaginatedResponse(
            items=paged_items,
            pagination=PaginationMeta(
                page=page,
                limit=limit,
                total_items=total,
                total_pages=total_pages,
            ),
        )

    def get_summary(self) -> PrioritizationSummaryResponse:
        scored = self.get_all_scored_open_opportunities()
        total_open = len(scored)

        tier_counts = {
            "Tier 1 — High Priority": 0,
            "Tier 2 — Medium Priority": 0,
            "Tier 3 — Lower Priority": 0,
        }
        for s in scored:
            if s.priority_tier in tier_counts:
                tier_counts[s.priority_tier] += 1

        dist_list = [
            TierWorkloadItem(
                tier="Tier 1 — High Priority",
                count=tier_counts["Tier 1 — High Priority"],
                percentage=round(tier_counts["Tier 1 — High Priority"] / total_open * 100.0, 2),
                description="Scores >= 75: Executive & Manager Attention required.",
            ),
            TierWorkloadItem(
                tier="Tier 2 — Medium Priority",
                count=tier_counts["Tier 2 — Medium Priority"],
                percentage=round(tier_counts["Tier 2 — Medium Priority"] / total_open * 100.0, 2),
                description="Scores 55-74: Standard Representative Active Follow-up.",
            ),
            TierWorkloadItem(
                tier="Tier 3 — Lower Priority",
                count=tier_counts["Tier 3 — Lower Priority"],
                percentage=round(tier_counts["Tier 3 — Lower Priority"] / total_open * 100.0, 2),
                description="Scores < 55: Routine Qualification & Pipeline Maintenance.",
            ),
        ]

        # Agent Workloads
        agent_map = {}
        for s in scored:
            a = s.sales_agent
            if a not in agent_map:
                agent_map[a] = {
                    "manager": s.manager, "regional_office": s.regional_office,
                    "total": 0, "t1": 0, "t2": 0, "t3": 0
                }
            agent_map[a]["total"] += 1
            if "Tier 1" in s.priority_tier:
                agent_map[a]["t1"] += 1
            elif "Tier 2" in s.priority_tier:
                agent_map[a]["t2"] += 1
            elif "Tier 3" in s.priority_tier:
                agent_map[a]["t3"] += 1

        agent_items = [
            AgentWorkloadItem(
                sales_agent=a,
                manager=d["manager"],
                regional_office=d["regional_office"],
                total_open=d["total"],
                tier_1_count=d["t1"],
                tier_2_count=d["t2"],
                tier_3_count=d["t3"],
            )
            for a, d in agent_map.items()
        ]
        agent_items.sort(key=lambda x: x.tier_1_count, reverse=True)

        # Product Workloads
        prod_map = {}
        for s in scored:
            p = s.product
            if p not in prod_map:
                prod_map[p] = {
                    "series": s.product_series, "price": s.product_sales_price,
                    "total": 0, "t1": 0, "t2": 0, "t3": 0
                }
            prod_map[p]["total"] += 1
            if "Tier 1" in s.priority_tier:
                prod_map[p]["t1"] += 1
            elif "Tier 2" in s.priority_tier:
                prod_map[p]["t2"] += 1
            elif "Tier 3" in s.priority_tier:
                prod_map[p]["t3"] += 1

        prod_items = [
            ProductWorkloadItem(
                product=p,
                series=d["series"],
                sales_price=d["price"],
                total_open=d["total"],
                tier_1_count=d["t1"],
                tier_2_count=d["t2"],
                tier_3_count=d["t3"],
            )
            for p, d in prod_map.items()
        ]
        prod_items.sort(key=lambda x: x.tier_1_count, reverse=True)

        return PrioritizationSummaryResponse(
            governance_notice=GOVERNANCE_STATEMENT,
            total_open_opportunities=total_open,
            distribution=dist_list,
            top_agents_by_tier1=agent_items,
            products_workload=prod_items,
        )
