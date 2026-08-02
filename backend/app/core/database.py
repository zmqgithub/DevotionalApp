# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# Convert PostgresDsn to string
database_url = str(settings.DATABASE_URL) if settings.DATABASE_URL else ""

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize database - create all tables
    """
    Base.metadata.create_all(bind=engine)