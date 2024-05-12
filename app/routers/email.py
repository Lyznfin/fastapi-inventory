from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.models import NotFoundError
from app.serializers.products import read_db_product_by_id
from app.serializers.suppliers import read_db_supplier_by_id
from app.routers.limiter import limiter
from app.database import get_db
from app.constant import email, key

email_router = APIRouter (
    prefix="/email",
)

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

class EmailSchema(BaseModel):
    email: list[EmailStr]

class EmailContent(BaseModel):
    message: str
    subject: str

conf = ConnectionConfig(
    MAIL_USERNAME = email,
    MAIL_PASSWORD = key,
    MAIL_FROM = email,
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

@email_router.post("/{product_id}")
@limiter.limit("1/minute")
async def send_email(request: Request, product_id: int, content: EmailContent, db: Session = Depends(get_db)):
    try:
        product = await read_db_product_by_id(product_id, db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    
    try:
        supplier = await read_db_supplier_by_id(product.supplier_id, db)
    except NotFoundError as error:
        raise HTTPException(status_code=404) from error
    
    supplier_email = supplier.email

    html = f"""
    <p> Hallo {content.subject} </p>
    <br>
    <p> {content.message} </p>
    <br>
    """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[supplier_email],
        body=html,
        subtype=MessageType.html
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})