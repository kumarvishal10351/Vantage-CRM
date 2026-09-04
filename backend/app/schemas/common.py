from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationMeta(BaseModel):
    page: int = Field(..., description="Current page number (1-indexed)")
    limit: int = Field(..., description="Items per page")
    total_items: int = Field(..., description="Total count of matching items")
    total_pages: int = Field(..., description="Total number of pages")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T] = Field(..., description="Page items")
    pagination: PaginationMeta = Field(..., description="Pagination metadata")

class ApiResponse(BaseModel, Generic[T]):
    success: bool = Field(True, description="Request status")
    data: T = Field(..., description="Payload data")
    message: Optional[str] = Field(None, description="Optional informational message")
