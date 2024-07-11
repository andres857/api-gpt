from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import agent, transcription, inference
from routes.mzg import clients
from db import get_db_connection_myzonego, initialize_db, create_unique_index

app = FastAPI(debug=True)

# db = connect_to_database()
db_myzonego = get_db_connection_myzonego()

@app.on_event("startup")
async def startup_event():
    initialize_db()
    await create_unique_index()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde este origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(agent.router)
app.include_router(inference.router)
app.include_router(transcription.router)
# routes myzonego
app.include_router(clients.router)
