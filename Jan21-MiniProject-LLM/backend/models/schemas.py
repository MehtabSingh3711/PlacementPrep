from pydantic import BaseModel
from typing import Optional, List
import uuid

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str

class Message(BaseModel):
    role: str
    content: str
    timestamp: str

class HistoryResponse(BaseModel):
    session_id: str
    history: List[Message]
