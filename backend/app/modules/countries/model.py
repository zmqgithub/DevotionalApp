from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    iso_code = Column(String(2), unique=True, index=True, nullable=False)
    iso3_code = Column(String(3), unique=True, nullable=True)
    phone_code = Column(String(10), nullable=True)
    currency_code = Column(String(3), nullable=True)
    currency_name = Column(String(50), nullable=True)
    region = Column(String(100), nullable=True)
    subregion = Column(String(100), nullable=True)
    capital = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    flag = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    states = relationship("State", back_populates="country", cascade="all, delete-orphan")
    currencies = relationship("Currency", back_populates="country", cascade="all, delete-orphan")
    languages = relationship("Language", back_populates="country", cascade="all, delete-orphan")