from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_deletion(client: TestClient, create_user, auth_headers, create_account, create_transaction, create_tag):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    account = create_account()

    client.post("/account/create-account", json=account, headers=auth_headers())

    tag = []
    tag.append(create_tag())
    transaction = create_transaction(tags=tag)

    client.post("/transaction", json=transaction, headers=auth_headers())

    response = client.delete("/tag/1", headers=auth_headers())

    assert response.status_code == 200
    assert response.json() == {
        "message": "Tag successfully deleted"
    }

def test_inexistent_tag(client: TestClient, create_user, auth_headers, create_account, create_transaction, create_tag):
    user = create_user()
    
    client.post("/user/create-account", json=user)

    account = create_account()

    client.post("/account/create-account", json=account, headers=auth_headers())

    tag = []
    tag.append(create_tag())
    transaction = create_transaction(tags=tag)

    client.post("/transaction", json=transaction, headers=auth_headers())

    response = client.delete("/tag/2", headers=auth_headers())

    assert response.status_code == 400
    assert "Tag not found" in response.json()["detail"] 