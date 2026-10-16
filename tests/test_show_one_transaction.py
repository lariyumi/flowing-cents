from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_request(client: TestClient, create_user, auth_headers, create_account, create_transaction):
    user = create_user()
    client.post("/user/create-account", json=user)

    auth = auth_headers()

    account = create_account()
    client.post("/account/create-account", json=account, headers=auth)

    transaction = create_transaction()
    client.post("/transaction", json=transaction, headers=auth)

    response = client.get("/transaction/1", headers=auth)

    assert response.status_code == 200
    assert "amount" in response.json()

def test_inexistent_transaction(client: TestClient, create_user, auth_headers):
    user = create_user()
    client.post("/user/create-account", json=user)

    auth = auth_headers()
    response = client.get("transaction/1", headers=auth)

    assert response.status_code == 400
    assert response.json()["detail"] == "Transaction not found"