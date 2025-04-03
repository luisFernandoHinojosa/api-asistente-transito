from fastapi import FastAPI
from app.routes.openai import router as openai_router

app = FastAPI()

app.include_router(openai_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de FastAPI con MODELO TUNEADO"}
