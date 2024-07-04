# Definir el esquema JSON
agent_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["rol", "prompt"],
        "properties": {
            "rol": {"bsonType": "string"},
            "prompt": {"bsonType": "string"},
            "descripcion": {"bsonType": "string"},
        },
        "created_at": {"bsonType": "date"},
        "updated_at": {"bsonType": "date"}
    }
}