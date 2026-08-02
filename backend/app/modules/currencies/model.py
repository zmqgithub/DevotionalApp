from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(3), unique=True, index=True, nullable=False)
    symbol = Column(String(10), nullable=True)
    symbol_native = Column(String(10), nullable=True)
    decimal_digits = Column(Integer, default=2)
    rounding = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True)

    # Relationships
    country = relationship("Country", back_populates="currencies")