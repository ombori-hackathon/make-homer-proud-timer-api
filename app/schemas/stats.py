from datetime import date

from pydantic import BaseModel, ConfigDict


class UserStats(BaseModel):
    id: int
    user_id: str
    total_sessions: int
    total_focus_minutes: int
    current_streak: int
    last_session_date: date | None
    sessions_by_god: dict[str, int]

    model_config = ConfigDict(from_attributes=True)
