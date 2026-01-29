from sqlalchemy.orm import Session

from app.daos.base import BaseDAO
from app.models.user_preferences import UserPreferences


class UserPreferencesDAO(BaseDAO[UserPreferences]):
    def __init__(self, db: Session):
        super().__init__(db, UserPreferences)

    def get_or_create(self, user_id: str = "default") -> UserPreferences:
        prefs = (
            self.db.query(UserPreferences)
            .filter(UserPreferences.user_id == user_id)
            .first()
        )
        if not prefs:
            prefs = self.create(
                {
                    "user_id": user_id,
                    "selected_god_id": None,
                    "favorite_god_ids": [],
                    "auto_select_favorites": False,
                }
            )
        return prefs

    def toggle_favorite(self, user_id: str, god_id: int) -> UserPreferences:
        prefs = self.get_or_create(user_id)
        favorites = list(prefs.favorite_god_ids or [])

        if god_id in favorites:
            favorites.remove(god_id)
        else:
            favorites.append(god_id)

        prefs.favorite_god_ids = favorites
        self.db.commit()
        self.db.refresh(prefs)
        return prefs

    def set_selected_god(self, user_id: str, god_id: int | None) -> UserPreferences:
        prefs = self.get_or_create(user_id)
        prefs.selected_god_id = god_id
        self.db.commit()
        self.db.refresh(prefs)
        return prefs

    def update_preferences(
        self,
        user_id: str,
        selected_god_id: int | None = None,
        favorite_god_ids: list[int] | None = None,
        auto_select_favorites: bool | None = None,
    ) -> UserPreferences:
        prefs = self.get_or_create(user_id)

        if selected_god_id is not None:
            prefs.selected_god_id = selected_god_id
        if favorite_god_ids is not None:
            prefs.favorite_god_ids = favorite_god_ids
        if auto_select_favorites is not None:
            prefs.auto_select_favorites = auto_select_favorites

        self.db.commit()
        self.db.refresh(prefs)
        return prefs
