from fastapi import APIRouter, HTTPException, Query 
from pydantic import ValidationError, BaseModel
from bson import ObjectId
from schemas.agent import AgentCreate, AgentUpdate, Agent
from services.agent_service import get_agent_by_id, get_all_agents, update_agent
from ia.inference import inference 

class InferenceBody(BaseModel):
    text: str = Query(...)

router = APIRouter(
    prefix='/agents',
    tags=['agents']
)

@router.get("/", responses = {
    200: {"description": "Video uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})

async def get_all():
    agents_list = get_all_agents()
    print(agents_list)
    return agents_list


# @router.post("/", response_model=Agent)
# def create_agent_route(agent_data: AgentCreate):
#     # agent_id = create_agent(agent_data)
#     return "Agent(id=agent_id, **agent_data.dict())"
@router.post("/{agent_id}/inference", responses = {
    200: {"description": "Inference uploaded successfully"},
    400: {"description": "Invalid request body"},
    500: {"description": "Internal server error"}
})

async def generateInference(agent_id: str, body: InferenceBody):
    agent = get_agent_by_id(agent_id)
    print('DATA');
    print (body)
    prompt_message = body.text;
    nombre = agent['rol'];
    inferencia = await inference(agent['prompt'], prompt_message)
    print("inferencia", inferencia)
    print(type(body))
    print(type(nombre))

    return {
        "inference": inferencia,
    }


@router.put("/{agent_id}", responses={
    200: {"description": "Agent updated successfully"},
    400: {"description": "Invalid request body"},
    404: {"description": "Agent not found"},
    500: {"description": "Internal server error"}
})
async def update_agent_route(agent_id: str, agent_update: AgentUpdate):
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(agent_id):
            raise HTTPException(status_code=400, detail="Invalid agent ID format")

        agent = update_agent(agent_id, agent_update)
        
        if agent.matched_count == 0:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return {"message": "Agent updated successfully"}
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
