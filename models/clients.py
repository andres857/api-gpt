customer_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "id_customer", "state_transcription", "transcriptions", "inference", "inference_chat", "created_at", "updated_at"],
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "id_customer": {
                "bsonType": "int"
            },
            "state_transcription": {
                "bsonType": "string",
                "enum": ["pending", "in_progress", "completed"]
            },
            "transcriptions": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                }
            },
            "inference": {
                "bsonType": "object",
                "required": ["tokens", "cost", "limit"],
                "properties": {
                    "tokens": {
                        "bsonType": "object",
                        "required": ["prompt_tokens", "total_tokens", "completion_tokens"],
                        "properties": {
                            "prompt_tokens": {"bsonType": "int"},
                            "total_tokens": {"bsonType": "int"},
                            "completion_tokens": {"bsonType": "int"}
                        }
                    },
                    "cost": {
                        "bsonType": "object",
                        "required": ["prompt_tokens", "total_tokens", "completion_tokens"],
                        "properties": {
                            "prompt_tokens": {"bsonType": "double"},
                            "total_tokens": {"bsonType": "double"},
                            "completion_tokens": {"bsonType": "double"}
                        }
                    },
                    "limit": {"bsonType": "int"}
                }
            },
            "inference_chat": {
                "bsonType": "object",
                "required": ["tokens", "cost", "limit"],
                "properties": {
                    "tokens": {
                        "bsonType": "object",
                        "required": ["prompt_tokens", "total_tokens", "completion_tokens"],
                        "properties": {
                            "prompt_tokens": {"bsonType": "int"},
                            "total_tokens": {"bsonType": "int"},
                            "completion_tokens": {"bsonType": "int"}
                        }
                    },
                    "cost": {
                        "bsonType": "object",
                        "required": ["prompt_tokens", "total_tokens", "completion_tokens"],
                        "properties": {
                            "prompt_tokens": {"bsonType": "double"},
                            "total_tokens": {"bsonType": "double"},
                            "completion_tokens": {"bsonType": "double"}
                        }
                    },
                    "limit": {"bsonType": "int"}
                }
            },
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"}
        }
    }
}