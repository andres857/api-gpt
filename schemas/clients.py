from pydantic import BaseModel, Field
from pydantic_core import core_schema
from typing import Optional, List, Any
from enum import Enum
from datetime import datetime
from bson import ObjectId

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

class TranscriptionState(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Tokens(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: int = 0

class Cost(BaseModel):
    prompt_tokens: float = 0.0
    total_tokens: float = 0.0
    completion_tokens: float = 0.0

class InferenceData(BaseModel):
    tokens: Tokens = Field(default_factory=Tokens)
    cost: Cost = Field(default_factory=Cost)
    limit: int = 0

class Customer(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id_customer: int
    state_transcription: TranscriptionState = TranscriptionState.pending
    transcriptions: List[PyObjectId] = []
    inference: InferenceData = Field(default_factory=InferenceData)
    inference_chat: InferenceData = Field(default_factory=InferenceData)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CustomerCreate(BaseModel):
    id_customer: int

class CustomerUpdate(BaseModel):
    state_transcription: Optional[TranscriptionState] = None
    transcriptions: Optional[List[PyObjectId]] = None
    inference: Optional[InferenceData] = None
    inference_chat: Optional[InferenceData] = None