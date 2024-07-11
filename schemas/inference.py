from pydantic import BaseModel, Field
from pydantic_core import core_schema
from typing import Optional, Dict, Any
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

class InferenceState(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    error = "error"

class InferenceTask(BaseModel):
    state: InferenceState = InferenceState.pending
    message: str = ""

class InferenceResult(BaseModel):
    text: Optional[str] = None
    task: InferenceTask

class InferenceMetadata(BaseModel):
    caracteres: Optional[int] = None
    palabras: Optional[int] = None
    tokens: Optional[int] = None
    idioma: Optional[str] = None
    porcentaje_reduccion: Optional[float] = None

class Inference(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    id_mzg_content: int
    id_agent: PyObjectId
    result: InferenceResult
    metadata: Optional[InferenceMetadata] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
    }