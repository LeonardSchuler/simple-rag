import boto3
import pytest
from rag.adapters.language_models import BedrockClaudeLLM
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.aws
@pytest.mark.asyncio
async def test_bedrock_claude_language_model():
    session = boto3.Session()
    language_model = BedrockClaudeLLM(session)
    response = await language_model.answer("Hello! How are you?")
    assert isinstance(response, str)
    assert len(response) > 0
