from fastapi import APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError, BaseModel, HttpUrl
from typing import Optional
from utils import save_video, save_video_from_url, delete_video
from services.transcription_service import  create, list_videos, getTranscriptionVideo, list_videos_by_id_client, update_status_transcription_by_id_content
from schemas.video import Video
import uuid

router = APIRouter(
    prefix='/transcriptions',
    tags=['transcription']
)

# crea el document en la collection para el video
@router.post("/video/record", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def create_record(video: Video):
    created_video = await create(video)
    return Video(**created_video)

# crea la transcription del video con una URL
@router.put("/video/url", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def upload_video_from_url(video: Video):
    await update_status_transcription_by_id_content(video.id_mzg_content, video.transcription.task.state)
    path = await save_video_from_url(video.video_url)
    transcription = await getTranscriptionVideo(path, video.id_mzg_content)
    
    # # Save transcription in colection Videos.
    await delete_video(path)
    # return { 
    #     transcription
    # }
    return Video(**transcription)

# list registros de un client
@router.get("/client/{id}", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_transcriptions_status_for_client(id:int):
    lists_videos = await list_videos_by_id_client(id)
    return lists_videos

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
