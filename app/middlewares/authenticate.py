from fastapi import Depends, HTTPException, Request, status, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.dtos.user_dto import UserResponseDto
from app.services.user_service import UserService
from app.core.config import get_settings
from app.utils.constants.constants import AuthConstants


settings = get_settings()

security = HTTPBearer(auto_error=False)
ALGORITHM = "HS256"

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends()
) -> UserResponseDto:
    token = credentials.credentials if credentials else request.cookies.get(AuthConstants.ACCESS_TOKEN_COOKIE_KEY)
    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token")
    return await auth_user(token, user_service)


async def get_email_from_token(token):
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])  # Or use Google’s public key
    email: str = payload.get("email")
    return email


async def get_current_user_websocket(websocket: WebSocket, user_service: UserService = Depends()) -> UserResponseDto:
    auth_header = websocket.headers.get("authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=400, detail="Missing or invalid auth header")

    token = auth_header.split(" ")[1]

    return await auth_user(token, user_service)


async def auth_user(token: str, user_service: UserService) -> UserResponseDto:
    try:
        email = await get_email_from_token(token)
        if not email:
            raise HTTPException(status_code=400, detail="Token payload missing email")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token {e}")

    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user