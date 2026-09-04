from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class SalesTeam(Base):
    __tablename__ = "sales_teams"
    __table_args__ = {"schema": "crm_sales"}

    sales_agent = Column(String(100), primary_key=True)
    manager = Column(String(100), nullable=False)
    regional_office = Column(String(50), nullable=False)

    opportunities = relationship("Opportunity", back_populates="sales_agent_rel")
