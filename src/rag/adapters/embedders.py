import boto3
import json
from ..core import ports


class BedrockTitanEmbedder(ports.Embedder):
    def __init__(
        self, session: boto3.Session, model_id: str = "amazon.titan-embed-text-v2:0"
    ):
        self.model_id = model_id
        self._session = session
        self.client = session.client("bedrock-runtime", region_name=session.region_name)

    async def embed(self, document: ports.Document) -> ports.Embedding:
        body = json.dumps({"inputText": document})
        resp = self.client.invoke_model(
            modelId=self.model_id,
            body=body,
            accept="application/json",
            contentType="application/json",
        )
        # parse embedding list from response
        result = json.loads(resp["body"].read())
        embedding = result.get("embedding")
        return embedding

    async def embed_batch(
        self, documents: list[ports.Document]
    ) -> list[ports.Embedding]:
        # simple sequential; could extend to batch mode if supported
        embeddings = []
        for d in documents:
            embeddings.append(await self.embed(d))
        return embeddings
