from openai import OpenAI
from anthropic import Anthropic
import os

key = os.environ.get('OPEN_IA_KEY')

client = OpenAI(
  api_key= key
)

claude_client = Anthropic(
  api_key=os.environ.get("ANTHROPIC_API_KEY")
)

async def inference(prompt_root: str, prompt_user:str):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        { "role": "system", "content": prompt_root },
        { "role": "user", "content": prompt_user }
      ]
    )
    message = completion.choices[0].message.content.strip('"')
    return {
        "inference_text": message,
        "prompt_tokens" : completion.usage.prompt_tokens,
        "completion_tokens" : completion.usage.completion_tokens,
        "total_tokens" : completion.usage.total_tokens,
    }

async def inference_chat(prompt_root: str, prompt_user:str):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        { "role": "system", "content": prompt_root },
        { "role": "user", "content": prompt_user }
      ]
    )
    message = completion.choices[0].message.content.strip('"')
    # return {
    #     "message": message,
    #     "prompt_tokens" : completion.usage.prompt_tokens,
    #     "completion_tokens" : completion.usage.completion_tokens,
    #     "total_tokens" : completion.usage.total_tokens,
    # }
    return{
        message
    }

def format_chat_history(messages):
    formatted_history = []
    for i, message in enumerate(messages):
        # Elimina espacios en blanco al principio y al final, y verifica si el mensaje no está vacío
        message = message.strip()
        if message:
            role = "user" if i % 2 == 0 else "assistant"
            formatted_history.append({"role": role, "content": message})
    return formatted_history

async def inference_claude_chat(system_prompt: str, chat_history: dict):
    message = claude_client.messages.create(
        max_tokens=1024,
        system= system_prompt,
        messages= chat_history,
        model="claude-3-sonnet-20240229",
    )
    print("**",message.content)
    print("============",message)
    assistant_message = message.content[0].text
    return {
        "inference_text": assistant_message,
        "prompt_tokens": message.usage.input_tokens,
        "completion_tokens": message.usage.output_tokens
    }

#claude-3-5-sonnet-20240620
#claude-3-haiku-20240307
#claude-3-sonnet-20240229
#claude-3-opus-20240229