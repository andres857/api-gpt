inferences_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["agents"],
        "properties": {
            "agents": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["idAgent", "text", "task", "metadata"],
                    "properties": {
                        "idAgent": {"bsonType": "objectId"},
                        "text": {"bsonType": "string"},
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