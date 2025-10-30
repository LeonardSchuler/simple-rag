from pydantic import BaseModel


class Message(BaseModel):
    message: str


class Document(BaseModel):
    document: str
