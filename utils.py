import json, os, requests
from bson import ObjectId
from fastapi import HTTPException
import uuid

class VideoDownloadError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
    def to_dict(self):
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "status_code": self.status_code
        }

#Encode la respuesta de la base de datos MYSQL cursor to JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)
    
# Función para guardar el video en el sistema de archivos
async def save_video(video_file):
    # Obtener la extensión del archivo
    extension = video_file.filename.split('.')[-1]

    current_directory = os.path.abspath(os.path.dirname(__file__))
    # root_directory = os.path.dirname(current_directory)

    videos_directory = os.path.join(current_directory, "temp-files")

    # Construir la ruta de destino del archivo
    destination = os.path.join(videos_directory, f"{uuid.uuid4()}.{extension}")
    print ("current_directory",current_directory)
    # print ("root_directory",root_directory)
    print("destination", destination)

    # Escribir el contenido del archivo en el destino
    with open(destination, "wb") as buffer:
        contents = await video_file.read()
        buffer.write(contents)
    return destination

async def save_video_from_url(url_video):
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
        print(f"[ UTILS ] - Video Descargado Exitosamente")
        return destination
    
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el video: {e}")
        raise VideoDownloadError(f"Error al descargar el video: {str(e)}", 404)
    except IOError as e:
        print(f"Error de E/S al guardar el video: {e}")
        raise VideoDownloadError(f"Error de E/S al guardar el video: {str(e)}", 500)
    except Exception as e:
        print(f"Error inesperado: {e}")
        raise VideoDownloadError(f"Error inesperado: {str(e)}", 500)

async def delete_video(filename: str):
    try:
        current_directory = os.path.abspath(os.path.dirname(__file__))
        videos_directory = os.path.join(current_directory, "temp-files")
        file_path = os.path.join(videos_directory, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"[ UTILS ] - Video eliminado exitosamente")
        else:
            print(f"Error - Video no encontrado")

    except Exception as e:
        print(f"Error al eliminar el video: {str(e)}")

import subprocess
import json

def get_duration_ffprobe(path):
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        path
    ]
    
    resultado = subprocess.run(cmd, capture_output=True, text=True)
    datos = json.loads(resultado.stdout)
    
    duracion = float(datos['format']['duration'])
    return duracion
