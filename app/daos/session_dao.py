from datetime import date, datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session as DBSession

from app.daos.base import BaseDAO
from app.models.session import Session


class SessionDAO(BaseDAO[Session]):
    def __init__(self, db: DBSession):
        super().__init__(db, Session)

    def create_session(
        self,
        god_id: int,
        session_type: str,
        duration_seconds: int,
        started_at: datetime,
    ) -> Session:
        return self.create(
            {
                "god_id": god_id,
                "session_type": session_type,
                "duration_seconds": duration_seconds,
                "started_at": started_at,
                "was_completed": False,
            }
        )

    def complete_session(
        self, session_id: int, completed_at: datetime | None = None
    ) -> Session | None:
        if completed_at is None:
            completed_at = datetime.now(timezone.utc)
        return self.update(
            session_id,
            {
                "completed_at": completed_at,
                "was_completed": True,
            },
        )

    def get_today_sessions(self) -> list[Session]:
        today = date.today()
        return (
            self.db.query(Session)
            .filter(func.date(Session.started_at) == today)
            .order_by(Session.started_at.desc())
            .all()
        )

    def get_today_count(self) -> int:
        today = date.today()
        return (
            self.db.query(Session)
            .filter(func.date(Session.started_at) == today)
            .filter(Session.was_completed)
            .count()
        )
