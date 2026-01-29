from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import God

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    db = TestingSessionLocal()
    test_god = God(
        id=1,
        name="TestGod",
        domain="Testing",
        icon="test.icon",
        coaching_style="Patient",
        focus_messages=["Focus"],
        break_messages=["Break"],
        session_start_messages=["Start"],
    )
    db.add(test_god)
    db.commit()
    db.close()

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_create_session(client):
    response = client.post(
        "/sessions",
        json={
            "god_id": 1,
            "session_type": "focus",
            "duration_seconds": 1500,
            "started_at": datetime.now().isoformat(),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["god_id"] == 1
    assert data["session_type"] == "focus"
    assert data["duration_seconds"] == 1500
    assert data["was_completed"] is False


def test_create_session_invalid_god(client):
    response = client.post(
        "/sessions",
        json={
            "god_id": 999,
            "session_type": "focus",
            "duration_seconds": 1500,
            "started_at": datetime.now().isoformat(),
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid god_id"


def test_complete_session(client):
    # Create session first
    create_response = client.post(
        "/sessions",
        json={
            "god_id": 1,
            "session_type": "focus",
            "duration_seconds": 1500,
            "started_at": datetime.now().isoformat(),
        },
    )
    session_id = create_response.json()["id"]

    # Complete it
    response = client.patch(f"/sessions/{session_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["was_completed"] is True
    assert data["completed_at"] is not None


def test_get_today_sessions(client):
    # Create a session
    client.post(
        "/sessions",
        json={
            "god_id": 1,
            "session_type": "focus",
            "duration_seconds": 1500,
            "started_at": datetime.now().isoformat(),
        },
    )

    response = client.get("/sessions/today")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "sessions" in data
    assert len(data["sessions"]) == 1
