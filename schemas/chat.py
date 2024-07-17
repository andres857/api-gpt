from pydantic import BaseModel
from typing import List

class Messages(BaseModel):
    role: str
    content: str

class Context(BaseModel):
    messages: List[Messages]

class ChatRequest(BaseModel):
    id_club: int
    context: Context