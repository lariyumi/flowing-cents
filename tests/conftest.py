import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from dependencies import db_session
import models
from models import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    # Create new tables for each session and drop them when the work is done.
    Base.metadata.create_all(bind=engine)
    db = TestingSession()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(session: Session):
    def override_db_session():
        yield session

    # Switch the real database with the test database
    app.dependency_overrides[db_session] = override_db_session

    with TestClient(app) as test_client:
        yield test_client

    # Clear the overrides done for test
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_headers(session: Session, client: TestClient):
    user = {
        "name": "TestName",
        "email": "testemail@gmail.com",
        "password": "TestPassword",
        "active": True
    }
    
    response = client.post("/user/create-account", json=user)
    login_data = {"username": "testemail@gmail.com", "password": "TestPassword"}
    response = client.post("/user/login/auth-form", data=login_data)
    token = response.json()["access_token"]
    
    # 2. Return the header dictionary
    return {"Authorization": f"Bearer {token}"}