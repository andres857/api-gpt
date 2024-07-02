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

async def getTranscriptionVideo(path_video: str, id_content:int):
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
    
    # update state and text in db
    updateDocument = await update_transcription_by_id_content(id_content, 'success', inference_video)

    return updateDocument

async def create(video):
    video_dict = video.dict(exclude={"id"}, by_alias=True)
    print(f"Service created Service: ${video_dict}")
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

async def list_videos_by_id_client(id):
    videos = []
    cursor = db.transcriptions.find({"id_mzg_customer":id})
    async for video in cursor:
        video["_id"] = str(video["_id"])
        videos.append(video)
    return videos

async def update_status_transcription_by_id_content(id, status):
    print('service')
    print(id,status)
    filter = {"id_mzg_content": id}
    update = {
        "$set": {
            "transcription.task.state": status
        }
    }
    result = await db.transcriptions.update_one(filter, update)
    # Verificar si se actualizó algún documento
    if result.modified_count > 0:
        return {"message": f"Estado actualizado para id_mzg_content: {id}"}
    else:
        return {"message": f"No se encontró documento para id_mzg_content: {id}"}


async def update_transcription_by_id_content(id, status, inferencia):
    filter = {"id_mzg_content": id}
    update = {
        "$set": {
            "transcription.task.state": status,
            "transcription.task.text": inferencia
        }
    }
    result = await db.transcriptions.update_one(filter, update)
    # Verificar si se actualizó algún documento
    if result.modified_count > 0:
        # return {"message": f"Estado actualizado para id_mzg_content: {id}"}
        return result
    else:
        return {"message": f"No se encontró documento para id_mzg_content: {id}"}