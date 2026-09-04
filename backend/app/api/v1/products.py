from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.product import ProductPerformance, ProductDetail
from backend.app.schemas.common import ApiResponse
from backend.app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=ApiResponse[List[ProductPerformance]], summary="List product catalog with CRM performance metrics and tiers")
def list_products(
    search: Optional[str] = Query(None, description="Search product name or series"),
    series: Optional[str] = Query(None, description="Filter by product series (GTX, GTK, MG)"),
    tier: Optional[str] = Query(None, description="Filter by catalog value tier: High Value, Medium Value, Low Value"),
    min_price: Optional[float] = Query(None, description="Minimum catalog sales price"),
    max_price: Optional[float] = Query(None, description="Maximum catalog sales price"),
    sort_by: str = Query("sales_price", description="Sort field: sales_price, won_revenue, win_rate, total_opportunities"),
    sort_desc: bool = Query(True, description="Sort descending"),
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    products = service.list_products(
        search=search,
        series=series,
        tier=tier,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )
    return ApiResponse(data=products)

@router.get("/{product_name}", response_model=ApiResponse[ProductDetail], summary="Get product details with sector and agent breakdowns")
def get_product(product_name: str, db: Session = Depends(get_db)):
    service = ProductService(db)
    detail = service.get_product_detail(product_name)
    return ApiResponse(data=detail)
