from dataclasses import dataclass
from . import ports


@dataclass
class MessageService(ports.MessageService):
    vector_db: ports.VectorDatabase
    language_model: ports.LanguageModel

    def process(self, message: str) -> str:
        embedding = self.vector_db.get_embedding(message)
        similar_embeddings = self.vector_db.search_similar(embedding)
        similar_docs = self.vector_db.inverse_embeddings(similar_embeddings)
        return self.language_model.answer(message, similar_docs)
