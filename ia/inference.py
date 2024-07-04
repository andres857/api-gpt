from openai import OpenAI
import os

key = os.environ.get('OPEN_IA_KEY')

client = OpenAI(
  api_key= key
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
    return message