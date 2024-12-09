import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from infraestructure.db.db import get_db
from infraestructure.models.user import Base
from main import app

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class TestUserAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    def setUp(self):
        self.db = SessionLocal()

        self.client = TestClient(app)

        self.db.execute(text("DELETE FROM users"))
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_add_user(self):
        response = client.post("/users/", json={"name": "John Doe", "age": 30})
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["name"], "John Doe")
        self.assertEqual(response.json()["age"], 30)

    def test_get_all_users(self):
        # Prueba para obtener todos los usuarios
        client.post("/users", json={"name": "John Doe", "age": 30})
        client.post("/users", json={"name": "Alejo", "age": 22})
        response = client.get("/users")
        users = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), 2)

    def test_get_user_by_id(self):
        response = client.post("/users/", json={"name": "John Doe", "age": 30})
        user_id = response.json()["id"]
        response = client.get(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], user_id)
        self.assertEqual(response.json()["name"], "John Doe")
        self.assertEqual(response.json()["age"], 30)

if __name__ == "__main__":
    unittest.main()
