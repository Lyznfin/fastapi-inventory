from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.serializers.products import Product, ProductCreate, ProductUpdate, read_db_product_all, create_db_product, read_db_product_by_id, read_db_product_by_supplier, update_db_product, delete_db_product
from app.database import get_db
from app.models import NotFoundError
from app.routers.limiter import limiter

products_router = APIRouter (
    prefix="/products",
)

@products_router.get("/")
@limiter.limit("1/second")
async def read_all_product(request: Request, db: Session = Depends(get_db)) -> list[Product]:
    try:
        db_products = await read_db_product_all(db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    return [Product(**db_product.__dict__) for db_product in db_products]

@products_router.post("/{supplier_id}")
@limiter.limit("1/second")
async def create_product(request: Request, supplier_id: int, product: ProductCreate, db: Session = Depends(get_db)) -> Product:
    db_product = await create_db_product(product, supplier_id, db)
    return Product(**db_product.__dict__)

@products_router.get("/{product_id}")
@limiter.limit("1/second")
async def read_product(request: Request, product_id: int, db: Session = Depends(get_db)) -> Product:
    try:
        db_product = await read_db_product_by_id(product_id, db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    return Product(**db_product.__dict__)

@products_router.get("/supplier/{supplier_id}")
@limiter.limit("1/second")
async def read_product_by_supplier(request: Request, supplier_id: int, db: Session = Depends(get_db)) -> list[Product]:
    try:
        db_products = await read_db_product_by_supplier(supplier_id, db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    return [Product(**db_product.__dict__) for db_product in db_products]

@products_router.put("/{product_id}/supplier/{supplier_id}")
@limiter.limit("1/second")
async def update_product(request: Request, product_id: int, product: ProductUpdate, supplier_id: int | None = None, db: Session = Depends(get_db)) -> Product:
    try:
        db_product = await update_db_product(product_id, supplier_id, product, db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    return Product(**db_product.__dict__)

@products_router.delete("/{product_id}")
@limiter.limit("1/second")
async def delete_product(request: Request, product_id: int, db: Session = Depends(get_db)) -> Product:
    try:
        db_product = await delete_db_product(product_id, db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    return Product(**db_product.__dict__)