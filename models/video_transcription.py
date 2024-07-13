# Definir el esquema JSON para la colección de videos
video_transcription_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["id_mzg_customer", "id_mzg_club", "id_mzg_content", "video_url", "transcription"],
        "properties": {
            "id_mzg_customer": {"bsonType": "int"},
            "id_mzg_club": {"bsonType": "int"},
            "id_mzg_content": {"bsonType": "int"},
            "video_url": {"bsonType": "string"},
            "transcription": {
                "bsonType": "object",
                "required": ["task"],
                "properties": {
                    "text": {"bsonType": ["string", "null"]},
                    "task": {
                        "bsonType": "object",
                        "required": ["state", "message"],
                        "properties": {
                            "state": {
                                "bsonType": "string",
                                "enum": ["pending", "in_progress", "completed", "error"]
                            },
                            "message": {"bsonType": "string"},
                        }
                    },
                    "metadata": {
                        "bsonType": ["object","null"],
                        "properties": {
                            "characters": {"bsonType": "int"},
                            "words": {"bsonType": "int"},
                            "total_tokens": {"bsonType": "int"},
                            "completion_tokens": {"bsonType": "int"},
                            "prompt_tokens": {"bsonType": "int"},

                        }
                    }
                }
            },
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"}
        }
    }
}

