from pymongo import MongoClient

def connect_to_database():
    # URI de conexión
    uri = "mongodb+srv://aguerrero:mB3xSu5IBdf1bfi6@cluster0.0axlxff.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Crear una instancia de MongoClient
    client = MongoClient(uri)

    # Obtener una referencia a la base de datos
    db = client["test_database"]

    return db
