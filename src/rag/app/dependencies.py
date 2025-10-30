from typing import Annotated
from fastapi import Depends

from ..core import services, ports
from ..adapters import db, language_models


_database = db.EmptyDB()
_language_model = language_models.Parrot()


def get_database() -> ports.VectorDatabase:
    return _database


def get_language_model():
    return _language_model


# def get_embedder(
#    database: Annotated[db.Database, Depends(get_database)],
# ) -> services.EmbeddingService:
#    return services.EmbeddingService(database=database)


def get_message_service(
    vector_db: Annotated[ports.VectorDatabase, Depends(get_database)],
    language_model: Annotated[ports.LanguageModel, Depends(get_language_model)],
) -> ports.MessageService:
    return services.MessageService(vector_db=vector_db, language_model=language_model)
