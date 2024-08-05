from fastapi import APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError, BaseModel, HttpUrl
from typing import Optional
from utils import save_video, save_video_from_url, delete_video
from services.transcription_service import  create, getTranscriptionVideoFromUrl, list_videos_by_id_client, update_status_transcription_by_id_content,get_completed_tasks_count, transcription_details
from schemas.video_transcription import VideoTranscription
import uuid
from services.inferences_service import create_inferences_for_videotranscription

router = APIRouter(
    prefix='/inference',
    tags=['inference']
)


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

# transcription progress by client
@router.get("/testing/{id}", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def test_func(id: str):
    progress = await create_inferences_for_videotranscription(id)
    return progress
    # print('hello')

# obtener informacion de una inferencia
@router.get("/{id}", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_transcription_info(id:str):
    transcription = await transcription_details(id)
    return transcription