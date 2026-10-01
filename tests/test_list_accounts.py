from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_successful_request(client: TestClient, auth_headers: dict):
    response = client.get("/account", headers=auth_headers)

    assert response.status_code == 200
    assert "accounts" in response.json()

def test_error_not_authenticated(client: TestClient):
    response = client.get("/account")

    assert response.status_code == 401

    errors = response.json()["detail"]
    assert "Not authenticated" in errors