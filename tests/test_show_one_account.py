from fastapi.testclient import TestClient

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_request(client: TestClient, auth_headers, create_account, create_user):
    user = create_user()

    client.post("/user/create-account", json=user)

    account = create_account()

    client.post("/account/create-account", json=account, headers=auth_headers())

    response = client.get("/account/1", headers=auth_headers())

    assert response.status_code == 200
    assert "name_financial_institution" in response.json()
    assert "balance" in response.json()

def test_error_not_authenticated(client: TestClient, auth_headers, create_account, create_user):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    account = create_account()
    
    client.post("/account/create-account", json=account, headers=auth_headers())
    
    response = client.get("/account/1")

    assert response.status_code == 401

    errors = response.json()["detail"]
    assert "Not authenticated" in errors

def test_error_permission_denied(client: TestClient, auth_headers, create_account, create_user):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    account = create_account()
    
    client.post("/account/create-account", json=account, headers=auth_headers())

    user = create_user(email="testemail2@gmail.com")

    client.post("/user/create-account", json=user)

    response_auth = auth_headers(email="testemail2@gmail.com")

    response = client.get("account/1", headers=response_auth)

    assert response.status_code == 403
    assert "don't have permission to view" in response.json()["detail"]

def test_error_inexistent_account(client: TestClient, auth_headers, create_user):
    user = create_user()

    client.post("/user/create-account", json=user)

    response = client.get("account/1", headers=auth_headers())

    assert response.status_code == 400
    assert response.json()["detail"] == "Requested account doesn't exist"