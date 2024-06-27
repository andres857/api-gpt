from fastapi import APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError, BaseModel, HttpUrl
from typing import Optional
from utils import save_video, save_video_from_url, delete_video
from services.transcription_service import getTranscriptionVideo, create, list_videos
from schemas.video import Video
import uuid

router = APIRouter(
    prefix='/transcriptions',
    tags=['transcription']
)

@router.post("/video/url", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def upload_video_from_url(video: Video):
    print(video)

    created_video = await create(video)
    return Video(**created_video)
    # path = await save_video_from_url(video_request.url_video)
    # transcription = await getTranscriptionVideo(path)
    # # Save transcription in colection Videos.

    # await delete_video(path)

    # return { 
    #     "text": transcription
    # }

# list registros de un client
@router.get("/video/url", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_transcriptions_status_for_client():
    lists_videos = await list_videos()
    return lists_videos

@router.post("/video", responses={
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def upload_video(video: Optional[UploadFile] = None):
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
