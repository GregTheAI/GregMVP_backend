from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.api.v1 import auth, conversations, customers, upload

api_router = APIRouter()


bearer_scheme = HTTPBearer()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(conversations.router, prefix="/conversations", dependencies=[Depends(bearer_scheme)])

api_router.include_router(customers.router, prefix="/customers", tags=["customers"], dependencies=[Depends(bearer_scheme)])

api_router.include_router(upload.router, prefix="/upload", tags=["Uploads"], dependencies=[Depends(bearer_scheme)])

