from sqlalchemy import Column, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Opportunity(Base):
    __tablename__ = "sales_pipeline"
    __table_args__ = {"schema": "crm_sales"}

    opportunity_id = Column(String(50), primary_key=True)
    sales_agent = Column(String(100), ForeignKey("crm_sales.sales_teams.sales_agent"), nullable=False)
    product = Column(String(50), ForeignKey("crm_sales.products.product"), nullable=False)
    account = Column(String(100), ForeignKey("crm_sales.accounts.account"), nullable=True)
    deal_stage = Column(String(20), nullable=False)
    engage_date = Column(Date, nullable=True)
    close_date = Column(Date, nullable=True)
    close_value = Column(Numeric(12, 2), nullable=True)

    sales_agent_rel = relationship("SalesTeam", back_populates="opportunities")
    product_rel = relationship("Product", back_populates="opportunities")
    account_rel = relationship("Account", back_populates="opportunities")
