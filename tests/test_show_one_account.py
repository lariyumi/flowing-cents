from fastapi.testclient import TestClient

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def create_account(client: TestClient, auth_headers: dict):
    account = {
        "name_financial_institution": "Nubank",
        "balance": 1000.00,
        "user": 1
    }
    
    client.post("/account/create-account", json=account, headers=auth_headers)

def test_successful_request(client: TestClient, auth_headers: dict):
    create_account(client, auth_headers)

    response = client.get("/account/1", headers=auth_headers)

    assert response.status_code == 200
    assert "name_financial_institution" in response.json()
    assert "balance" in response.json()

def test_error_not_authenticated(client: TestClient, auth_headers: dict):
    create_account(client, auth_headers)
    
    response = client.get("/account/1")

    assert response.status_code == 401

    errors = response.json()["detail"]
    assert "Not authenticated" in errors

def test_error_permission_denied(client: TestClient, auth_headers: dict):
    create_account(client, auth_headers)

    user = {
        "name": "TestName",
        "email": "testemail2@gmail.com",
        "password": "TestPassword"
    }
        
    response = client.post("/user/create-account", json=user)
    login_data = {"username": "testemail2@gmail.com", "password": "TestPassword"}
    response = client.post("/user/login/auth-form", data=login_data)
    token = response.json()["access_token"]

    response = client.get("account/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403
    assert "don't have permission to view" in response.json()["detail"]

def test_error_inexistent_account(client: TestClient, auth_headers: dict):
    response = client.get("account/1", headers=auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Requested account doesn't exist"