from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DevotionalApp API",
        "version": "1.0.0"
    }

@router.get("/db")
async def db_health_check(db: Session = Depends(get_db)):
    """Database health check"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}