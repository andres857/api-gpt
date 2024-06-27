from fastapi import Depends
from db import get_database
from models.agent import agent_model
from utils import JSONEncoder
from bson import ObjectId
import json

async def get_db():
    db = await anext(get_database())
    try:
        yield db
    finally:
        pass
    
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

async def get_agent_by_id(agent_id: str, db = Depends(get_db)) -> dict:
    agent = await db.agentes.find_one({"_id": ObjectId(agent_id)})
    if agent:
        agent = json.loads(JSONEncoder().encode(agent))
    return agent

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