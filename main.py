from fastapi import FastAPI
from contextlib import asynccontextmanager
from controller.webhook_controller import router as webhook_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield 

app = FastAPI(
    title="Telenova Multi-Tenant API", 
    description="API para integração do n8n com MySQL local",
    lifespan=lifespan 
)


app.include_router(webhook_router)

@app.get("/")
def home():
    return {"message": "API Telenova está online! Acesse /docs para ver o Swagger."}
