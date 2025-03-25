from pydantic import BaseModel, Field
from enum import Enum


class ProductStatus(str, Enum):
    EM_ESTOQUE = "EM_ESTOQUE"
    EM_REPOSICAO = "EM_REPOSICAO"
    EM_FALTA = "EM_FALTA"
    

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="Nome do produto é obrigatório")
    description: str | None = None
    price: float = Field(..., gt=0, description="O preço deve ser numérico e maior que zero")
    status: ProductStatus
    stock_quantity: int = Field(..., ge=0, description="A quantidade em estoque deve ser numérica e maior ou igual a zero")


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
        

class ProductUpdate(ProductBase):
    pass
