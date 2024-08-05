inferences_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["inferences"],
        "properties": {
            "inferences": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": [ "text" ],
                    "properties": {
                        "id_video_transcription": {"bsonType": "objectId"},
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
                                "tokens": {"bsonType": "int"},
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