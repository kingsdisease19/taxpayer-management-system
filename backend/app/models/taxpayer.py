from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Taxpayer(Base):
    __tablename__ = "taxpayers"

    id = Column(Integer, primary_key=True, index=True)
    tpin = Column(String, unique=True, index=True, nullable=False)
    taxpayer_type = Column(String, nullable=False)
    business_name = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=False)
    address = Column(String, nullable=True)
    registration_status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())