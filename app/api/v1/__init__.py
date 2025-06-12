from fastapi import APIRouter

from app.api.v1 import auth, conversations, customers, upload

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(conversations.router, prefix="/conversations")

api_router.include_router(customers.router, prefix="/customers", tags=["customers"])

api_router.include_router(upload.router, prefix="/upload", tags=["Uploads"])

