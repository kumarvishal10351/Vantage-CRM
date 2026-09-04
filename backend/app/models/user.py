from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from backend.app.core.database import Base

class AppUser(Base):
    __tablename__ = "app_users"
    __table_args__ = {"schema": "crm_sales"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="Sales Agent")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
