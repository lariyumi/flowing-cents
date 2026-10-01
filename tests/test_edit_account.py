from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_edit(client: TestClient, auth_headers, create_user, create_account):
    user = create_user()
    client.post("/user/create-account", json=user)

    account = create_account()
    client.post("/account/create-account", json=account, headers=auth_headers())

    account = create_account(name_financial_institution="XP")
    response = client.put("/account/1", json=account ,headers=auth_headers())

    assert response.status_code == 200
    assert response.json() == {
        "message": "Account successfully edited"
    }

def test_error_no_account(client: TestClient, auth_headers, create_user, create_account):
    user = create_user()
    client.post("/user/create-account", json=user)
    
    account = create_account()
    response = client.put("/account/1", json=account ,headers=auth_headers())

    assert response.status_code == 400
    assert response.json()["detail"] == "Requested account doesn't exist"

def test_error_different_owner(client: TestClient, auth_headers, create_user, create_account):
    user = create_user()
    client.post("/user/create-account", json=user)

    account = create_account()
    client.post("/account/create-account", json=account, headers=auth_headers())

    user2 = create_user(email="testemail2@gmail.com")
    client.post("/user/create-account", json=user2)

    account = create_account(name_financial_institution="XP")
    response = client.put("/account/1", json=account, headers=auth_headers(email="testemail2@gmail.com"))

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission to edit another user's account"