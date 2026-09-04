from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "crm_sales"}

    product = Column(String(50), primary_key=True)
    series = Column(String(20), nullable=False)
    sales_price = Column(Numeric(10, 2), nullable=False)

    opportunities = relationship("Opportunity", back_populates="product_rel")
