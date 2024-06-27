from motor.motor_asyncio import AsyncIOMotorDatabase
import whisper, json
from db import get_database
from models.video import transcription_model
from utils import JSONEncoder
from bson import ObjectId
from whisper.utils import get_writer
from ia.inference import inference 
from services.agent_service import get_agent_by_id
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError



db = get_database()

# Se usa el agente transcriptor para mejorar el texto obtenido del video
async def getInferenceIA( text:str ):
    agent = get_agent_by_id('664aad0249069de0f6070f48')
    inferencia = await inference(agent['prompt'], text)
    return {
        "inference": inferencia,
    }

async def getTranscriptionVideo(path_video: str):
    model = whisper.load_model("base")
    result = model.transcribe(path_video)

    # Convertir el resultado a un diccionario
    transcription_dict = {
        "text": result["text"],
        "language": result["language"],
    }
    # Convertir el diccionario a JSON
    transcription = json.dumps(transcription_dict["text"], ensure_ascii=False)
    inference_video = await getInferenceIA(transcription)

    return inference_video

async def create(video):
    video_dict = video.dict()
    try:
        result = await db.transcriptions.insert_one(video_dict)
        created_video = await db.transcriptions.find_one({"_id": result.inserted_id})

        if created_video:
            created_video["_id"] = str(created_video["_id"])
            return created_video
        else:
            raise HTTPException(status_code=404, detail="Created video not found")
    
    except DuplicateKeyError as e:
        raise HTTPException(status_code=400, detail="A video with this ID already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating or retrieving video: {str(e)}")

async def list_videos():
    videos = []
    cursor = db.transcriptions.find()
    async for video in cursor:
        video["_id"] = str(video["_id"])
        videos.append(video)
    return videos

# async def create(video):
#     video_dict = video.dict(exclude={"id"}, by_alias=True)
#     result = db.transcriptions.insert_one(video_dict)
#     if result.inserted_id:
#         created_video = db.transcriptions.find_one({"_id": result.inserted_id})
#         # Convertir ObjectId a string
#         created_video["_id"] = str(created_video["_id"])
#         return created_video
#     else:
#         raise Exception("Failed to create video")

# async def list_videos(skip: int = 0, limit: int = 10):
#     videos = []
#     cursor = db.transcriptions.find().skip(skip).limit(limit)
    
#     for doc in cursor:
#         # Convertir ObjectId a string
#         doc["_id"] = str(doc["_id"])
#         videos.append(doc)
#     return videos