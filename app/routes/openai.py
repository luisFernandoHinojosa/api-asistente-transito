from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

router = APIRouter()

# Obtener la API Key desde las variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("La API Key de OpenAI no está configurada.")  

@router.post("/chat")
async def chat_with_openai(payload: dict):
    message = payload.get("message")
    
    if not message:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo", 
        "messages": [{"role": "user", "content": message}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
