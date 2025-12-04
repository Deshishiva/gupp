
from pydantic import BaseModel
from typing import List, Dict, Any

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    persona: str
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str
    memory: Dict[str, Any]
