from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.daos import GodDAO, UserPreferencesDAO
from app.db import get_db
from app.schemas import (
    FavoriteToggle,
    SelectedGodUpdate,
    UserPreferences,
    UserPreferencesUpdate,
)

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.get("", response_model=UserPreferences)
async def get_preferences(db: Session = Depends(get_db)):
    """Get user preferences (creates default if not exists)"""
    dao = UserPreferencesDAO(db)
    return dao.get_or_create("default")


@router.put("", response_model=UserPreferences)
async def update_preferences(
    prefs_in: UserPreferencesUpdate, db: Session = Depends(get_db)
):
    """Update user preferences"""
    dao = UserPreferencesDAO(db)
    god_dao = GodDAO(db)

    # Validate selected_god_id if provided
    if prefs_in.selected_god_id is not None:
        god = god_dao.get(prefs_in.selected_god_id)
        if not god:
            raise HTTPException(status_code=400, detail="Invalid selected_god_id")

    # Validate favorite_god_ids if provided
    if prefs_in.favorite_god_ids is not None:
        for god_id in prefs_in.favorite_god_ids:
            god = god_dao.get(god_id)
            if not god:
                raise HTTPException(
                    status_code=400, detail=f"Invalid god_id in favorites: {god_id}"
                )

    return dao.update_preferences(
        user_id="default",
        selected_god_id=prefs_in.selected_god_id,
        favorite_god_ids=prefs_in.favorite_god_ids,
        auto_select_favorites=prefs_in.auto_select_favorites,
    )


@router.patch("/favorites", response_model=UserPreferences)
async def toggle_favorite(toggle: FavoriteToggle, db: Session = Depends(get_db)):
    """Toggle a god as favorite (add if not present, remove if present)"""
    god_dao = GodDAO(db)
    god = god_dao.get(toggle.god_id)
    if not god:
        raise HTTPException(status_code=400, detail="Invalid god_id")

    dao = UserPreferencesDAO(db)
    return dao.toggle_favorite("default", toggle.god_id)


@router.patch("/selected-god", response_model=UserPreferences)
async def set_selected_god(update: SelectedGodUpdate, db: Session = Depends(get_db)):
    """Set the selected god for next session (null to clear)"""
    god_dao = GodDAO(db)

    # Validate god_id if not null
    if update.god_id is not None:
        god = god_dao.get(update.god_id)
        if not god:
            raise HTTPException(status_code=400, detail="Invalid god_id")

    dao = UserPreferencesDAO(db)
    return dao.set_selected_god("default", update.god_id)
