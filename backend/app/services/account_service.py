import math
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.repositories.account_repository import AccountRepository
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.schemas.account import (
    AccountRead, AccountDetail, AccountStats, AccountSummaryResponse
)
from backend.app.schemas.common import PaginatedResponse, PaginationMeta

def classify_account_tier(revenue: Optional[float], employees: Optional[int], account_name: Optional[str] = None) -> str:
    if not account_name and (revenue is None and employees is None):
        return "Unassigned Account"
    rev = float(revenue) if revenue is not None else 0.0
    emp = int(employees) if employees is not None else 0
    if rev >= 2500 or emp >= 5000:
        return "Enterprise"
    elif rev >= 500 or emp >= 1000:
        return "Mid-Market"
    else:
        return "Commercial / Small"

class AccountService:
    def __init__(self, db: Session):
        self.repo = AccountRepository(db)

    def list_accounts(
        self,
        search: Optional[str] = None,
        sector: Optional[str] = None,
        office_location: Optional[str] = None,
        min_revenue: Optional[float] = None,
        max_revenue: Optional[float] = None,
        tier: Optional[str] = None,
        has_subsidiary: Optional[bool] = None,
        sort_by: str = "account",
        sort_desc: bool = False,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[AccountRead]:
        items, total = self.repo.list_accounts(
            search=search,
            sector=sector,
            office_location=office_location,
            min_revenue=min_revenue,
            max_revenue=max_revenue,
            has_subsidiary=has_subsidiary,
            sort_by=sort_by,
            sort_desc=sort_desc,
            page=page,
            limit=limit,
        )

        account_reads = []
        for a in items:
            t = classify_account_tier(float(a.revenue), int(a.employees), a.account)
            account_reads.append(
                AccountRead(
                    account=a.account,
                    sector=a.sector,
                    year_established=a.year_established,
                    revenue=float(a.revenue),
                    employees=int(a.employees),
                    office_location=a.office_location,
                    subsidiary_of=a.subsidiary_of,
                    account_tier=t,
                )
            )

        # In-memory filter by tier if requested
        if tier:
            account_reads = [a for a in account_reads if a.account_tier.lower() == tier.lower().strip()]
            total = len(account_reads)

        total_pages = math.ceil(total / limit) if limit > 0 else 1

        return PaginatedResponse(
            items=account_reads,
            pagination=PaginationMeta(
                page=page,
                limit=limit,
                total_items=total,
                total_pages=total_pages,
            ),
        )

    def get_account_detail(self, account_id: str) -> AccountDetail:
        acc = self.repo.get_by_id(account_id)
        if not acc:
            raise EntityNotFoundException("Account", account_id)

        stats_dict = self.repo.get_account_opportunity_stats(account_id)
        subsidiaries = self.repo.get_subsidiaries(account_id)
        tier = classify_account_tier(float(acc.revenue), int(acc.employees), acc.account)

        return AccountDetail(
            account=acc.account,
            sector=acc.sector,
            year_established=acc.year_established,
            revenue=float(acc.revenue),
            employees=int(acc.employees),
            office_location=acc.office_location,
            subsidiary_of=acc.subsidiary_of,
            account_tier=tier,
            stats=AccountStats(**stats_dict),
            subsidiaries_list=subsidiaries,
        )

    def get_account_summary(self) -> AccountSummaryResponse:
        summary_data = self.repo.get_overall_summary()
        accounts, _ = self.repo.list_accounts(limit=1000)

        tiers = {"Enterprise": 0, "Mid-Market": 0, "Commercial / Small": 0}
        for a in accounts:
            t = classify_account_tier(float(a.revenue), int(a.employees), a.account)
            tiers[t] = tiers.get(t, 0) + 1

        return AccountSummaryResponse(
            total_accounts=summary_data["total_accounts"],
            total_corporate_revenue=summary_data["total_corporate_revenue"],
            total_employees=summary_data["total_employees"],
            sectors_count=summary_data["sectors_count"],
            tier_distribution=tiers,
            top_sectors_by_revenue=summary_data["top_sectors_by_revenue"],
        )
