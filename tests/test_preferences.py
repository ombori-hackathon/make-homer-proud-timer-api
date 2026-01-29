import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models.god import God

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


def seed_gods(db):
    """Seed test gods"""
    gods = [
        God(
            id=1,
            name="Athena",
            domain="Wisdom & Strategy",
            icon="brain",
            coaching_style="wise",
            focus_messages=["Focus message 1"],
            break_messages=["Break message 1"],
            session_start_messages=["Start message 1"],
        ),
        God(
            id=2,
            name="Ares",
            domain="War & Strength",
            icon="flame",
            coaching_style="aggressive",
            focus_messages=["Focus message 2"],
            break_messages=["Break message 2"],
            session_start_messages=["Start message 2"],
        ),
    ]
    db.add_all(gods)
    db.commit()


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    # Seed test data
    db = TestingSessionLocal()
    seed_gods(db)
    db.close()

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_get_preferences_creates_default(client):
    """Preferences endpoint should create default user if none exists"""
    response = client.get("/preferences")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "default"
    assert data["selected_god_id"] is None
    assert data["favorite_god_ids"] == []
    assert data["auto_select_favorites"] is False


def test_get_preferences_returns_existing(client):
    """Preferences endpoint should return existing preferences"""
    # First call creates the preferences
    client.get("/preferences")
    # Second call returns the same preferences
    response = client.get("/preferences")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_toggle_favorite_adds_god(client):
    """Toggle favorite should add god when not present"""
    response = client.patch("/preferences/favorites", json={"god_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert 1 in data["favorite_god_ids"]


def test_toggle_favorite_removes_god(client):
    """Toggle favorite should remove god when already present"""
    # Add first
    client.patch("/preferences/favorites", json={"god_id": 1})
    # Remove by toggling again
    response = client.patch("/preferences/favorites", json={"god_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert 1 not in data["favorite_god_ids"]


def test_toggle_favorite_invalid_god(client):
    """Toggle favorite should return 400 for invalid god_id"""
    response = client.patch("/preferences/favorites", json={"god_id": 999})
    assert response.status_code == 400
    assert "Invalid god_id" in response.json()["detail"]


def test_set_selected_god(client):
    """Set selected god should update preferences"""
    response = client.patch("/preferences/selected-god", json={"god_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["selected_god_id"] == 1


def test_set_selected_god_null(client):
    """Set selected god to null should clear selection"""
    # Set first
    client.patch("/preferences/selected-god", json={"god_id": 1})
    # Clear
    response = client.patch("/preferences/selected-god", json={"god_id": None})
    assert response.status_code == 200
    data = response.json()
    assert data["selected_god_id"] is None


def test_set_selected_god_invalid(client):
    """Set selected god should return 400 for invalid god_id"""
    response = client.patch("/preferences/selected-god", json={"god_id": 999})
    assert response.status_code == 400
    assert "Invalid god_id" in response.json()["detail"]


def test_update_preferences_full(client):
    """PUT preferences should update all fields"""
    response = client.put(
        "/preferences",
        json={
            "selected_god_id": 2,
            "favorite_god_ids": [1, 2],
            "auto_select_favorites": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["selected_god_id"] == 2
    assert data["favorite_god_ids"] == [1, 2]
    assert data["auto_select_favorites"] is True


def test_update_preferences_partial(client):
    """PUT preferences should allow partial updates"""
    response = client.put("/preferences", json={"auto_select_favorites": True})
    assert response.status_code == 200
    data = response.json()
    assert data["auto_select_favorites"] is True
    assert data["selected_god_id"] is None  # unchanged


def test_update_preferences_invalid_selected_god(client):
    """PUT preferences should validate selected_god_id"""
    response = client.put("/preferences", json={"selected_god_id": 999})
    assert response.status_code == 400
    assert "Invalid selected_god_id" in response.json()["detail"]


def test_update_preferences_invalid_favorite(client):
    """PUT preferences should validate favorite_god_ids"""
    response = client.put("/preferences", json={"favorite_god_ids": [1, 999]})
    assert response.status_code == 400
    assert "Invalid god_id in favorites" in response.json()["detail"]


def test_multiple_favorites(client):
    """Should support multiple favorites"""
    client.patch("/preferences/favorites", json={"god_id": 1})
    response = client.patch("/preferences/favorites", json={"god_id": 2})
    assert response.status_code == 200
    data = response.json()
    assert 1 in data["favorite_god_ids"]
    assert 2 in data["favorite_god_ids"]
