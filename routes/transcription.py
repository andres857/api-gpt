from fastapi import APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError, BaseModel, HttpUrl
from typing import Optional
from utils import save_video, save_video_from_url, delete_video
from services.transcription_service import  create, getTranscriptionVideoFromUrl, list_videos_by_id_client, update_status_transcription_by_id_content,get_completed_tasks_count, transcription_details, get_stats_video_transcription
from schemas.video_transcription import VideoTranscription
import uuid

router = APIRouter(
    prefix='/transcriptions',
    tags=['transcription']
)

# crea el document en la collection para el video
@router.post("/video/create-record", responses={
    200: {"description": "record created successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def create_record(video: VideoTranscription):
    created_video = await create(video)
    return VideoTranscription(**created_video)

# crea la transcription del video con una URL
@router.put("/video/url", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def upload_video_from_url(video: VideoTranscription):
    await update_status_transcription_by_id_content(video.id_mzg_content, video.transcription.task.state)

    transcription = await getTranscriptionVideoFromUrl(video.video_url, video.id_mzg_content)
    print (transcription)
    if transcription["status"] == "success":
        return JSONResponse(status_code=201, content=transcription)
    elif transcription["status"] == "not_found":
        return JSONResponse(status_code=404, content=transcription)
    else:
        return JSONResponse(
            status_code=500, 
            content={"detail": transcription.get("message", "An error occurred")}
        )

# obtener informacion de una transcripcion
@router.get("/{id}", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_transcription_info(id:str):
    transcription = await transcription_details(id)
    return transcription

# list las transcripciones de un client
@router.get("/client/{id}", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def list_videos(id:int):
    lists_videos = await list_videos_by_id_client(id)
    return lists_videos

# obtener informacion de una transcripcion
@router.get("/client/{id}/tokens", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_stats(id:int):
    stats = await get_stats_video_transcription(id)
    return stats

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
