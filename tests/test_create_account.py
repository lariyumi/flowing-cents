from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_account_creation(client: TestClient, auth_headers, create_user, create_account):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    account = create_account()

    response = client.post("/account/create-account", json=account, headers=auth_headers())

    assert response.status_code == 201
    assert response.json() == {
        "message": "Account successfully created"
    }

def test_error_not_authenticated(client: TestClient, create_account):
    account = create_account()

    response = client.post("/account/create-account", json=account)

    assert response.status_code == 401
    errors = response.json()["detail"]

    assert "Not authenticated" in errors

def test_error_forbidden_user(client: TestClient, auth_headers, create_user, create_account):
    user = create_user()

    client.post("/user/create-account", json=user)

    account = create_account(user=2)
    
    response = client.post("/account/create-account", json=account, headers=auth_headers())

    assert response.status_code == 403
    assert response.json() == {
        "detail": "User linked to the account doesn't match authenticated user"
    }

def test_error_no_name(client: TestClient, auth_headers, create_user, create_account):
    user = create_user()

    client.post("/user/create-account", json=user)

    account = create_account(name_financial_institution="")

    response = client.post("/account/create-account", json=account, headers=auth_headers())

    assert response.status_code == 422

    error = response.json()["detail"]
    assert "at least 2 characters" in error[0]["msg"]