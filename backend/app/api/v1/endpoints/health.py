from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import engine


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health_check():

    database = 0

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        database = 1

    except Exception:
        database = 0

    return {
        "status": "healthy",
        "database": database,
    }