from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import os
from typing import Optional
from urllib.parse import quote_plus

client: Optional[AsyncIOMotorClient] = None
database = None

# Configuración de la conexión
DB_USERNAME = "desarrollo"
DB_PASSWORD = "ppvBUKihdqYNWsA7R"
DB_HOST = "mongodb"
DB_PORT = "27017"
DB_NAME = "inferences_private_zones"
AUTH_SOURCE = "admin"

DB_URI = f"mongodb://{quote_plus(DB_USERNAME)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource={AUTH_SOURCE}"

async def initialize_db():
    """Inicializa la conexión a MongoDB de forma asíncrona"""
    global client, database
    try:
        # Inicializar el cliente con opciones adicionales de configuración
        client = AsyncIOMotorClient(
            DB_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
            maxPoolSize=50
        )        
        database = client[DB_NAME]
        # Verificar la conexión y autenticación
        try:
            await client.admin.command('ping')
            print("[MONGO - DB] Conexión exitosa al servidor")
            
            # Verificar autenticación intentando una operación
            await database.list_collection_names()
            print("[MONGO - DB] Autenticación exitosa")
            
            # Listar las colecciones disponibles
            collections = await database.list_collection_names()
            print(f"[MONGO - DB] Colecciones disponibles: {collections}")
            
            return database

        except OperationFailure as e:
            if "Authentication failed" in str(e):
                print("[MONGO - DB] Error de autenticación. Verifica usuario y contraseña.")
            else:
                print(f"[MONGO - DB] Error de operación: {str(e)}")
            raise

    except ServerSelectionTimeoutError as e:
        print("[MONGO - DB] No se pudo conectar a MongoDB. Verifica que el servidor esté activo.")
        print(f"[MONGO - DB] Error: {str(e)}")
        raise
    except Exception as e:
        print(f"[MONGO - DB] Error inesperado: {str(e)}")
        raise

async def get_database():
    global database
    if database is None:
        database = await initialize_db()
    return database

async def create_unique_index():
    db = await get_database()
    await db.video_transcriptions.create_index("id_mzg_content", unique=True)

def get_db_connection_myzonego():
    database_url = f'mysql+mysqlconnector://{os.environ.get("DB_USERNAME")}:{os.environ.get("DB_PASSWORD")}@{"192.168.0.102"}:{3307}/{os.environ.get("DB_DATABASE")}'
    engine = create_engine(database_url)    
    return engine
