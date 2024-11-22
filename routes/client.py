from fastapi import APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError, BaseModel, HttpUrl
from typing import Optional
from schemas.clients import Customer, CustomerCreate, CustomerUpdate
from services.clients_service import create_customer,get_client, update_customer_chat, update_customer_files, get_tokens_files, get_tokens_chat

router = APIRouter(
    prefix='/clients',
    tags=['clients']
)

# crear un cliente con el id de myzonego
@router.post("/", responses={
    200: {"description": "client created successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def create_client(body: CustomerCreate):
    client = Customer(id_customer = body.id_customer)
    return await create_customer(client)

# Informacion del cliente con el id de myzonego
@router.get("/{id_customer}", responses={
    200: {"description": "client created successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})
async def get_client_info(id_customer:str):
    return await get_client(id_customer)

# tokens usados en los files, video_transcription etc
@router.get("/{id_customer}/tokens/files", responses={
    200: {"description": "tokens returns successfully"},
    400: {"description": "Invalid request body"},
    404: {"description": "Token not found"},
    500: {"description": "Internal server error"}
})
async def get_customer_file_tokens(id_customer:str):
    return await get_tokens_files(id_customer)

# tokens usados en los files, video_transcription etc
@router.get("/{id_customer}/tokens/chat", responses={
    200: {"description": "tokens returns successfully"},
    400: {"description": "Invalid request body"},
    404: {"description": "Token not found"},
    500: {"description": "Internal server error"}
})
async def get_customer_chat_tokens(id_customer:str):
    return await get_tokens_chat(id_customer)

# actualiza los tokens usados en los files, video_transcription etc
@router.put("/{id_customer}/tokens/files", responses={
    200: {"model": Customer, "description": "Client updated successfully"},
    400: {"description": "Invalid request body"},
    404: {"description": "Client not found"},
    500: {"description": "Internal server error"}
})
async def update_customer_file_tokens(
    id_customer: int,
    update_data: CustomerUpdate,
):
    return await update_customer_files( id_customer, update_data)

# actualiza los tokens usados en el chat
@router.put("/{id_customer}/tokens/chat", responses={
    200: {"model": Customer, "description": "Client updated successfully"},
    400: {"description": "Invalid request body"},
    404: {"description": "Client not found"},
    500: {"description": "Internal server error"}
})
async def update_customer_chat_tokens(
    id_customer: int,
    update_data: CustomerUpdate,
):
    return await update_customer_chat( id_customer, update_data)