from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module

client = TestClient(app_module.app)
_original_activities = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: restore a fresh copy of the in-memory activities before each test
    app_module.activities = deepcopy(_original_activities)
    yield
    app_module.activities = deepcopy(_original_activities)


def test_get_activities():
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    normalized = email.strip().lower()
    assert normalized in [p.strip().lower() for p in app_module.activities[activity]["participants"]]
    assert "Signed up" in resp.json().get("message", "")


def test_signup_duplicate_returns_400():
    # Arrange
    activity = "Chess Club"
    existing = app_module.activities[activity]["participants"][0]
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": existing})
    # Assert
    assert resp.status_code == 400


def test_signup_activity_not_found_returns_404():
    # Act
    resp = client.post("/activities/NonexistentActivity/signup", params={"email": "a@b.com"})
    # Assert
    assert resp.status_code == 404


def test_unregister_success():
    # Arrange
    activity = "Chess Club"
    existing = app_module.activities[activity]["participants"][0]
    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": existing})
    # Assert
    assert resp.status_code == 200
    normalized = existing.strip().lower()
    assert all(p.strip().lower() != normalized for p in app_module.activities[activity]["participants"])


def test_unregister_participant_not_found_returns_404():
    # Act
    resp = client.delete("/activities/Chess Club/signup", params={"email": "notfound@mergington.edu"})
    # Assert
    assert resp.status_code == 404
