from services.agent_service import get_agent_by_id
from ia.inference import inference 

async def get_inference (agent_id, prompt_message):
    agent = get_agent_by_id(agent_id)
    nombre = agent['rol']
    inferencia = await inference(agent['prompt'], prompt_message)
    print(type(inferencia))
    print(type(nombre))

        
    return "message"

