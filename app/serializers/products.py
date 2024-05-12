from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import DBProducts, NotFoundError

class Product(BaseModel):
    id: int
    name: str
    stock_quantity: int
    unit_price: float
    sold_quantity: int
    revenue: float
    supplier_id: int | None

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    stock_quantity: int
    unit_price: float
    sold_quantity: int
    revenue: float

class ProductUpdate(BaseModel):
    name: str | None
    stock_quantity: int | None
    unit_price: float | None
    sold_quantity: int | None
    revenue: float | None

async def read_db_product_all(session: Session) -> list[DBProducts]:
    db_products = session.query(DBProducts).all()
    if db_products is None:
        raise NotFoundError(f"Products is still empty.")
    return [db_product for db_product in db_products]

async def create_db_product(product: ProductCreate, supplier_id: int, session: Session) -> DBProducts:
    db_product = DBProducts(**product.model_dump())
    db_product.supplier_id = supplier_id
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

async def read_db_product_by_id(product_id: int, session: Session) -> DBProducts:
    db_product = session.query(DBProducts).filter(DBProducts.id == product_id).first()
    if db_product is None:
        raise NotFoundError(f"Product with id {product_id} not found.")
    return db_product

async def read_db_product_by_supplier(supplier_id: int, session: Session) -> list[Product]:
    db_products = session.query(DBProducts).filter(DBProducts.supplier_id == supplier_id).all()
    if db_products is None:
        raise NotFoundError(f"Product with id {supplier_id} not found.")
    return [Product(**db_product.__dict__) for db_product in db_products]

async def update_db_product(product_id: int, supplier_id: int, product: ProductUpdate, session: Session) -> DBProducts:
    db_product = await read_db_product_by_id(product_id, session)
    for key, value in product.model_dump(exclude_none=True).items():
        setattr(db_product, key, value)
    if supplier_id != None:
        db_product.supplier_id = supplier_id
    session.commit()
    session.refresh(db_product)
    return db_product

async def delete_db_product(product_id: int, session: Session) -> DBProducts:
    db_product = await read_db_product_by_id(product_id, session)
    session.delete(db_product)
    session.commit()
    return db_product