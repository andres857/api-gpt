from db import connect_to_database
from models.agent import agent_model
from utils import JSONEncoder
from bson import ObjectId
import json

db = connect_to_database()
    
def create_agent(agent_data):
    # Validar y formatear los datos con el esquema JSON del modelo
    validated_data = agent_model.validate(agent_data.dict())

    # Utilizar la referencia 'db' para insertar los datos en MongoDB
    result = db.agentes.insert_one(validated_data)
    return str(result.inserted_id)

def get_all_agents() -> list:
    agents_cursor = db.agentes.find({})
    agents_list = list(agents_cursor)
    agents = json.loads(JSONEncoder().encode(agents_list))
    return agents

def update_agent(agent_id, updated_data):
    # Validar y formatear los datos actualizados con el esquema JSON del modelo
    update_dict = updated_data.dict(exclude_unset=True)

    # Utilizar la referencia 'db' para actualizar el documento en MongoDB
    result = db.agentes.update_one(
        {'_id': ObjectId(agent_id)},
        {'$set': update_dict}
    )

    return result

def delete_agent(agent_id):
    # Utilizar la referencia 'db' para eliminar el documento en MongoDB
    result = db.agentes.delete_one({'_id': ObjectId(agent_id)})
    return result.deleted_count