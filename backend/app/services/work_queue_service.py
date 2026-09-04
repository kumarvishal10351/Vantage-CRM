import math
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.schemas.work_queue import WorkQueueOpportunityItem, WorkQueueSummaryItem
from backend.app.schemas.common import PaginatedResponse, PaginationMeta
from backend.app.services.prioritization_service import PrioritizationService

class WorkQueueService:
    def __init__(self, db: Session):
        self.db = db
        self.prio_service = PrioritizationService(db)

    def get_tier1_review_queue(
        self,
        sales_agent: Optional[str] = None,
        manager: Optional[str] = None,
        product: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[WorkQueueOpportunityItem]:
        all_scored = self.prio_service.get_all_scored_open_opportunities()
        tier1_deals = [s for s in all_scored if "Tier 1" in s.priority_tier]

        if sales_agent:
            tier1_deals = [d for d in tier1_deals if sales_agent.lower().strip() in d.sales_agent.lower()]
        if manager:
            tier1_deals = [d for d in tier1_deals if d.manager and manager.lower().strip() in d.manager.lower()]
        if product:
            tier1_deals = [d for d in tier1_deals if product.lower().strip() in d.product.lower()]

        items = [
            WorkQueueOpportunityItem(
                opportunity_id=d.opportunity_id,
                sales_agent=d.sales_agent,
                manager=d.manager or "Unassigned",
                regional_office=d.regional_office or "Unassigned",
                product=d.product,
                product_sales_price=d.product_sales_price,
                account=d.account,
                sector=d.sector,
                deal_stage=d.deal_stage,
                engage_date=d.engage_date,
                engagement_age_days=d.engagement_age_days,
                crm_priority_score=d.crm_priority_score,
                priority_tier=d.priority_tier,
                action_needed="Schedule executive sponsor check-in and sales management milestone review.",
            )
            for d in tier1_deals
        ]

        total = len(items)
        total_pages = math.ceil(total / limit) if limit > 0 else 1
        offset = (page - 1) * limit
        paged = items[offset : offset + limit]

        return PaginatedResponse(
            items=paged,
            pagination=PaginationMeta(
                page=page, limit=limit, total_items=total, total_pages=total_pages
            ),
        )

    def get_stalled_deals_queue(
        self,
        sales_agent: Optional[str] = None,
        manager: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[WorkQueueOpportunityItem]:
        all_scored = self.prio_service.get_all_scored_open_opportunities()
        stalled_deals = [s for s in all_scored if s.deal_stage == "Engaging" and s.engagement_age_days > 180]

        if sales_agent:
            stalled_deals = [d for d in stalled_deals if sales_agent.lower().strip() in d.sales_agent.lower()]
        if manager:
            stalled_deals = [d for d in stalled_deals if d.manager and manager.lower().strip() in d.manager.lower()]

        items = [
            WorkQueueOpportunityItem(
                opportunity_id=d.opportunity_id,
                sales_agent=d.sales_agent,
                manager=d.manager or "Unassigned",
                regional_office=d.regional_office or "Unassigned",
                product=d.product,
                product_sales_price=d.product_sales_price,
                account=d.account,
                sector=d.sector,
                deal_stage=d.deal_stage,
                engage_date=d.engage_date,
                engagement_age_days=d.engagement_age_days,
                crm_priority_score=d.crm_priority_score,
                priority_tier=d.priority_tier,
                action_needed="Cycle exceeds 180 days (standard avg is 48 days). Validate viability or mark Lost.",
            )
            for d in stalled_deals
        ]

        total = len(items)
        total_pages = math.ceil(total / limit) if limit > 0 else 1
        offset = (page - 1) * limit
        paged = items[offset : offset + limit]

        return PaginatedResponse(
            items=paged,
            pagination=PaginationMeta(
                page=page, limit=limit, total_items=total, total_pages=total_pages
            ),
        )

    def get_unassigned_accounts_queue(
        self,
        sales_agent: Optional[str] = None,
        manager: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[WorkQueueOpportunityItem]:
        all_scored = self.prio_service.get_all_scored_open_opportunities()
        unassigned_deals = [s for s in all_scored if not s.account]

        if sales_agent:
            unassigned_deals = [d for d in unassigned_deals if sales_agent.lower().strip() in d.sales_agent.lower()]
        if manager:
            unassigned_deals = [d for d in unassigned_deals if d.manager and manager.lower().strip() in d.manager.lower()]

        items = [
            WorkQueueOpportunityItem(
                opportunity_id=d.opportunity_id,
                sales_agent=d.sales_agent,
                manager=d.manager or "Unassigned",
                regional_office=d.regional_office or "Unassigned",
                product=d.product,
                product_sales_price=d.product_sales_price,
                account=None,
                sector=None,
                deal_stage=d.deal_stage,
                engage_date=d.engage_date,
                engagement_age_days=d.engagement_age_days,
                crm_priority_score=d.crm_priority_score,
                priority_tier=d.priority_tier,
                action_needed="Link opportunity to strategic corporate account or qualify enterprise entity.",
            )
            for d in unassigned_deals
        ]

        total = len(items)
        total_pages = math.ceil(total / limit) if limit > 0 else 1
        offset = (page - 1) * limit
        paged = items[offset : offset + limit]

        return PaginatedResponse(
            items=paged,
            pagination=PaginationMeta(
                page=page, limit=limit, total_items=total, total_pages=total_pages
            ),
        )

    def get_queues_summary(self) -> List[WorkQueueSummaryItem]:
        all_scored = self.prio_service.get_all_scored_open_opportunities()

        t1_deals = [s for s in all_scored if "Tier 1" in s.priority_tier]
        stalled_deals = [s for s in all_scored if s.deal_stage == "Engaging" and s.engagement_age_days > 180]
        unassigned = [s for s in all_scored if not s.account]

        return [
            WorkQueueSummaryItem(
                queue_name="Tier 1 High-Priority Review Queue",
                description="High-score opportunities requiring executive alignment and sales manager coaching.",
                item_count=len(t1_deals),
                total_value=round(sum(d.product_sales_price for d in t1_deals), 2),
                recommended_owner_role="Sales Manager / Executive",
            ),
            WorkQueueSummaryItem(
                queue_name="Stalled Opportunities Queue",
                description="Engaging deals active for > 180 days exceeding standard velocity.",
                item_count=len(stalled_deals),
                total_value=round(sum(d.product_sales_price for d in stalled_deals), 2),
                recommended_owner_role="Sales Representative / Manager",
            ),
            WorkQueueSummaryItem(
                queue_name="Unassigned Accounts Queue",
                description="Active pipeline deals missing account linkages needing firmographic enrichment.",
                item_count=len(unassigned),
                total_value=round(sum(d.product_sales_price for d in unassigned), 2),
                recommended_owner_role="Sales Operations / Representative",
            ),
        ]
