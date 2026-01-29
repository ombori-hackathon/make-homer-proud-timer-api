from datetime import date

from sqlalchemy.orm import Session

from app.daos.base import BaseDAO
from app.models.user_stats import UserStats


class UserStatsDAO(BaseDAO[UserStats]):
    def __init__(self, db: Session):
        super().__init__(db, UserStats)

    def get_or_create(self, user_id: str = "default") -> UserStats:
        stats = self.db.query(UserStats).filter(UserStats.user_id == user_id).first()
        if not stats:
            stats = self.create(
                {
                    "user_id": user_id,
                    "total_sessions": 0,
                    "total_focus_minutes": 0,
                    "current_streak": 0,
                    "sessions_by_god": {},
                }
            )
        return stats

    def update_on_session_complete(
        self,
        user_id: str,
        god_id: int,
        god_name: str,
        duration_minutes: int,
        session_type: str,
    ) -> UserStats:
        stats = self.get_or_create(user_id)

        # Update totals
        stats.total_sessions += 1
        if session_type == "focus":
            stats.total_focus_minutes += duration_minutes

        # Update sessions by god
        sessions_by_god = dict(stats.sessions_by_god or {})
        sessions_by_god[god_name] = sessions_by_god.get(god_name, 0) + 1
        stats.sessions_by_god = sessions_by_god

        # Update streak
        today = date.today()
        if stats.last_session_date:
            days_diff = (today - stats.last_session_date).days
            if days_diff == 1:
                stats.current_streak += 1
            elif days_diff > 1:
                stats.current_streak = 1
            # If same day, don't change streak
        else:
            stats.current_streak = 1

        stats.last_session_date = today

        self.db.commit()
        self.db.refresh(stats)
        return stats
