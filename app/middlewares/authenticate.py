from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.services.user_service import UserService
from app.core.config import settings

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends()
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])  # Or use Google’s public key
        email: str = payload.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Token payload missing email")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token {e}")

    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
