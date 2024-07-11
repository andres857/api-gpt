inference_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["id_mzg_content", "id_agent", "result"],
        "properties": {
            "id_mzg_content": {"bsonType": "int"},
            "id_agent": {"bsonType": "objectId"},
            "result": {
                "bsonType": "object",
                "required": ["text", "task"],
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
                            "message": {"bsonType": "string"}
                        }
                    }
                }
            },
            "metadata": {
                "bsonType": "object",
                "properties": {
                    "caracteres": {"bsonType": "int"},
                    "palabras": {"bsonType": "int"},
                    "tokens": {"bsonType": "int"},
                    "idioma": {"bsonType": "string"},
                    "porcentaje_reduccion": {"bsonType": "double"}
                }
            },
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"}
        }
    }
}