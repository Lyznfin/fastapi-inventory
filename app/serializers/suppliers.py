from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session, joinedload

from app.models import DBSuppliers, NotFoundError
from app.serializers.products import Product, DBProducts

class Supplier(BaseModel):
    id: int
    name: str
    company: str
    email: EmailStr
    phone: str
    products: list[Product] = []

    class Config:
        orm_mode = True

class CreateSupplier(BaseModel):
    name: str
    company: str
    email: EmailStr
    phone: str

class UpdateSupplier(BaseModel):
    name: str | None
    company: str | None
    email: EmailStr | None
    phone: str | None

async def read_db_supplier_all(session: Session) -> list[DBSuppliers]:
    db_suppliers = session.query(DBSuppliers).options(joinedload(DBSuppliers.products)).all()
    if db_suppliers is None:
        raise NotFoundError(f"Products is still empty.")
    suppliers: list[DBSuppliers] = []
    for db_supplier in db_suppliers:
        products = [Product(**product.__dict__) for product in db_supplier.products]
        supplier_data = db_supplier.__dict__
        supplier_data["products"] = products
        suppliers.append(Supplier(**supplier_data))
    return suppliers

async def create_db_supplier(supplier: CreateSupplier, session: Session) -> DBSuppliers:
    db_supplier = DBSuppliers(**supplier.model_dump())
    session.add(db_supplier)
    session.commit()
    session.refresh(db_supplier)
    return db_supplier

async def read_db_supplier_by_id(supplier_id: int, session: Session) -> DBSuppliers:
    db_supplier = session.query(DBSuppliers).filter(DBSuppliers.id == supplier_id).first()
    if db_supplier is None:
        raise NotFoundError(f"Product with id {supplier_id} not found.")
    return db_supplier

# def read_db_supplier_by_item(supplier_id: int, session: Session) -> Product:
#     db_suppliers = session.query(DBSuppliers).filter(DBSuppliers. == supplier_id).all()
#     if db_suppliers is None:
#         raise NotFoundError(f"Product with id {supplier_id} not found.")
#     return [Product(**db_supplier.__dict__) for db_supplier in db_suppliers]

async def update_db_supplier(supplier_id: int, supplier: UpdateSupplier, session: Session) -> DBSuppliers:
    db_supplier = await read_db_supplier_by_id(supplier_id, session)
    for key, value in supplier.model_dump(exclude_none=True).items():
        setattr(db_supplier, key, value)
    session.commit()
    session.refresh(db_supplier)
    return db_supplier

async def update_db_supplier_product(supplier_id: int, supplier: UpdateSupplier, session: Session) -> DBSuppliers:
    db_supplier = await read_db_supplier_by_id(supplier_id, session)
    for key, value in supplier.model_dump(exclude_none=True).items():
        setattr(db_supplier, key, value)
    session.commit()
    session.refresh(db_supplier)
    return db_supplier

async def delete_db_supplier(supplier_id: int, session: Session) -> DBSuppliers:
    db_supplier = await read_db_supplier_by_id(supplier_id, session)
    session.delete(db_supplier)
    session.commit()
    return db_supplier