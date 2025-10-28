import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Sign up a new participant
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Check participant is added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # Unregister the participant
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert f"Unregistered {email}" in unregister_resp.json()["message"]

    # Check participant is removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

def test_signup_activity_not_found():
    resp = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"

def test_unregister_not_found():
    resp = client.post("/activities/Chess Club/unregister?email=notfound@mergington.edu")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found in this activity"
