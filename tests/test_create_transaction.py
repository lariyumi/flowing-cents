from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successfull_transaction_creation(client: TestClient, create_user, auth_headers, create_account, create_transaction):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    account = create_account()

    client.post("/account/create-account", json=account, headers=auth_headers())

    transaction = create_transaction()

    response = client.post("/transaction", json=transaction, headers=auth_headers())

    assert response.status_code == 201
    assert response.json() == {
        "message": "Transaction successfully registered"
    }

def test_invalid_user(client: TestClient, create_user, auth_headers, create_account, create_transaction):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    email = "testemail2@gmail.com"
    user2 = create_user(email=email)

    client.post("/user/create-account", json=user2)

    account = create_account()

    client.post("/account/create-account", json=account, headers=auth_headers())

    transaction = create_transaction()

    response = client.post("/transaction", json=transaction, headers=auth_headers(email=email))

    assert response.status_code == 403
    assert response.json() == {
        "detail": "User linked to the account doesn't match authenticated user"
    }

def test_user_not_authenticated(client: TestClient, create_transaction):
    transaction = create_transaction()

    result = client.post("/transaction", json=transaction)

    assert result.status_code == 401
    errors = result.json()["detail"]

    assert "Not authenticated" in errors

def test_invalid_account(client: TestClient, create_user, auth_headers, create_transaction):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    transaction = create_transaction()

    response = client.post("/transaction", json=transaction, headers=auth_headers())

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Informed account doesn't exist"
    }

def test_invalid_type_transaction(client: TestClient, create_user, auth_headers, create_account, create_transaction):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    account = create_account()

    client.post("/account/create-account", json=account, headers=auth_headers())

    transaction = create_transaction(type_transaction="INVALID")

    response = client.post("/transaction", json=transaction, headers=auth_headers())

    assert response.status_code == 422

    error = response.json()["detail"]
    assert "'EXPENSE' or 'INCOME'" in error[0]["msg"]