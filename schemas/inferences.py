from pydantic import BaseModel, Field
from pydantic_core import core_schema
from typing import List, Optional, Dict,Any
from datetime import datetime
from bson import ObjectId
from enum import Enum

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]),
        ])

    @classmethod
    def validate(cls, value):
        if isinstance(value, ObjectId):
            return value
        if ObjectId.is_valid(value):
            return ObjectId(value)
        raise ValueError("Invalid ObjectId")

class TaskState(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"

class Task(BaseModel):
    state: TaskState = TaskState.PENDING
    message: str = ""

class Metadata(BaseModel):
    tokens: int
    completion_time: Optional[datetime] = None

class Inference(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # id_video_transcription: PyObjectId
    text: Dict[str, str]  # Cambiado para permitir múltiples idiomas
    task: Optional[Task] = None
    metadata: Optional[Metadata] = None

class Inferences(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id_video_transcription: PyObjectId
    inferences: List[Inference]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}