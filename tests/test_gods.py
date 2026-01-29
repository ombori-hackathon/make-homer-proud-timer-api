import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import God

# Create test database
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

    # Seed test data
    db = TestingSessionLocal()
    test_god = God(
        id=1,
        name="TestGod",
        domain="Testing",
        icon="test.icon",
        coaching_style="Patient tester",
        focus_messages=["Focus message 1"],
        break_messages=["Break message 1"],
        session_start_messages=["Start message 1"],
    )
    db.add(test_god)
    db.commit()
    db.close()

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_get_all_gods(client):
    response = client.get("/gods")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "TestGod"
    assert data[0]["domain"] == "Testing"
    assert data[0]["icon"] == "test.icon"
    assert data[0]["coaching_style"] == "Patient tester"
    assert data[0]["focus_messages"] == ["Focus message 1"]
    assert data[0]["break_messages"] == ["Break message 1"]
    assert data[0]["session_start_messages"] == ["Start message 1"]


def test_get_god_by_id(client):
    response = client.get("/gods/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestGod"


def test_get_god_not_found(client):
    response = client.get("/gods/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "God not found"
