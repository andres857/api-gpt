import json, os
from bson import ObjectId

#Encode las respuesta de la base de datos cursor to json
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)
    
# Función para guardar el video en el sistema de archivos
async def save_video(video_file, video_id: str):
    # Obtener la extensión del archivo
    extension = video_file.filename.split('.')[-1]

    current_directory = os.path.abspath(os.path.dirname(__file__))
    # root_directory = os.path.dirname(current_directory)

    videos_directory = os.path.join(current_directory, "temp-files")

    # Construir la ruta de destino del archivo
    destination = os.path.join(videos_directory, f"{video_id}.{extension}")
    print ("current_directory",current_directory)
    # print ("root_directory",root_directory)
    print("destination", destination)

    # Escribir el contenido del archivo en el destino
    with open(destination, "wb") as buffer:
        contents = await video_file.read()
        buffer.write(contents)
    return destination