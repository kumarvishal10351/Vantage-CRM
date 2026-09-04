from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "crm_sales"}

    account = Column(String(100), primary_key=True)
    sector = Column(String(50), nullable=False)
    year_established = Column(Integer, nullable=False)
    revenue = Column(Numeric(12, 2), nullable=False)
    employees = Column(Integer, nullable=False)
    office_location = Column(String(100), nullable=False)
    subsidiary_of = Column(String(100), ForeignKey("crm_sales.accounts.account"), nullable=True)

    parent_account = relationship("Account", remote_side=[account], backref="subsidiaries")
    opportunities = relationship("Opportunity", back_populates="account_rel")
