from motor.motor_asyncio import AsyncIOMotorDatabase
import whisper, json
from db import get_database
from models.video import transcription_model
from utils import save_video_from_url, delete_video
from bson import ObjectId
from whisper.utils import get_writer
from ia.inference import inference 
from services.agent_service import get_agent_by_id
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

db = get_database()

# Se usa el agente transcriptor para mejorar el texto obtenido del video
async def getInferenceIA( text:str ):
    agent = await get_agent_by_id('664aad0249069de0f6070f48')
    print(f"[ SERVICE INFERENCE AGENT USED ] - {agent['prompt']}")
    inferencia = await inference(agent['prompt'], text)
    print(f"[SERVICE INFERENCE result] - {inferencia}")
    return inferencia
    

async def getTranscriptionVideoFromUrl(video_url: str, id_content:int):
    try:
        model = whisper.load_model("base")
        path = await save_video_from_url(video_url)
        print(f"[SERVICE TRANSCRIPTION WHISPER path] - {path}")
        result = model.transcribe(path)
        print(f"[SERVICE TRANSCRIPTION WHISPER model] - {result}")

        # Borrar el Video
        await delete_video(path)
        
        # Convertir el resultado a un diccionario
        transcription_dict = {
            "text": result["text"],
            "language": result["language"],
        }

        # Convertir el diccionario a JSON
        transcription = json.dumps(transcription_dict["text"], ensure_ascii=False)        
        inference_video = await getInferenceIA(transcription)
        
        # Update state and text in db
        updateDocument = await update_transcription_by_id_content(id_content, 'completed','Inferencia guardarda correctamente', inference_video)
        
        return {
            "status": "success",
            "data": updateDocument
        }
    
    except Exception as e:
        # Manejar cualquier error que ocurra durante el proceso
        error_message = f"Error en la transcripción: {str(e)}"
        print(error_message)  # Para logging

        # Actualizar el documento en la base de datos con estado "error"
        try:
            updateDocument = await update_transcription_by_id_content(id_content, 'error', error_message)
            return {
                "status": "not_found",
                "data": updateDocument
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error en la transcripción y al actualizar la base de datos: {error_message}. {str(e)}"
            }

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
    print('SERVICE - ACTUALIZANDO EL ESTADO DE LA TAREA')
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


async def update_transcription_by_id_content(id, status, statusMessage, inferencia=None):
    print(f"[ SERVICE UPDATE DOCUMENT - {status}, {statusMessage}, {inferencia}]")

    filter = {"id_mzg_content": id}
    update = {
        "$set": {
            "transcription.task.state": status,
            "transcription.task.message": statusMessage
        }
    }
    if inferencia is not None:
        update["$set"]["transcription.text"] = inferencia

    try:
        result = await db.transcriptions.update_one(filter, update)

        if result.modified_count > 0:
            # El documento fue actualizado exitosamente
            updated_doc = await db.transcriptions.find_one(filter, projection={"_id": 1, "transcription.task": 1})
            if updated_doc:
                updated_doc["_id"] = str(updated_doc["_id"])
                return updated_doc
            else:
                raise HTTPException(status_code=404, detail="Document not found")
        elif result.matched_count > 0:
            # El documento fue encontrado pero no modificado
            return {"message": "Document found but not modified"}
        else:
            # No se encontró ningún documento para actualizar
            raise HTTPException(status_code=404, detail="No document found to update")
        
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"An error occurred: {str(e)}")