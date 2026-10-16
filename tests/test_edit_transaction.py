from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_edit(client: TestClient, create_user, auth_headers, create_account, create_transaction):
    user = create_user()
    client.post("/user/create-account", json=user)

    auth = auth_headers()

    account = create_account()
    client.post("/account/create-account", json=account, headers=auth)
    balance = account["balance"]

    transaction = create_transaction()
    client.post("/transaction", json=transaction, headers=auth)

    new_amount=100
    edited_transaction = create_transaction(amount=new_amount)
    response_transaction = client.put("/transaction/1", json=edited_transaction, headers=auth)

    response_account = client.get("/account/1", headers=auth_headers())

    assert response_transaction.status_code == 200
    assert response_transaction.json()["message"] == "Transaction successfully edited"
    assert response_account.json()["balance"] == balance - new_amount