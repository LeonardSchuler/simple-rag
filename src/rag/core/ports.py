from typing import Protocol


Embedding = list[float]
Vector = list[float]
Document = str


class Embedder(Protocol):
    async def embed(self, document: Document) -> Embedding: ...
    async def embed_batch(self, documents: list[Document]) -> list[Embedding]: ...


class VectorDatabase(Protocol):
    async def add(self, vectors: list[Vector], documents: list[Document]) -> bool: ...
    # def remove(self, vectors: list[Vector]) -> bool: ...
    async def search_similar(self, vector: Vector) -> list[Vector]: ...
    async def look_up(self, vectors: list[Vector]) -> list[Document]: ...


class LanguageModel(Protocol):
    async def answer(self, message: str, context: None | list[str] = None) -> str: ...


class ChatService(Protocol):
    async def answer(self, message: str) -> str: ...


class IngestionService(Protocol):
    async def add_documents(self, documents: list[Document]) -> bool: ...
