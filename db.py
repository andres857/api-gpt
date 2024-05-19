from pymongo import MongoClient
import os

def connect_to_database():
    # URI de conexión
    
    uri = os.environ.get('DB_URI')

    # Crear una instancia de MongoClient
    client = MongoClient(uri)

    # Obtener una referencia a la base de datos
    db = client["test_database"]

    return db
