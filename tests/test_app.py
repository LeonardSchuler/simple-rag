import pytest
from fastapi.testclient import TestClient
from rag.app.main import app
from rag.app.dependencies import get_language_model, get_database
from rag.adapters import db, language_models

documents = [
    "The Eiffel Tower is located in Paris, France.",
    "Mount Everest is the highest mountain in the world.",
    "The Great Wall of China is visible from space.",
    "The Amazon rainforest is located in South America.",
    "The Sahara is the largest hot desert in the world.",
]


@pytest.fixture
def client():
    app.dependency_overrides[get_language_model] = lambda: language_models.Parrot()
    app.dependency_overrides[get_database] = lambda: db.EmptyDB()
    client = TestClient(app)
    return client


def test_send_message(client):
    message = "This is a test"
    res = client.post("/api/message", json={"message": message})
    assert res.status_code == 200
    data = res.json()
    assert data["response"] == message


def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    content_type = res.headers.get("Content-Type", "")
    assert "text/html" in content_type.lower()
