import json, os, subprocess, uuid, requests
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

async def save_video_from_url(url_video):
    print('Download from URL....')
    try:
        response = requests.get(url_video, stream=True)
        response.raise_for_status()

        filename = url_video.split("/")[-1]

        current_directory = os.path.abspath(os.path.dirname(__file__))
        videos_directory = os.path.join(current_directory, "temp-files")
        # Construir la ruta de destino del archivo
        destination = os.path.join(videos_directory, filename)

        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Sucess al descargar el video")
        return destination;

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el video: {e}")

async def delete_video(filename: str):
    try:
        current_directory = os.path.abspath(os.path.dirname(__file__))
        videos_directory = os.path.join(current_directory, "temp-files")
        file_path = os.path.join(videos_directory, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": f"Video {filename} eliminado exitosamente"}
        else:
            print(f"Error - Video no encontrado")

    except Exception as e:
                print(f"Error al eliminar el video: {str(e)}")

