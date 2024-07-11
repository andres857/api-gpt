from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from pymongo.errors import ServerSelectionTimeoutError
import os

# client = AsyncIOMotorClient(os.environ.get('DB_URI'))
# database = client.get_database("test_database")

client = None
database = None

def initialize_db():
    global client, database
    try:
        client = AsyncIOMotorClient(os.environ.get('DB_URI'), serverSelectionTimeoutMS=5000)
        database = client.get_database("test_database")
        # Verifica la conexión
        client.server_info()
        print("Conexión a MongoDB establecida exitosamente.")
    except ServerSelectionTimeoutError:
        print("No se pudo conectar a MongoDB. Verifica la URI de conexión y la red.")

def get_database():
    if database is None:
        initialize_db()
    return database

async def create_unique_index():
    db = get_database()
    await db.video_transcriptions.create_index("id_mzg_content", unique=True)

def get_db_connection_myzonego():
    database_url = f'mysql+mysqlconnector://{os.environ.get("DB_USERNAME")}:{os.environ.get("DB_PASSWORD")}@{"192.168.0.102"}:{3307}/{os.environ.get("DB_DATABASE")}'
    engine = create_engine(database_url)    
    return engine
