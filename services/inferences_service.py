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
from datetime import datetime, timezone

db = get_database()

async def update_transcriptions_with_inference(db: AsyncIOMotorDatabase):
    transcriptions_collection = db.video_transcriptions
    inferences_collection = db.inferences

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
    inference_dict = inference.dict(exclude={"id"}, by_alias=True)
    print(f"Service INFERENCE Create: ${inference_dict}")
    try:
        result = await db.inferences.insert_one(inference_dict)
        inferences_created = await db.inferences.find_one({"_id": result.inserted_id})

        if inferences_created:
            inferences_created["_id"] = str(inferences_created["_id"])
            return inferences_created
        else:
            raise HTTPException(status_code=404, detail="Error creando la inferencia")
    
    except DuplicateKeyError as e:
        raise HTTPException(status_code=400, detail="A Inference with this ID already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating or retrieving Inference: {str(e)}")
    
# Para cada Document/registro de video_transcription, crear un registro 
# en la coleccion de inferencias y actualizar el id recien en 
# el document de video_transcription
async def create_inferences_for_videotranscription(id_video_transcription: str):
    # Para los agentes requeridos crear las inferencias requeridas
    transcription = await transcription_details(id_video_transcription)
    content_transcription = transcription["data"]["content"]["transcription"]["text"]
    
    agents = await get_all_agents()
    agent_translate_to_en = await get_agent_by_id('66b03a0304d4364a6e55d37a')
    # Delete agents que no son necesarios
    agents = [agent for agent in agents if agent['rol'] != 'Chat' and agent['rol'] != 'Resumen video IA' and agent['rol'] != 'Traductor EN']
    inferences_list = []
    for agent in agents:
        inferencia = await inference(agent['prompt'], content_transcription)
        inferencia_en = await inference(agent_translate_to_en['prompt'], inferencia["inference_text"])

        inference_item = Inference(
            text={
                "es": inferencia.get('inference_text', ''),
                "en": inferencia_en.get('inference_text', '')
            },
            task=Task(
                state=TaskState.COMPLETED,
                message="Inference created successfully"
            ),
            metadata=Metadata(
                tokens=inferencia.get('total_tokens', 0),
                completion_time=datetime.now(timezone.utc)
            )
        )
        inferences_list.append(inference_item)
    
    # Crear un objeto Inferences con todas las inferencias
    inferences_document = Inferences(
        id_video_transcription=PyObjectId(id_video_transcription),
        inferences=inferences_list,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    # Llamar a la función create con el documento completo
    result = await create(inferences_document)
    # return result
        

async def add_inference(id_video_transcription, id_inference):
    pass