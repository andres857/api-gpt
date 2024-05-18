import whisper
from whisper.utils import get_writer
import json

async def getTranscriptionVideo(path_video: str):
    model = whisper.load_model("base")
    result = model.transcribe(path_video)

    # Convertir el resultado a un diccionario
    transcription_dict = {
        "text": result["text"],
        "language": result["language"],
    }

    # Convertir el diccionario a JSON
    transcription_video = json.dumps(transcription_dict["text"], ensure_ascii=False)
    return transcription_video


    # async def getTranscriptionVideo(path_video: str):
    #     model = whisper.load_model("base")
    #     audio = path_video
    #     result = model.transcribe(audio)
    #     output_directory = "./"


    #     # Save as a TXT file without any line breaks
    #     with open("transcription.txt", "w", encoding="utf-8") as txt:
    #         txt.write(result["text"])

    #     # Save as a TXT file with hard line breaks
    #     txt_writer = get_writer("txt", output_directory)
    #     txt_writer(result, audio)
