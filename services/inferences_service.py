from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List
from db import get_database

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
