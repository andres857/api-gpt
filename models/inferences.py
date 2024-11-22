inferences_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["inferences"],
        "properties": {
            "_id": {"bsonType": "objectId"},
            "id_video_transcription": {"bsonType": "objectId"},
            "inferences": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": [ "id_agent", "rol","text" ],
                    "properties": {
                        "id_agent": {"bsonType": "objectId"},
                        "rol": {"bsonType": "string"},
                        "text": {
                            "bsonType": "object",
                            "properties": {
                                "es": {"bsonType": "string"},
                                "en": {"bsonType": "string"}
                            },
                            "additionalProperties": False
                        },
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
                            "bsonType": "object",
                            "properties": {
                                "role": {"bsonType": "string"},
                                "model": {"bsonType": "string"},
                                "finish_reason": {"bsonType": "string"},                                
                                "total_tokens": {"bsonType": "int"},
                                "completion_tokens": {"bsonType": "int"},
                                "prompt_tokens": {"bsonType": "int"},
                                "completion_time": {"bsonType": "date"}
                            }
                        }
                    }
                }
            },
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"}
        }
    }
}