# schemas/agent.py
from pydantic import BaseModel
from typing import Optional

class AgentBase(BaseModel):
    rol: str
    prompt: str
    descripcion: Optional[str] = None

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    rol: Optional[str] = None
    prompt: Optional[str] = None
    descripcion: Optional[str] = None
    
class Agent(AgentBase):
    id: str

    class Config:
        orm_mode = True
