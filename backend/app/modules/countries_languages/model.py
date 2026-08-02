# app/modules/countries_languages/model.py
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class CountryLanguage(Base):
    __tablename__ = "countries_languages"

    id = Column(Integer, primary_key=True, index=True)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)

    # Relationships
    country = relationship("Country")
    language = relationship("Language")

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('country_id', 'language_id', name='unique_country_language'),
    )