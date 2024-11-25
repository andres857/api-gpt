from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from typing import List
from db import get_database
from schemas.clients import Customer, CustomerCreate, CustomerUpdate, InferenceData
from datetime import datetime, timezone
from pydantic import BaseModel

class InferenceResponse(BaseModel):
    inference: InferenceData

# db = get_database()

async def get_customers_collection():
    db = await get_database()
    return db.customers

async def create_customer( customer: Customer):
    customers = await get_customers_collection()
    # Crear un índice único en id_customer si aún no existe
    await customers.create_index("id_customer", unique=True)
    
    # Convertir el objeto Customer a un diccionario
    customer_dict = customer.model_dump(by_alias=True)

    print(f"Service CUSTOMER Create: ${customer_dict}")
    try:
        # Insertar el cliente en la base de datos
        result = await customers.insert_one(customer_dict)
        
        # Recuperar el cliente recién creado
        customer_created = await customers.find_one({"_id": result.inserted_id})
        print("Service CREATED CUSTOMER", customer_created)
        
        if customer_created:
            # Validar y retornar el cliente creado
            return Customer(**customer_created)
        else:
            raise HTTPException(status_code=404, detail="Error creating the customer")
    
    except DuplicateKeyError as e:
        raise HTTPException(status_code=400, detail="A Customer with this ID already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating or retrieving Customer: {str(e)}")

#retorna la informacion de un cliente
async def get_client(id):
    customers = await get_customers_collection()
    doc = await customers.find_one({"id_customer": int(id)})
    if doc:
        return Customer(**doc)
    raise HTTPException(status_code=404, detail="Customer not found")

# retorna los tokens de files de un client, id_client
async def get_tokens_files(id):
    customers = await get_customers_collection()
    doc = await customers.find_one({"id_customer": int(id)})
    if doc:
        client = Customer(**doc)
        return InferenceResponse(inference=client.inference)
    raise HTTPException(status_code=404, detail="Customer not found")

# retorna los tokens de chat de un client, id_client
async def get_tokens_chat(id):
    customers = await get_customers_collection()
    doc = await customers.find_one({"id_customer": int(id)})
    if doc:
        client = Customer(**doc)
        print(client)
        return InferenceResponse(inference=client.inference_chat)
    raise HTTPException(status_code=404, detail="Customer not found")

async def update_customer_chat(id_customer: int, update_data: InferenceData):
    # Preparar la operación de actualización
    customers = await get_customers_collection()
    update_operation = {
        "$inc": {
            "inference_chat.tokens.prompt_tokens": update_data.inference_chat.tokens.prompt_tokens,
            "inference_chat.tokens.total_tokens": update_data.inference_chat.tokens.total_tokens,
            "inference_chat.tokens.completion_tokens": update_data.inference_chat.tokens.completion_tokens,
            "inference_chat.cost.prompt_tokens": update_data.inference_chat.cost.prompt_tokens,
            "inference_chat.cost.total_tokens": update_data.inference_chat.cost.total_tokens,
            "inference_chat.cost.completion_tokens": update_data.inference_chat.cost.completion_tokens,
        },
        "$set": {
            "inference_chat.limit": update_data.inference_chat.limit
        }
    }

    # Actualizar el documento en la base de datos
    result = await customers.update_one(
        {"id_customer": id_customer},
        update_operation
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Recuperar el cliente actualizado
    updated_customer = await customers.find_one({"id_customer": id_customer})
    
    if updated_customer:
        # Convertir ObjectId a str para las transcripciones antes de la validación
        if 'transcriptions' in updated_customer:
            updated_customer['transcriptions'] = [str(t) for t in updated_customer['transcriptions']]
        return Customer(**updated_customer)
    else:
        raise HTTPException(status_code=404, detail="Error retrieving updated customer")

async def update_customer_files( id_customer: int, update_data: InferenceData):
    customers = await get_customers_collection()
    # Convertir los datos de actualización a un diccionario
    update_operation = {
        "$inc": {
            "inference.tokens.prompt_tokens": update_data.inference.tokens.prompt_tokens,
            "inference.tokens.total_tokens": update_data.inference.tokens.total_tokens,
            "inference.tokens.completion_tokens": update_data.inference.tokens.completion_tokens,
            "inference.cost.prompt_tokens": update_data.inference.cost.prompt_tokens,
            "inference.cost.total_tokens": update_data.inference.cost.total_tokens,
            "inference.cost.completion_tokens": update_data.inference.cost.completion_tokens,
        },
        "$set": {
            "inference.limit": update_data.inference.limit
        }
    }

    # Actualizar el documento en la base de datos
    result = await customers.update_one(
        {"id_customer": id_customer},
        update_operation
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Recuperar el cliente actualizado
    updated_customer = await customers.find_one({"id_customer": id_customer})
    
    if updated_customer:
        # Convertir ObjectId a str para las transcripciones antes de la validación
        if 'transcriptions' in updated_customer:
            updated_customer['transcriptions'] = [str(t) for t in updated_customer['transcriptions']]
        return Customer(**updated_customer)
    else:
        raise HTTPException(status_code=404, detail="Error retrieving updated customer")