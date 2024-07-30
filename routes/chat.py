from fastapi import APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Any
from schemas.chat import ChatRequest
from services.chat_service import get_transcriptions_by_id_club,get_context_chat_messages, chat_agent, chat_agent_claude_model, get_context_chat_messages_for_claude

router = APIRouter(
    prefix='/chat',
    tags=['chat']
)

# crea el document en la collection para el video
@router.post("", responses={
    200: {"description": "chat uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def chat_responses(body: ChatRequest = Body(...)):
    print(body.id_club)
    # video_t = await get_transcriptions_by_id_club(body.id_club)
    tx = await chat_agent(body.id_club, body)
    return {"message": tx}

# crea el document en la collection para el video
@router.post("/claude-model", responses={
    200: {"description": "chat uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def chat_responses(body: ChatRequest = Body(...)):
    print(body.id_club)
    tx = await chat_agent_claude_model(body.id_club, body.context)
    return {"message": tx}
