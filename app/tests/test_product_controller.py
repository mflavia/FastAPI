import pytest
from httpx import AsyncClient
import os
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from main import app

from app.database import get_db

from sqlalchemy import create_engine




# Depois (correto para SQLAlchemy 2.0+)
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


from app.models import Base, Product

# Criar banco de testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar uma sessão de banco de dados para testes
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_product(client):
    response = await client.post("/products", json={
        "name": "Produto Teste",
        "description": "Descrição Teste",
        "price": 10.99,
        "status": "EM_ESTOQUE",
        "stock_quantity": 100
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Produto Teste"

@pytest.mark.asyncio
async def test_get_products(client):
    response = await client.get("/products")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_product():
    # Crie o produto primeiro, caso necessário
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Supondo que o ID do produto seja 1
        response = await client.delete("/products/1")

    # Verifique se a exclusão foi bem-sucedida
    assert response.status_code == 200
    assert response.json() == {"detail": "Produto excluído com sucesso"}
