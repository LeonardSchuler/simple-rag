import boto3
import json
from ..core import ports
from botocore.exceptions import ClientError


class BedrockClaudeLLM(ports.LanguageModel):
    def __init__(
        self,
        session: boto3.Session,
        model_id: str = "eu.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature: float = 0.7,
        max_tokens: int = 512,
    ):
        self.model_id = model_id
        self.session = session
        # if region_name is not given, session.region_name should be set
        self.client = session.client("bedrock-runtime", region_name=session.region_name)
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def answer(self, message: str, context: None | list[str] = None) -> str:
        # Combine the context + user message into the prompt/messages format
        # Here I’ll use the “messages” style (Anthropic Claude) per docs.
        system_prompt = "You are a helpful assistant."
        # Format messages
        messages = [
            {"role": "user", "content": [{"type": "text", "text": system_prompt}]},
        ]

        context_text = "\n".join(context) if context else ""

        if context_text:
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Here are some references:\n{context_text}",
                        }
                    ],
                }
            )

        messages.append(
            {"role": "user", "content": [{"type": "text", "text": message}]}
        )

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": messages,
            }
        )

        try:
            resp = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
                accept="application/json",
                contentType="application/json",
            )
            resp_body = json.loads(resp["body"].read())
            # extract the text from the structure
            # According to docs, for messages style: output → message → content array with text key.
            output_message = resp_body["content"][0]["text"]
            return output_message
        except ClientError as e:
            # handle error
            raise RuntimeError(f"Bedrock Claude invocation error: {e}")
