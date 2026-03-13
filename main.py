from fastapi import FastAPI
from database import database
from controller.webhook_controller import router as webhook_router

app = FastAPI(title="Telenova API", description="API para integração do n8n com MySQL local")

@app.on_event("startup")
async def startup():
    print("Conectando ao banco de dados...")
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    print("Desconectando do banco de dados...")
    await database.disconnect()

app.include_router(webhook_router)

@app.get("/")
def home():
    return {"message": "API Telenova está online! Acesse /docs para ver o Swagger."}
