from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.daos import UserStatsDAO
from app.db import get_db
from app.schemas import UserStats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", response_model=UserStats)
async def get_stats(db: Session = Depends(get_db)):
    """Get user statistics"""
    dao = UserStatsDAO(db)
    return dao.get_or_create("default")
