import pytest
from fastapi.testclient import TestClient
from rag.core import ports
from rag.app.main import app
from rag.app.dependencies import get_language_model, get_database, get_embedder
from rag.adapters import language_models, vector_dbs, embedders

documents = [
    "The Eiffel Tower is located in Paris, France.",
    "Mount Everest is the highest mountain in the world.",
    "The Great Wall of China is visible from space.",
    "The Amazon rainforest is located in South America.",
    "The Sahara is the largest hot desert in the world.",
]


class DummyEmbedder(ports.Embedder):
    async def embed(self, document: ports.Document) -> ports.Embedding:
        return [(ord(c) % 50) / 50 for c in document[:10]]

    async def embed_batch(
        self, documents: list[ports.Document]
    ) -> list[ports.Embedding]:
        return [await self.embed(d) for d in documents]


class Parrot(ports.LanguageModel):
    async def answer(self, message: str, context: None | list[str] = None):
        # context = "\n".join(context) if context else ""
        return f"{message}"


@pytest.fixture
def client():
    app.dependency_overrides[get_language_model] = lambda: Parrot()
    app.dependency_overrides[get_database] = lambda: vector_dbs.EmptyDB()
    app.dependency_overrides[get_embedder] = lambda: DummyEmbedder()
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
