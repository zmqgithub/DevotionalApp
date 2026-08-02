# app/modules/cities/model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    city_code = Column(String(20), nullable=True)
    type = Column(String(50), nullable=True)  # city, town, village
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    population = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    is_capital = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)

    # Relationships
    state = relationship("State", back_populates="cities")
    mosques = relationship("Mosque", back_populates="city", cascade="all, delete-orphan")