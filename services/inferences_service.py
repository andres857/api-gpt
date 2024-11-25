from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from typing import List
from db import get_database
from schemas.inferences import PyObjectId, Inferences, Inference, Task, Metadata, TaskState
from services.agent_service import get_all_agents, get_agent_by_id
from ia.inference import inference
from services.transcription_service import transcription_details
from services.transcription_service import get_video_trancriptions_collection
from datetime import datetime, timezone

async def get_inferences_collection():
    db = await get_database()
    return db.inferences

async def update_transcriptions_with_inference(db: AsyncIOMotorDatabase):
    transcriptions_collection = await get_video_trancriptions_collection()
    inferences_collection = await get_inferences_collection()

    async def process_batch(batch: List[dict]):
        for transcription in batch:
            try:
                # Crear nuevo documento de inferencia
                new_inference = {"agents": []}
                result = await inferences_collection.insert_one(new_inference)
                new_inference_id = result.inserted_id

                # Actualizar el documento de transcripción
                await transcriptions_collection.update_one(
                    {"_id": transcription["_id"]},
                    {"$set": {"inference_id": new_inference_id}}
                )

                print(f"Updated transcription {transcription['_id']} with inference {new_inference_id}")
            except Exception as e:
                print(f"Error processing transcription {transcription['_id']}: {str(e)}")

    batch_size = 100
    cursor = transcriptions_collection.find({"inference_id": {"$exists": False}})
    
    batch = []
    async for transcription in cursor:
        batch.append(transcription)
        await process_batch(batch)

    # Procesar el último lote si queda alguno
    if batch:
        await process_batch(batch)

    print("Proceso completado")

async def create(inference):
    print(f"Service INFERENCE Create", inference)
    inferences_collection = await get_inferences_collection()
    await inferences_collection.create_index("id_video_transcription", unique=True)
    inference_dict = inference.dict(by_alias=True)

    print(f"Service INFERENCE Create: ${inference_dict}")
    try:
        result = await inferences_collection.insert_one(inference_dict)
        inferences_created = await inferences_collection.find_one({"_id": result.inserted_id})
        print("service CREATED INFERENCES",inferences_created)
        if inferences_created:
            return Inferences.model_validate(inferences_created)
        else:
            raise HTTPException(status_code=404, detail="Error creando la inferencia")
    
    except DuplicateKeyError as e:
        raise HTTPException(status_code=400, detail="A Inference with this ID already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating or retrieving Inference: {str(e)}")
    
# Crea las inferencias iniciales para un video_transcription
async def create_inferences_for_videotranscription(id_video_transcription: str):
    inferences_list = []

    transcription = await transcription_details(id_video_transcription)
    content_transcription = transcription["data"]["content"]["transcription"]["text"]
    
    agents = await get_all_agents()
    agent_translate_to_en = await get_agent_by_id('66b03a0304d4364a6e55d37a')
    
    print('here agent', agent_translate_to_en)
    agents = [agent for agent in agents if agent['rol'] != 'Chat' and agent['rol'] and agent['rol'] != 'Traductor EN'] # Delete agents que no son necesarios

    for agent in agents:
        inferencia = await inference(agent['prompt'], content_transcription)
        inferencia_en = await inference(agent_translate_to_en['prompt'], inferencia["inference_text"])
        
        rol_agent= agent['rol']
        agent_id_used = str(agent["_id"])

        inference_item = Inference(
            id_agent= PyObjectId(agent_id_used),
            rol= rol_agent,
            text={
                "es": inferencia.get('inference_text', ''),
                "en": inferencia_en.get('inference_text', '')
            },
            task=Task(
                state=TaskState.COMPLETED,
                message="Inference created successfully"
            ),
            metadata=Metadata(
                role= inferencia.get('role', 0),
                model= inferencia.get('model',0),
                finish_reason = inferencia.get('finish_reason',0),
                total_tokens=inferencia.get('total_tokens', 0),
                completion_tokens=inferencia.get('completion_tokens', 0),
                prompt_tokens=inferencia.get('prompt_tokens', 0),
                completion_time=datetime.now(timezone.utc)
            )
        )
        inferences_list.append(inference_item)
    
    # Crear un objeto Inferences con todas las inferencias
    inferences_document = Inferences(
        id_video_transcription= PyObjectId(id_video_transcription),
        inferences=inferences_list,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    # Llamar a la función create con el documento completo
    result = await create(inferences_document)

    return {
        "status": "success",
        "data": result 
    }

# retorna todas la inferencias de un video_transcription
async def get_inferences_by_id_video_transcription(id):
    inferences = await get_inferences_collection()
    doc = await inferences.find_one({"id_video_transcription": ObjectId(id)})
    print("list FUNCTION", doc)
    if doc:
        return Inferences.model_validate(doc)
    return None

# retorna la inferencia Acortada para el chat
async def get_inference_chat_by_id_video_transcription(id):
    inferences = await get_inferences_collection()
    doc = await inferences.find_one({"id_video_transcription": ObjectId(id)})
    if doc:
        chat_inference = next((inference for inference in doc.get('inferences', []) if inference.get('rol') == 'Resumen video IA'), None)
        message_es = chat_inference["text"]["es"]
        return message_es
    return None

async def add_inference(id_video_transcription, id_inference):
    pass

# retorna los tokens usados para una transcripcion de video 
async def used_tokens(id_video_transcription):
    inferences = await get_inferences_collection()
    doc = await inferences.find_one({"id_video_transcription": ObjectId(id_video_transcription)})
    if doc:
        total_tokens = 0
        inferences = doc["inferences"]
        for inference in inferences:
            tokens = inference['metadata']["total_tokens"]
            total_tokens += tokens 
        return total_tokens
    return None

# retorna los tokens usados para una transcripcion de video 
async def used_tokens_by_client(id_client):
    inferences = await get_inferences_collection()
    video_transcriptions = await get_video_trancriptions_collection()

    video_transcriptions_cursor = video_transcriptions.find({"id_mzg_customer": int(id_client)})
    total_tokens = 0
    total_tokens_sent = 0
    total_tokens_generated = 0
    async for video_transcriptor in video_transcriptions_cursor:
        doc = await inferences.find_one({"id_video_transcription": video_transcriptor["_id"]})
        if doc:
            inferences = doc["inferences"]
            for inference in inferences:
                tokens = inference['metadata']["total_tokens"]
                tokens_sent = inference['metadata']["prompt_tokens"]
                tokens_generated = inference['metadata']["completion_tokens"]
                total_tokens += tokens
                total_tokens_sent += tokens_sent
                total_tokens_generated += tokens_generated
    cost_prompt_tokens = round(total_tokens_sent / 1000 * 0.0005, 2)
    cost_completion_tokens = round(total_tokens_generated / 1000 * 0.0015, 2)
    cost_total_tokens = round (cost_prompt_tokens + cost_completion_tokens, 2)

    return total_tokens, total_tokens_sent, total_tokens_generated, cost_prompt_tokens, cost_completion_tokens, cost_total_tokens