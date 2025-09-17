from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    session_id: int
    user_message: str
    agent: str
    agent_response: str