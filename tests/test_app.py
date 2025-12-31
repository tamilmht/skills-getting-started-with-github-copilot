import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@mergington.edu for Chess Club" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=duplicate@mergington.edu")
    # Second signup
    response = client.post("/activities/Programming%20Class/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up" in data["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First signup
    client.post("/activities/Gym%20Class/signup?email=unregister@mergington.edu")
    # Then unregister
    response = client.delete("/activities/Gym%20Class/participants/unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@mergington.edu from Gym Class" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@mergington.edu" not in data["Gym Class"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/participants/notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student is not signed up" in data["detail"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent%20Activity/participants/test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]