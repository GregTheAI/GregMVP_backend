from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.api.v1 import auth, conversations, customers, upload
from app.middlewares.authenticate import get_current_user
from app.services.dependencies import get_user_service

api_router = APIRouter()


bearer_scheme = HTTPBearer()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(conversations.router, prefix="/conversations", dependencies=[Depends(get_current_user)], tags=["conversations"])

api_router.include_router(customers.router, prefix="/customers", tags=["customers"], dependencies=[Depends(bearer_scheme)])

api_router.include_router(upload.router, prefix="/upload", tags=["Uploads"], dependencies=[Depends(get_current_user)])

