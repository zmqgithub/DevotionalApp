# app/modules/mosques/model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Mosque(Base):
    __tablename__ = "mosques"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    arabic_name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Contact
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)

    # Features
    capacity = Column(Integer, nullable=True)
    has_parking = Column(Boolean, default=False)
    has_wudu_area = Column(Boolean, default=True)
    has_women_area = Column(Boolean, default=True)
    has_handicap_access = Column(Boolean, default=False)
    has_library = Column(Boolean, default=False)

    # Multimedia
    images = Column(JSON, nullable=True)  # Array of image URLs
    cover_image = Column(String(500), nullable=True)

    # Additional info
    denomination = Column(String(100), nullable=True)  # Sunni, Shia, etc.
    language = Column(String(50), nullable=True)  # Primary language
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    city = relationship("City", back_populates="mosques")
    events = relationship("Event", back_populates="mosque", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="mosque", cascade="all, delete-orphan")