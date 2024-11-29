from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import agent, transcription, inference, chat, client
from routes.mzg import clients
from db import get_db_connection_myzonego, initialize_db, create_unique_index

app = FastAPI(debug=True)
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup
#     print("Starting functions...")
#     await initialize_db()
#     await create_unique_index()
#     yield

# app = FastAPI(debug=True, lifespan=lifespan)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde este origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# db = connect_to_database()
db_myzonego = get_db_connection_myzonego()


@app.on_event("startup")
async def startup_event():
    print("Starting functions...")
    await initialize_db()
    await create_unique_index()
    print("Initialization complete")
    
# @app.on_event("startup")
# async def startup_event():
#     await initialize_db()
#     await create_unique_index()

app.include_router(agent.router)
app.include_router(inference.router)
app.include_router(transcription.router)
app.include_router(chat.router)
app.include_router(client.router)


# routes myzonego
app.include_router(clients.router)
