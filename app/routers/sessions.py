from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.daos import GodDAO, SessionDAO, UserStatsDAO
from app.db import get_db
from app.schemas import Session as SessionSchema
from app.schemas import SessionCreate, TodaySessions

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionSchema)
async def create_session(session_in: SessionCreate, db: Session = Depends(get_db)):
    """Create a new timer session"""
    # Validate god exists
    god_dao = GodDAO(db)
    god = god_dao.get(session_in.god_id)
    if not god:
        raise HTTPException(status_code=400, detail="Invalid god_id")

    # Validate session type
    if session_in.session_type not in ("focus", "break"):
        raise HTTPException(
            status_code=400, detail="session_type must be 'focus' or 'break'"
        )

    session_dao = SessionDAO(db)
    return session_dao.create_session(
        god_id=session_in.god_id,
        session_type=session_in.session_type,
        duration_seconds=session_in.duration_seconds,
        started_at=session_in.started_at,
    )


@router.patch("/{session_id}/complete", response_model=SessionSchema)
async def complete_session(session_id: int, db: Session = Depends(get_db)):
    """Mark a session as completed"""
    session_dao = SessionDAO(db)
    session = session_dao.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.was_completed:
        raise HTTPException(status_code=400, detail="Session already completed")

    # Complete the session
    completed_session = session_dao.complete_session(session_id)

    # Update user stats
    god_dao = GodDAO(db)
    god = god_dao.get(session.god_id)

    stats_dao = UserStatsDAO(db)
    stats_dao.update_on_session_complete(
        user_id="default",
        god_id=session.god_id,
        god_name=god.name if god else "Unknown",
        duration_minutes=session.duration_seconds // 60,
        session_type=session.session_type,
    )

    return completed_session


@router.get("/today", response_model=TodaySessions)
async def get_today_sessions(db: Session = Depends(get_db)):
    """Get today's sessions with count"""
    session_dao = SessionDAO(db)
    sessions = session_dao.get_today_sessions()
    count = session_dao.get_today_count()
    return TodaySessions(count=count, sessions=sessions)
