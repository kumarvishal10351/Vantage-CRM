import math
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from backend.app.repositories.opportunity_repository import OpportunityRepository
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.schemas.opportunity import OpportunityRead, OpportunityDetail
from backend.app.schemas.common import PaginatedResponse, PaginationMeta
from backend.app.services.account_service import classify_account_tier
from backend.app.services.product_service import classify_product_tier

def classify_engagement_age_band(stage: str, age_days: int) -> str:
    if stage == "Prospecting" or age_days <= 0:
        return "Unengaged (Prospecting)"
    elif age_days <= 90:
        return "Recent (<= 90 days)"
    elif age_days <= 180:
        return "Aging (91-180 days)"
    else:
        return "Stalled / Critical (> 180 days)"

class OpportunityService:
    def __init__(self, db: Session):
        self.repo = OpportunityRepository(db)

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
    ) -> PaginatedResponse[OpportunityRead]:
        items, total = self.repo.list_opportunities(
            search=search,
            account=account,
            product=product,
            sales_agent=sales_agent,
            manager=manager,
            deal_stage=deal_stage,
            pipeline_status=pipeline_status,
            regional_office=regional_office,
            min_close_value=min_close_value,
            max_close_value=max_close_value,
            engage_date_from=engage_date_from,
            engage_date_to=engage_date_to,
            close_date_from=close_date_from,
            close_date_to=close_date_to,
            sort_by=sort_by,
            sort_desc=sort_desc,
            page=page,
            limit=limit,
        )

        reads = []
        for d in items:
            reads.append(OpportunityRead(**d))

        total_pages = math.ceil(total / limit) if limit > 0 else 1

        return PaginatedResponse(
            items=reads,
            pagination=PaginationMeta(
                page=page,
                limit=limit,
                total_items=total,
                total_pages=total_pages,
            ),
        )

    def get_opportunity_detail(self, opportunity_id: str) -> OpportunityDetail:
        opp_dict = self.repo.get_by_id(opportunity_id)
        if not opp_dict:
            raise EntityNotFoundException("Opportunity", opportunity_id)

        acc_tier = classify_account_tier(
            opp_dict.get("account_revenue"),
            opp_dict.get("account_employees"),
            opp_dict.get("account")
        )
        prod_price = opp_dict.get("product_sales_price") or 0.0
        prod_tier = classify_product_tier(prod_price)
        age_band = classify_engagement_age_band(opp_dict["deal_stage"], opp_dict["opportunity_age_days"])

        return OpportunityDetail(
            **opp_dict,
            account_tier=acc_tier,
            product_value_tier=prod_tier,
            aging_band=age_band,
        )
