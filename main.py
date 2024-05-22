from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import agent, transcription, inference
from db import connect_to_database

app = FastAPI(debug=True)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde este origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

db = connect_to_database()

app.include_router(agent.router)
app.include_router(inference.router)
app.include_router(transcription.router)




















# @app.post("/document/upload", responses={
#     200: {"description": "Video uploaded successfully"},
#     400: {"description": "Invalid request body"},
#     500: {"description": "Internal server error"}
# })
# async def upload_video(video: UploadFile = File(...)):
#     """
#     Endpoint para subir un video.
    
#     Parameters:
#     - video: El archivo de video a subir.
    
#     Returns:
#     - Mensaje de éxito si el video se subió correctamente.
#     """
#     # Lógica para manejar y guardar el video en el sistema
#     pass

# @app.get("/video/transcription/{video_id}", responses={
#     200: {"description": "Transcription retrieved successfully", "model": TranscriptionResponse},
#     404: {"description": "Video not found"},
#     500: {"description": "Internal server error"}
# })
# async def get_transcription(video_id: str):
#     """
#     Endpoint para obtener la transcripción de un video.
    
#     Parameters:
#     - video_id: El ID del video del cual se desea obtener la transcripción.
    
#     Returns:
#     - La transcripción del video en formato de texto.
#     """
#     # Lógica para obtener la transcripción del video de la base de datos
#     transcription = get_transcription_from_db(video_id)
#     return TranscriptionResponse(transcription=transcription)

# @app.get("/document/transcription/{video_id}", responses={
#     200: {"description": "Transcription retrieved successfully", "model": TranscriptionResponse},
#     404: {"description": "Video not found"},
#     500: {"description": "Internal server error"}
# })
# async def get_transcription(video_id: str):