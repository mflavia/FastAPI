from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from .models import Base  # ou o nome do seu modelo
from pymongo import MongoClient
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# Conexão com o MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/logs")
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["logs"]
mongo_collection = mongo_db["product_views"]


# Função que cria uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db  # usando 'yield' para criar uma dependência em FastAPI
    finally:
        db.close()
        



