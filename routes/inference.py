from fastapi import APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from services.agent_service import get_agent_by_id

router = APIRouter(
    prefix='/inference',
    tags=['inference']
)

@router.get("/", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})

async def get_inference():
    id = "6643d2fa1ff9b7b60b557df5"
    agent = get_agent_by_id(id)
    nombre = agent['rol']

    return { 
        "agent": agent,
        "nombre": nombre,
    }