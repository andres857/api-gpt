# Definir el esquema JSON para la colección de videos
video_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["Transcripcion"],
        "properties": {
            "id_videomzg": {"bsonType": "int"},
            "name": {"bsonType": "string"},
            "grupo": {"bsonType": "string"},
            "Zona": {"bsonType": "string"},
            "Transcripcion": {"bsonType": "string"}
        }
    }
}
# from pymongo import MongoClient

# # URI de conexión
# uri = "mongodb+srv://aguerrero:mB3xSu5IBdf1bfi6@cluster0.0axlxff.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Crear una instancia de MongoClient
# client = MongoClient(uri)

# try:
#     # Obtener una referencia a una nueva base de datos
#     db = client["test_database"]

#     # Definir el esquema JSON para la colección de videos
#     video_schema = {
#         "$jsonSchema": {
#             "bsonType": "object",
#             "required": ["Transcripcion"],
#             "properties": {
#                 "id_videomzg": {"bsonType": "int"},
#                 "name": {"bsonType": "string"},
#                 "grupo": {"bsonType": "string"},
#                 "Zona": {"bsonType": "string"},
#                 "Transcripcion": {"bsonType": "string"}
#             }
#         }
#     }

#     # Definir el esquema JSON
#     agent_schema = {
#         "$jsonSchema": {
#             "bsonType": "object",
#             "required": ["rol", "prompt"],
#             "properties": {
#                 "rol": {"bsonType": "string"},
#                 "prompt": {"bsonType": "string"},
#                 "descripcion": {"bsonType": "string"},
#             },
#         }
#     }

#     # Crear una nueva colección con el esquema definido
#     videos = db.create_collection("videos", validator=video_schema)
#     # Crear una nueva colección con el esquema definido
#     agents = db.create_collection("agentes", validator=agent_schema)


#     # Insertar un documento que cumpla con el esquema
#     video = {
#         "id_videomzg": 1,
#         "name": "Video1",
#         "grupo": "Grupo1",
#         "Zona": "Zona1",
#         "Transcripcion": "Esta es la transcripción del video."
#     }

#     videos.insert_one(video)

#     # Insertar un documento que cumpla con el esquema
#     agent = {
#         "rol": "Evaluador",
#         "prompt": "Eres un experto en evaluar contenido. Tu tarea es hacer 3 preguntas de evaluación basadas en el contenido que se te proporcione.",
#         "descripcion": "Este agente genera preguntas de evaluación para medir la comprensión del contenido."
#     }

#     agents.insert_one(agent)
# except Exception as e:
#     print(f"Error al conectar a MongoDB: {e}")
# finally:
#     # Cerrar la conexión
#     client.close()
