from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    thread_id: str | None = None


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatResponse(BaseModel):
    thread_id: str
    reply: ChatMessage


class ChatHistory(BaseModel):
    thread_id: str
    messages: list[ChatMessage]
