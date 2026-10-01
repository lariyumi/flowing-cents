from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_login(client: TestClient, create_user, login_request):
    user = create_user()

    client.post("/user/create-account", json=user)

    login = login_request()

    response = client.post("/user/login", json=login)

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0
    assert "refresh_token" in data
    assert isinstance(data["refresh_token"], str)
    assert len(data["refresh_token"]) > 0
    assert data.get("token_type") == "Bearer"

def test_error_wrong_email(client: TestClient, create_user, login_request):
    user = create_user()
    
    client.post("/user/create-account", json=user)
    
    login = login_request(email="estemail@gmail.com")
    
    response = client.post("/user/login", json=login)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "User not found or invalid credentials"
    }

def test_error_wrong_password(client: TestClient, create_user, login_request):
    user = create_user()

    client.post("/user/create-account", json=user)

    login = login_request(password="TestPasswor")

    response = client.post("/user/login", json=login)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "User not found or invalid credentials"
    }

def test_error_no_email(client: TestClient, login_request):
    login = login_request(email="")

    response = client.post("/user/login", json=login)

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["body", "email"]
    assert "not a valid email address" in errors[0]["msg"]

def test_error_no_password(client: TestClient, login_request):
    login = login_request(password="")

    response = client.post("/user/login", json=login)

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["body", "password"]
    assert "at least 6 characters" in errors[0]["msg"]