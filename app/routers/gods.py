from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.daos import GodDAO
from app.db import get_db
from app.schemas import God

router = APIRouter(prefix="/gods", tags=["gods"])


@router.get("", response_model=list[God])
async def get_gods(db: Session = Depends(get_db)):
    """Get all available gods"""
    dao = GodDAO(db)
    return dao.get_all()


@router.get("/{god_id}", response_model=God)
async def get_god(god_id: int, db: Session = Depends(get_db)):
    """Get a specific god by ID"""
    dao = GodDAO(db)
    god = dao.get(god_id)
    if not god:
        raise HTTPException(status_code=404, detail="God not found")
    return god
