from fastapi import APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from utils import save_video
from services.transcription_service import getTranscriptionVideo
from services.agent_service import get_all_agents
from ia.inference import inference 
import uuid

router = APIRouter(
    prefix='/transcription',
    tags=['transcription']
)

@router.post("/video", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})

async def upload_video(video: Optional[UploadFile] = None):

    if not video:
        return {"message": "No video file provided"}

    # Generar un ID único para el video
    video_id = str(uuid.uuid4())

    # Guardar el video en el sistema de archivos
    destination = await save_video(video, video_id)

    transcriptionVideo = await getTranscriptionVideo(destination)
    # Aquí puedes agregar la lógica para procesar el video y generar la transcripción
    # ...

    return { 
        "text": transcriptionVideo,
    }