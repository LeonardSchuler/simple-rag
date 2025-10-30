from ..core import ports


class EmptyDB(ports.VectorDatabase):
    def add_documents(self, documents: list[str]) -> bool:
        return True

    def get_embeddings(self, documents: str | list[str]) -> list[ports.Embedding]:
        return []

    def inverse_embeddings(self, embeddings: list[ports.Embedding]) -> list[str]:
        return []

    def search_similar(self, embedding: ports.Embedding) -> list[ports.Embedding]:
        return []
