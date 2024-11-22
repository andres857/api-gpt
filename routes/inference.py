from fastapi import APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError, BaseModel, HttpUrl
from typing import Optional
from utils import save_video, save_video_from_url, delete_video
from services.transcription_service import  create, getTranscriptionVideoFromUrl, list_videos_by_id_client, update_status_transcription_by_id_content,get_completed_tasks_count, transcription_details
from schemas.video_transcription import VideoTranscription
import uuid
from services.inferences_service import create_inferences_for_videotranscription, get_inferences_by_id_video_transcription, get_inference_chat_by_id_video_transcription, used_tokens, used_tokens_by_client

router = APIRouter(
    prefix='/inference',
    tags=['inference']
)

# obtener informacion de una inferencia
@router.get("/{id}", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_transcription_info(id:str):
    transcription = await transcription_details(id)
    return transcription

@router.get("/testing/{id}", responses={
    200: {"description": "Inference gets successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def inferences_testing_route(id: str):
    inferences = await get_inference_chat_by_id_video_transcription(id)
    return inferences

# returna los tokens usados para una transcripcion de Video
@router.get("/video-transcription/tokens/{id_video_transcription}", responses={
    200: {"description": "Inference gets successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_tokens(id_video_transcription: str):
    tokens = await used_tokens(id_video_transcription)
    return {
        "tokens":tokens
    }

# returna los tokens usados para un cliente, recibe el id del cliente de MyZoneGo
@router.get("/video-transcription/client/{id_client}/tokens", responses={
    200: {"description": "Inference gets successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_tokens_used_by_Client(id_client: str):
    total_tokens, total_tokens_sent, total_tokens_generated, cost_prompt_tokens, cost_completion_tokens, cost_total_tokens = await used_tokens_by_client(id_client)
    return {
        "total_tokens":total_tokens,
        "prompt_tokens":total_tokens_sent,
        "completion_tokens": total_tokens_generated,
        "cost_total_tokens": cost_total_tokens,
        "cost_prompt_tokens":cost_prompt_tokens,
        "cost_completion_tokens":cost_completion_tokens,
    }

@router.get("/videotranscription/{id}", responses={
    200: {"description": "Inference gets successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def inferences_by_agent(id: str):
    inferences = await get_inferences_by_id_video_transcription(id)
    return inferences

# Crear inferencias para un video_transcription 
@router.post("/videotranscription/{id}", responses={
    201: {"description": "Inference created successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def test_func(id: str):
    inferences = await create_inferences_for_videotranscription(id)
    return inferences

# transcription progress by client
@router.get("/client/{id}/progress", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_transcriptions_progress(id:int):
    progress = await get_completed_tasks_count(id)
    return progress

# crea la transcripcion recibiendo el archivo del Video
@router.post("/video", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def upload_video_file(video: Optional[UploadFile] = None):
    print('route video')
    if not video:
        return {"message": "No video file provided"}

    # Generar un ID único para el video
    video_id = str(uuid.uuid4())

    # Guardar el video en el sistema de archivos
    destination = await save_video(video, video_id)

    transcription = await getTranscriptionVideo(destination)
    
    return { 
        "text": transcription,
        "idVideo": video_id
    }
