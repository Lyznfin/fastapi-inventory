from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.serializers.suppliers import Supplier, CreateSupplier, UpdateSupplier, read_db_supplier_all, create_db_supplier, read_db_supplier_by_id, update_db_supplier, delete_db_supplier
from app.database import get_db
from app.models import NotFoundError
from app.routers.limiter import limiter

suppliers_router = APIRouter (
    prefix="/suppliers",
)

@suppliers_router.get("/")
@limiter.limit("1/second")
async def read_all_supplier(request: Request, db: Session = Depends(get_db)) -> list[Supplier]:
    try:
        db_suppliers = await read_db_supplier_all(db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    return [Supplier(**db_supplier.__dict__) for db_supplier in db_suppliers]

@suppliers_router.post("/")
@limiter.limit("1/second")
async def create_supplier(request: Request, supplier: CreateSupplier, db: Session = Depends(get_db)) -> Supplier:
    db_supplier = await create_db_supplier(supplier, db)
    return Supplier(**db_supplier.__dict__)

@suppliers_router.get("/{supplier_id}")
@limiter.limit("1/second")
async def read_supplier(request: Request, supplier_id: int, db: Session = Depends(get_db)) -> Supplier:
    try:
        db_supplier = await read_db_supplier_by_id(supplier_id, db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    return Supplier(**db_supplier.__dict__)

@suppliers_router.put("/{supplier_id}")
@limiter.limit("1/second")
async def update_supplier(request: Request, supplier_id: int, supplier: UpdateSupplier, db: Session = Depends(get_db)) -> Supplier:
    try:
        db_supplier = await update_db_supplier(supplier_id, supplier, db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    return Supplier(**db_supplier.__dict__)

# @suppliers_router.put("/{supplier_id}")
# @limiter.limit("1/second")
# async def update_supplier_products(request: Request, supplier_id: int, supplier: UpdateSupplier, product_id: int, db: Session = Depends(get_db)) -> Supplier:
#     try:
#         db_supplier = await update_db_supplier(supplier_id, supplier, db)
#     except NotFoundError as error:
#         raise HTTPException(status_code=404) from error
#     return {"status code": "200", "data": Supplier(**db_supplier.__dict__)}

@suppliers_router.delete("/{supplier_id}")
@limiter.limit("1/second")
async def delete_supplier(request: Request, supplier_id: int, db: Session = Depends(get_db)) -> Supplier:
    try:
        db_supplier = await delete_db_supplier(supplier_id, db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    return Supplier(**db_supplier.__dict__)