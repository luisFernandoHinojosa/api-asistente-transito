from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv


#---------------------RUTAS-----------------------------------
router = APIRouter()
#--------------------API KEY----------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("La API Key de OpenAI no está configurada.")  
#--------------------------------------------------------
MODEL_ID = os.getenv("MODEL_ID")
#-------------------------------------------------------
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
        "model": MODEL_ID, 
        "messages": [
        {"role": "system", "content": "Asistente de leyes de tránsito de Bolivia. Responde con base en el Código de Tránsito de Bolivia de 1973."},
        {"role": "user", "content": message}
    ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
