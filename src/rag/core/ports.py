from typing import Protocol


Embedding = list[float]


class VectorDatabase(Protocol):
    def add_documents(self, documents: list[str]) -> bool: ...
    def get_embeddings(self, documents: list[str]) -> list[Embedding]: ...
    def inverse_embeddings(self, embeddings: list[Embedding]) -> list[str]: ...
    def search_similar(self, embedding: Embedding) -> list[Embedding]: ...

    def get_embedding(self, document: str) -> Embedding:
        embedding = self.get_embeddings([document])
        if embedding:
            return embedding[0]
        else:
            return []


class LanguageModel(Protocol):
    def answer(self, message: str, context: None | list[str] = None) -> str: ...


class MessageService(Protocol):
    def process(self, message: str) -> str: ...
