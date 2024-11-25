from fastapi import APIRouter, HTTPException, Query 
from pydantic import ValidationError, BaseModel
from bson import ObjectId
from schemas.agent import Agent
from services.agent_service import get_agent_by_id, get_all_agents, update_agent
from ia.inference import inference 

class InferenceBody(BaseModel):
    text: str = Query(...)

router = APIRouter(
    prefix='/agents',
    tags=['agents']
)

@router.get("/", responses = {
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_all():
    agents = await get_all_agents()
    return agents

@router.get("/{agent_id}", responses = {
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_agent_id(agent_id: str):
    agent = await get_agent_by_id(agent_id)
    return agent
