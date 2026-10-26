from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_tag_creation(client: TestClient, create_user, auth_headers, create_account, create_transaction, create_tag):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    account = create_account()

    client.post("/account/create-account", json=account, headers=auth_headers())

    tag = []
    tag.append(create_tag())
    transaction = create_transaction(tags=tag)

    response = client.post("/transaction", json=transaction, headers=auth_headers())

    assert response.status_code == 201
    assert response.json() == {
        "message": "Transaction successfully registered"
    }

def test_no_name(client: TestClient, create_user, auth_headers, create_account, create_transaction, create_tag):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    account = create_account()

    client.post("/account/create-account", json=account, headers=auth_headers())

    tag = []
    tag.append(create_tag(name=""))
    transaction = create_transaction(tags=tag)

    response = client.post("/transaction", json=transaction, headers=auth_headers())

    assert response.status_code == 422
    
    errors = response.json()["detail"]
    assert "at least 2 characters" in errors[0]["msg"]