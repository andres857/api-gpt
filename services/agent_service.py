import json
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from db import get_database

db = get_database()

async def create(agent):
    agent_dict = agent.dict(exclude={"id"}, by_alias=True)
    print(f"Service AGENT Create: ${agent_dict}")
    try:
        result = await db.agents.insert_one(agent_dict)
        agent_created = await db.agents.find_one({"_id": result.inserted_id})

        if agent_created:
            agent_created["_id"] = str(agent_created["_id"])
            return agent_created
        else:
            raise HTTPException(status_code=404, detail="Error creando un agente")
    
    except DuplicateKeyError as e:
        raise HTTPException(status_code=400, detail="A Agent with this ID already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating or retrieving agent: {str(e)}")

async def get_all_agents():
    agents = []
    cursor = db.agentes.find()
    async for agent in cursor:
        agent["_id"] = str(agent["_id"])
        agents.append(agent)
    return agents

async def get_agent_by_id(id):
    object_id = ObjectId(id)
    try:
        agent = await db.agentes.find_one({"_id": object_id})
        if agent:
            agent["_id"] = str(agent["_id"])
            return agent
        else:
            raise HTTPException(status_code=404, detail="Agent not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def update_agent(agent_id, updated_data):
    pass

def delete_agent(agent_id):
    # Utilizar la referencia 'db' para eliminar el documento en MongoDB
    pass