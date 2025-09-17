from pydantic import BaseModel
from typing import List, Optional

class ChatMessages(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    service: str
    message: str
    history: Opitional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    response: str