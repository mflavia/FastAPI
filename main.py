from fastapi import FastAPI
from app.controllers.product_controller import router as product_router

app = FastAPI()

app.include_router(product_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "API de Produtos FastAPI"}
