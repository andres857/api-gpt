from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from enum import Enum

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class TaskState(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"

class Task(BaseModel):
    state: TaskState
    message: str

class Metadata(BaseModel):
    tokens: int
    completion_time: Optional[datetime] = None

class Agent(BaseModel):
    idAgent: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    text: str
    task: Task
    metadata: Metadata

class Inference(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    agents: List[Agent]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}