from datetime import timezone, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

SECRET_KEY: str = settings.JWT_SECRET_KEY
EXPIRY_TIME: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM: str = "HS256"


class JwtService:
    @staticmethod
    def encode(payload: dict) -> str:
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode(token: str) -> dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    @staticmethod
    def verify_token(token: str) -> bool:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")

            return username is not None
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    @staticmethod
    def hash_password(password: str) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    @staticmethod
    def generate_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_TIME)
        to_encode.update({"exp": expire})
        return JwtService.encode(to_encode)
