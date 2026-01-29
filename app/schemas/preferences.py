from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserPreferences(BaseModel):
    id: int
    user_id: str
    selected_god_id: int | None
    favorite_god_ids: list[int]
    auto_select_favorites: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPreferencesUpdate(BaseModel):
    selected_god_id: int | None = None
    favorite_god_ids: list[int] | None = None
    auto_select_favorites: bool | None = None


class FavoriteToggle(BaseModel):
    god_id: int


class SelectedGodUpdate(BaseModel):
    god_id: int | None
