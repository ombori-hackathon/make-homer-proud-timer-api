import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

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

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_get_stats_creates_default(client):
    """Stats endpoint should create default user if none exists"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "default"
    assert data["total_sessions"] == 0
    assert data["total_focus_minutes"] == 0
    assert data["current_streak"] == 0
    assert data["sessions_by_god"] == {}


def test_get_stats_returns_existing(client):
    """Stats endpoint should return existing user stats"""
    # First call creates the stats
    client.get("/stats")
    # Second call returns the same stats
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
