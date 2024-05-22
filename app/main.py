from app.database import lifespan, SessionLocal
from app.routers.limiter import limiter
from app.routers.products import products_router
from app.routers.suppliers import suppliers_router

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://localhost:3000'
]

app = FastAPI(lifespan=lifespan)
app.include_router(suppliers_router)
app.include_router(products_router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.get("/")
def read_root():
    return "Server is running."