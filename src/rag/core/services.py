from dataclasses import dataclass
from . import ports


@dataclass
class ChatService(ports.ChatService):
    embedder: ports.Embedder
    vector_db: ports.VectorDatabase
    language_model: ports.LanguageModel

    async def answer(self, message: str) -> str:
        embedding = await self.embedder.embed(message)
        similar_embeddings = await self.vector_db.search_similar(embedding)
        similar_docs = await self.vector_db.look_up(similar_embeddings)
        return await self.language_model.answer(message, similar_docs)


@dataclass
class IngestionService:
    embedder: ports.Embedder
    vector_db: ports.VectorDatabase

    async def add_documents(self, documents: list[str]) -> bool:
        embeddings = await self.embedder.embed_batch(documents)
        return await self.vector_db.add(embeddings, documents)
