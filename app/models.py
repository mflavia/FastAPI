from sqlalchemy import Column, Integer, String, Float, Boolean, Enum 
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class ProductStatus(enum.Enum):
    EM_ESTOQUE = "EM_ESTOQUE"
    EM_REPOSICAO = "EM_REPOSICAO"
    EM_FALTA = "EM_FALTA"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    status = Column(Enum(ProductStatus), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
