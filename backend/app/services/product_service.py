from typing import Optional, List
from sqlalchemy.orm import Session
from backend.app.repositories.product_repository import ProductRepository
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.schemas.product import ProductPerformance, ProductDetail

def classify_product_tier(price: float) -> str:
    if price >= 4000:
        return "High Value"
    elif price >= 1000:
        return "Medium Value"
    else:
        return "Low Value"

class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def list_products(
        self,
        search: Optional[str] = None,
        series: Optional[str] = None,
        tier: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: str = "product",
        sort_desc: bool = False,
    ) -> List[ProductPerformance]:
        products = self.repo.list_products(
            search=search,
            series=series,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            sort_desc=sort_desc,
        )

        res = []
        for p in products:
            val_tier = classify_product_tier(float(p.sales_price))
            metrics = self.repo.get_product_metrics(p.product)
            item = ProductPerformance(
                product=p.product,
                series=p.series,
                sales_price=float(p.sales_price),
                product_value_tier=val_tier,
                total_opportunities=metrics.get("total_opportunities", 0),
                open_opportunities=metrics.get("open_opportunities", 0),
                won_opportunities=metrics.get("won_opportunities", 0),
                lost_opportunities=metrics.get("lost_opportunities", 0),
                open_pipeline_value=metrics.get("open_pipeline_value", 0.0),
                won_revenue=metrics.get("won_revenue", 0.0),
                win_rate=metrics.get("win_rate", 0.0),
                average_deal_size=metrics.get("average_deal_size", 0.0),
            )
            if tier and val_tier.lower() != tier.lower().strip():
                continue
            res.append(item)

        return res

    def get_product_detail(self, product_name: str) -> ProductDetail:
        prod = self.repo.get_by_id(product_name)
        if not prod:
            raise EntityNotFoundException("Product", product_name)

        metrics = self.repo.get_product_metrics(product_name)
        val_tier = classify_product_tier(float(prod.sales_price))

        return ProductDetail(
            product=prod.product,
            series=prod.series,
            sales_price=float(prod.sales_price),
            product_value_tier=val_tier,
            total_opportunities=metrics.get("total_opportunities", 0),
            open_opportunities=metrics.get("open_opportunities", 0),
            won_opportunities=metrics.get("won_opportunities", 0),
            lost_opportunities=metrics.get("lost_opportunities", 0),
            open_pipeline_value=metrics.get("open_pipeline_value", 0.0),
            won_revenue=metrics.get("won_revenue", 0.0),
            win_rate=metrics.get("win_rate", 0.0),
            average_deal_size=metrics.get("average_deal_size", 0.0),
            performance_by_sector=metrics.get("performance_by_sector", []),
            performance_by_agent=metrics.get("performance_by_agent", []),
        )
