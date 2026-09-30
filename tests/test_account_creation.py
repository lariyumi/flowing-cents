from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_account_creation(client):
    valid_user = {
        "name": "TestName",
        "email": "testemail@gmail.com",
        "password": "TestPassword",
        "active": True
    }

    response = client.post("/user/create-account", 
                           json=valid_user)

    assert response.status_code == 200
    assert response.json() == {
        "message": f"User successfully registered"
    }

def test_error_no_name(client):
    invalid_user = {
        "name": "",
        "email": "testemail@gmail.com",
        "password": "TestPassword",
        "active": True
    }

    response = client.post("/user/create-account", json=invalid_user)

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["body", "name"]
    assert "at least 2 characters" in errors[0]["msg"]

def test_error_no_email(client):
    invalid_user = {
        "name": "TestName",
        "email": "",
        "password": "TestPassword",
        "active": True
    }

    response = client.post("/user/create-account", json=invalid_user)

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["body", "email"]
    assert "not a valid email address" in errors[0]["msg"]

def test_error_existing_email(client):
    user = {
        "name": "TestName",
        "email": "testemail@gmail.com",
        "password": "TestPassword",
        "active": True
    }

    response = client.post("/user/create-account", json=user)

    response = client.post("/user/create-account", json=user)

    assert response.status_code == 400

    errors = response.json()["detail"]
    assert "Email already used" in errors

def test_error_no_password(client):
    user = {
        "name": "TestName",
        "email": "testemail@gmail.com",
        "password": "",
        "active": True
    }

    response = client.post("/user/create-account", json=user)

    assert response.status_code == 422

    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["body", "password"]
    assert "at least 6 characters" in errors[0]["msg"]