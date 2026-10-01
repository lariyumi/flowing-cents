from fastapi.testclient import TestClient

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_delete(client: TestClient, auth_headers, create_user, create_account):
    user = create_user()

    client.post("/user/create-account", json=user)

    account = create_account()

    auth = auth_headers()

    client.post("/account/create-account", json=account, headers=auth)

    response = client.delete("/account/delete/1", headers=auth)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Account successfully deleted"
    }

def test_inexistent_account(client: TestClient, auth_headers, create_user):
    user = create_user()

    client.post("/user/create-account", json=user)

    auth = auth_headers()

    response = client.delete("/account/delete/1", headers=auth)

    assert response.status_code == 400
    assert response.json()["detail"] == "Requested account doesn't exist"

def test_not_authenticated(client: TestClient, auth_headers, create_user, create_account):
    user = create_user()

    client.post("/user/create-account", json=user)

    account = create_account()

    auth = auth_headers()

    client.post("/account/create-account", json=account, headers=auth)

    response = client.delete("/account/delete/1")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_incorrect_user(client: TestClient, auth_headers, create_user, create_account):
    user = create_user()

    client.post("/user/create-account", json=user)

    user2 = create_user(email="testemail2@gmail.com")

    client.post("/user/create-account", json=user2)

    account = create_account()

    client.post("/account/create-account", json=account, headers=auth_headers())

    response = client.delete("/account/delete/1", headers=auth_headers(email="testemail2@gmail.com"))

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission to delete another user's account"