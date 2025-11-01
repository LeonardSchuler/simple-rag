import boto3
from typing import Annotated
from fastapi import Depends

from ..core import services, ports
from ..adapters import language_models, vector_dbs, embedders


session = boto3.Session()
_database = vector_dbs.EmptyDB()
_language_model = language_models.BedrockClaudeLLM(session=session)
_embedder = embedders.BedrockTitanEmbedder(session=session)


async def get_embedder() -> ports.Embedder:
    return _embedder


async def get_database() -> ports.VectorDatabase:
    return _database


async def get_language_model():
    return _language_model


async def get_chat_service(
    embedder: Annotated[ports.Embedder, Depends(get_embedder)],
    vector_db: Annotated[ports.VectorDatabase, Depends(get_database)],
    language_model: Annotated[ports.LanguageModel, Depends(get_language_model)],
) -> ports.ChatService:
    return services.ChatService(
        embedder=embedder, vector_db=vector_db, language_model=language_model
    )
