from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, mongo_collection
from app.models import Product, ProductStatus
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, Field

router = APIRouter(prefix="/products", tags=["Products"])

# Criar produto
@router.post("/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Verifica se o nome já existe
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Produto com esse nome já existe.")

    # Criando e salvando no banco
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Listar produtos
@router.get("/", response_model=list[ProductCreate])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    # Registrar log no MongoDB
    log_entry = {
        "action": "list_products",
        "timestamp": datetime.utcnow(),
        "count": len(products)
    }
    mongo_collection.insert_one(log_entry)

    return products

# Obter produto por ID
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    # Buscar o produto no SQLite
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Buscar os logs de visualização no MongoDB
    product_logs = list(mongo_collection.find({"product_id": product_id}, {"_id": 0}))

    # Registrar a visualização atual no MongoDB
    log_entry = {
        "product_id": product_id,
        "viewed_at": datetime.utcnow()
    }
    mongo_collection.insert_one(log_entry)

    # Retornar o produto e seu histórico de visualizações
    return {
        "product": {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "status": product.status.name,
            "stock_quantity": product.stock_quantity
        },
        "view_logs": product_logs
    }

# Definição do schema de entrada para atualização de produto
class ProductUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1, description="Nome do produto")
    description: str = Field(..., description="Descrição do produto")
    price: float = Field(..., gt=0, description="Preço deve ser positivo")
    status: ProductStatus = Field(..., description="Status do produto")
    stock_quantity: int = Field(..., ge=0, description="Quantidade em estoque não pode ser negativa")

@router.put("/{product_id}")
def update_product(product_id: int, product_data: ProductUpdateSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Atualizar os campos do produto
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.status = product_data.status
    product.stock_quantity = product_data.stock_quantity

    # Salvar as mudanças no banco
    db.commit()
    db.refresh(product)

    return {"message": "Produto atualizado com sucesso", "product": product}

# Deletar produto
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(product)
    db.commit()
    return {"message": "Produto deletado com sucesso"}



@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    # Formatar a resposta JSON
    product_list = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price
        }
        for product in products
    ]

    # Registrar log de busca no MongoDB
    log_entry = {
        "searched_at": datetime.utcnow(),
        "products": [{"id": p["id"], "name": p["name"]} for p in product_list]
    }
    mongo_collection.insert_one(log_entry)

    return {"products": product_list}

