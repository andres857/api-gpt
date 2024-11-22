from motor.motor_asyncio import AsyncIOMotorDatabase
import whisper, json
from db import get_database
from models.video_transcription import video_transcription_model
from utils import save_video_from_url, delete_video
from bson import ObjectId
from whisper.utils import get_writer
from ia.inference import inference_chat, inference_claude_chat
from services.agent_service import get_agent_by_id
from services.inferences_service import get_inference_chat_by_id_video_transcription
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from schemas.chat import ChatRequest
import json

db = get_database()

# Obtener las transcripciones guardadas del club
# return un STRING con las transcriptions 
async def get_transcriptions_by_id_club( id: int):
    separador = "\n\n===== SIGUIENTE TRANSCRIPCION DE VIDEO =====\n\n"
    videos_transcriptions = ""
    cursor = db.video_transcriptions.find({"id_mzg_club":id})
    async for video_transcription in cursor:
        video_transcription["_id"] = str(video_transcription["_id"])
        if (video_transcription["transcription"]["text"] != None):
            videos_transcriptions += video_transcription["transcription"]["text"] + separador
    # print(videos_transcriptions)
    return videos_transcriptions

async def get_resumen_transcription_IA_by_id_club( id: int):
    separador = "\n\n===== SIGUIENTE TRANSCRIPCION DE VIDEO =====\n\n"
    text_transcriptions = ""
    cursor = db.video_transcriptions.find({"id_mzg_club":id})
    async for video_transcription in cursor:
        video_transcription["_id"] = str(video_transcription["_id"])
        if (video_transcription["transcription"]["text"] != None):
            messages = await get_inference_chat_by_id_video_transcription(video_transcription["_id"])
            text_transcriptions += messages + separador
    # print(videos_transcriptions)
    return text_transcriptions

# convertir el contexto del chat en un string schema for GPT
async def get_context_chat_messages(chat: ChatRequest):
    result = ""
    for message in chat.context.messages:
        # print(message)
        result += f"{message.role.upper()}: {message.content}\n\n"
    # print (result)
    return result.strip()

# convertir el contexto del chat en un string schema for GPT
async def get_context_chat_messages_for_claude(chat):
    result = chat.dict()
    messages = result.get("messages")
    return messages

#Usar la funcion de inferencia 
async def chat_agent_gpt(idClub, chat):
    # transcriptions = await get_transcriptions_by_id_club(idClub) # Toda la transcription
    transcriptions = await get_resumen_transcription_IA_by_id_club(idClub) # Resumen del contenido con IA
    context_chat = await get_context_chat_messages(chat)
    agent = await get_agent_by_id('6697e1e946faf435426a412f')#Obtiene el agente del chat
    separador_inicio_transcriptions = "\n\n===== INICIO DE LAS TRANSCRIPCIONES DE VIDEO =====\n\n"
    
    promt_system = agent['prompt'] + separador_inicio_transcriptions + transcriptions

    inferencia = await inference_chat(promt_system, context_chat)
    return (inferencia)

#Usar la funcion de inferencia 
async def chat_agent_claude_model(idClub, chat):
    # transcriptions = await get_transcriptions_by_id_club(idClub) # Toda la transcription
    transcriptions = await get_resumen_transcription_IA_by_id_club(idClub) # Resumen del contenido con IA
    context_chat = await get_context_chat_messages_for_claude(chat)
    agent = await get_agent_by_id('6697e1e946faf435426a412f')
    separador_inicio_transcriptions = "\n\n===== INICIO DE LAS TRANSCRIPCIONES DE VIDEO =====\n\n"
    
    promt_system = agent['prompt'] + separador_inicio_transcriptions + transcriptions
    # print(promt_system)

    inferencia = await inference_claude_chat(promt_system, context_chat)
    return (inferencia)

# Se usa el agente transcriptor para mejorar el texto obtenido del video
async def getInferenceIA( text:str ):
    agent = await get_agent_by_id('664aad0249069de0f6070f48')
    print(f"[ SERVICE INFERENCE AGENT USED ] - {agent['prompt']}")
    inferencia = await inference_chat(agent['prompt'], text)
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

