import whisper, json
from db import get_database
from utils import save_video_from_url, save_video, delete_video, get_duration_ffprobe
from bson import ObjectId
from ia.inference import inference 
from services.agent_service import get_agent_by_id
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

async def get_video_trancriptions_collection():
    db = await get_database()
    return db.video_transcriptions

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
        duracion = get_duration_ffprobe(path)
        print(f"La duración del video es: {duracion} segundos")

        await delete_video(path) # Borrar el Video

        # Convertir el resultado a un diccionario
        transcription_dict = {
            "text": result["text"],
            "language": result["language"],
        }

        # transcription = json.dumps(transcription_dict["text"], ensure_ascii=False)        
        
        updateDocument = await update_transcription_by_id_content(id_content, 'completed','Transcription video guardarda correctamente', str(transcription_dict["text"]), duracion)
        
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
    video_transcriptions = await get_video_trancriptions_collection()
    await video_transcriptions.create_index("id_mzg_content", unique=True)
    video_dict = video.dict(exclude={"id"}, by_alias=True)
    print(f"Service created Service: ${video_dict}")
    try:
        result = await video_transcriptions.insert_one(video_dict)
        created_video = await video_transcriptions.find_one({"_id": result.inserted_id})

        if created_video:
            created_video["_id"] = str(created_video["_id"])
            return created_video
        else:
            raise HTTPException(status_code=404, detail="Created video not found")
    
    except DuplicateKeyError as e:
        raise HTTPException(status_code=400, detail="A video with this ID already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating or retrieving video: {str(e)}")

async def list_videos_by_id_client(id):
    videos = []
    video_transcriptions = await get_video_trancriptions_collection()
    cursor = video_transcriptions.find({"id_mzg_customer":id})
    async for video in cursor:
        video["_id"] = str(video["_id"])
        videos.append(video)
    return videos

async def transcription_details(id):
    video_transcriptions = await get_video_trancriptions_collection()
    result = await video_transcriptions.find_one({"_id": ObjectId(id)})
    if result:
        result["_id"] = str(result["_id"])
        return {
            "status": "success",
            "data": {
                "content": result
            }
        }
    else:
        raise HTTPException(status_code=404, detail=" Video transcription Not Found")


async def transcription_details_privates_zones(id):
    video_transcriptions = await get_video_trancriptions_collection()
    print(id, 'zones')
    result = await video_transcriptions.find_one({'id_mzg_content': int(id)})
    if result:
        result["_id"] = str(result["_id"])
        return {
            "status": "success",
            "data": {
                "content": result
            }
        }
    else:
        raise HTTPException(status_code=404, detail=" Video transcription Not Found")

async def update_status_transcription_by_id_content(id, status):
    video_transcriptions = await get_video_trancriptions_collection()
    print('SERVICE - ACTUALIZANDO EL ESTADO DE LA TAREA')
    filter = {"id_mzg_content": id}
    update = {
        "$set": {
            "transcription.task.state": status
        }
    }
    result = await video_transcriptions.update_one(filter, update)
    # Verificar si se actualizó algún documento
    if result.modified_count > 0:
        return {"message": f"Estado actualizado para id_mzg_content: {id}"}
    else:
        return {"message": f"No se encontró documento para id_mzg_content: {id}"}

async def update_transcription_by_id_content(id, status, statusMessage, inferencia=None, duration_video=None):
    video_transcriptions = await get_video_trancriptions_collection()
    print(f"[ SERVICE UPDATE DOCUMENT 1 - {status}, {statusMessage}, {inferencia}, {duration_video}]")
    print(f"[ SERVICE UPDATE DOCUMENT 2 XXXXXX - {inferencia}]")

    filter = {"id_mzg_content": id}
    update = {
        "$set": {
            "transcription.task.state": status,
            "transcription.task.message": statusMessage
        }
    }
    if inferencia is not None:
        print('aquitoy')
        # characters = len(inferencia["inference_text"])
        # words = len(inferencia["inference_text"].split())
        characters = len(inferencia)
        words = len(inferencia.split())
        print("c",characters)
        print("words",words)
        update["$set"]["duration"] = duration_video
        # update["$set"]["transcription.text"] = inferencia["inference_text"]
        update["$set"]["transcription.text"] = inferencia
        update["$set"]["transcription.metadata.characters"] = characters
        update["$set"]["transcription.metadata.words"] = words
        # update["$set"]["transcription.metadata.total_tokens"] = inferencia["total_tokens"]
        # update["$set"]["transcription.metadata.completion_tokens"] = inferencia["completion_tokens"]
        # update["$set"]["transcription.metadata.prompt_tokens"] = inferencia["prompt_tokens"]

    try:
        result = await video_transcriptions.update_one(filter, update)

        if result.modified_count > 0:
            # El documento fue actualizado exitosamente
            updated_doc = await video_transcriptions.find_one(filter, projection={"_id": 1, "transcription.task": 1})
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

async def get_total_documents_by_client(id_mzg_customer):
    video_transcriptions = await get_video_trancriptions_collection()
    pipeline = [
        {
            "$match": {
                "id_mzg_customer": id_mzg_customer
            }
        },
        {
            "$count": "total"
        }
    ]
    
    try:
        result = await video_transcriptions.aggregate(pipeline).to_list(length=None)
        
        if result:
            return {
                "status": "success",
                "data": {
                    "total_documents": result[0]["total"]
                }
            }
        else:
            return {
                "status": "success",
                "data": {
                    "total_documents": 0
                }
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error en la db: {str(e)}"
        }
    
async def get_completed_tasks_count(id):
    video_transcriptions = await get_video_trancriptions_collection()
    TASK_STATES = ["completed", "error", "pending", "in_progress"]
    pipeline = [
        {
            "$match": {
                "id_mzg_customer": id,
                "transcription.task.state": {"$in": TASK_STATES }
            }
        },
        {
            "$group": {
                "_id": "$transcription.task.state",
                "count": {"$sum": 1}
            }
        }
    ]
    try:
        result = await video_transcriptions.aggregate(pipeline).to_list(length=None)
        total =  await get_total_documents_by_client(id)
        # Inicializamos todos los estados con 0
        counts = {state: 0 for state in TASK_STATES}
        
        # Actualizamos con los conteos reales
        for item in result:
            counts[item["_id"]] = item["count"]
        
        return {
            "status": "success",
            "data": {
                "total": total["data"]["total_documents"],
                "counts": counts,
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error en la db {str(e)}"
        }
    
async def getTranscriptionVideoFromVideoFile(video):
    try:
        model = whisper.load_model("base")
        path = await save_video(video)
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

        return {
            "inferencia":inference_video
        }
    
    except Exception as e:
        # Manejar cualquier error que ocurra durante el proceso
        error_message = f"Error en la transcripción: {str(e)}"
        print(error_message)  # Para logging