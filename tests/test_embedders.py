import boto3
import pytest
from rag.adapters.embedders import BedrockTitanEmbedder
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.aws
@pytest.mark.asyncio
async def test_titan_embedder():
    session = boto3.Session()
    embedder = BedrockTitanEmbedder(session)
    embedding = await embedder.embed("This is a test")
    assert isinstance(embedding, list)
    assert all(isinstance(x, float) for x in embedding)
