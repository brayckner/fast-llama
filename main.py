from fastapi import FastAPI
import httpx
from httpx import request
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class Prompt(BaseModel):
    model: str
    messages: List[Message]
    stream: bool

@app.get("/")
async def root():
    return {"message": "Hello World LLama"}

# [POST] Request to local running llama3.2
@app.post("/llama/chat")
async def llama_prompt(prompt: Prompt):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/chat",
            json=prompt.model_dump()
        )
    return response.json()

def define_prompt(user_prompt: str):
    message = Message(role="user", content=user_prompt)
    prompt = Prompt(model="llama3.2", messages=[message], stream=False)
    return prompt

def hit_llama_endpoint(user_prompt):
    prompt = define_prompt(user_prompt)
    url = "http://localhost:8000/llama/chat"
    headers = {"Content-Type": "application/json"}
    response = httpx.request(
        "POST",
        url,
        json=prompt.model_dump(),
        headers=headers,
        timeout=30.0
    )

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    return response

if __name__ == "__main__":
    result = hit_llama_endpoint("Who was MF Doom? And what was his song belize about?")
    print("Response from llama: ", result)
