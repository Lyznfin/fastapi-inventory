from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship

from app.database import Base

class DBSuppliers(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    company = Column(String(100))
    email = Column(String(50))
    phone = Column(String(20))
    products = relationship("DBProducts", back_populates="supplier")

class DBProducts(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    stock_quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)
    sold_quantity = Column(Integer, default=0)
    revenue = Column(Float, default=0)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    supplier = relationship("DBSuppliers", back_populates="products")

class NotFoundError(Exception):
    pass