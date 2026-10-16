from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_deletion(client: TestClient, create_user, auth_headers, create_account, create_transaction):
    user = create_user()
    client.post("/user/create-account", json=user)

    auth = auth_headers()

    account = create_account()
    client.post("/account/create-account", json=account, headers=auth)
    balance = account["balance"]

    transaction = create_transaction()
    client.post("/transaction", json=transaction, headers=auth)

    response = client.delete("/transaction/delete/1", headers=auth)

    response_account = client.get("/account/1", headers=auth_headers())

    assert response.status_code == 200
    assert response.json()["message"] == "Transaction successfully deleted"
    assert response_account.json()["balance"] == balance