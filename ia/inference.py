from openai import OpenAI

client = OpenAI(
  api_key=""
)

async def inference(prompt_root: str, prompt_user:str):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": prompt_root },
      {"role": "user", "content": prompt_user}
    ]
  )
  print(completion.choices[0].message)
  return completion.choices[0].message

# async def main():
#   await transcription(message_prompt_root, message_prompt_user)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())