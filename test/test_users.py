import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from infraestructure.db.db import get_db
from infraestructure.models.user import Base, User
from main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module", autouse=True)
def set_environment():
    os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
    yield
    os.environ['DATABASE_URL'] = 'sqlite:///./prod.db'

@pytest.fixture(scope="module")
def create_tables(set_environment):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(create_tables):
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()

@pytest.fixture
def client():
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    del app.dependency_overrides[get_db]

def test_add_user(client, db_session):
    response = client.post("/users", json={"name": "John Doe", "age": 30})

    json_response = response.json()
    user = client.get(f"/users/{json_response.get('id')}")
    user_json = user.json()

    assert response.status_code == 200
    assert response is not None
    assert user_json.get('name') == "John Doe"
    assert user_json.get('age') == 30

def test_get_all_users(client, db_session):
    client.post("/users", json={"name": "John Doe", "age": 30})
    client.post("/users", json={"name": "Alejo", "age": 22})

    response = client.get("/users")
    assert response.status_code == 200

    users = response.json()

    first_user = {"name": "John Doe", "age": 30}
    assert any(user['name'] == first_user['name'] and user['age'] == first_user['age'] for user in users)
    second_user = {"name": "Alejo", "age": 22}
    assert any(user['name'] == second_user['name'] and user['age'] == second_user['age'] for user in users)
