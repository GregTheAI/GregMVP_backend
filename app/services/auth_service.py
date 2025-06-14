# write service for authentication with jwt and outh2
from symtable import Class

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.dtos.user_dto import UserResponseDto, RegisterUserDto
from app.entities import User
from app.repositories.user_repository import UserRepository
from app.services.jwt_service import JwtService

# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from app.dtos.user import User, UserInDB
# from app.database import get_user_by_email, create_user
# from app.config import settings
# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a plain password against a hashed password."""
#     return pwd_context.verify(plain_password, hashed_password)
# def get_password_hash(password: str) -> str:
#     """Hash a password using bcrypt."""
#     # implement password hashing with bcrypt without  validatiion
#
#
#     return pwd_context.hash(password)
#
# def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
#     """Create a JWT access token."""
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt
# def authenticate_user(email: str, password: str) -> UserInDB | None:
#     """Authenticate a user by email and password."""
#     user = get_user_by_email(email)
#     if not user or not verify_password(password, user.hashed_password):
#         return None
#     return user
# def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
#     """Get the current user from the JWT token."""
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = UserInDB(email=email)
#     except JWTError:
#         raise credentials_exception
#     user = get_user_by_email(token_data.email)
#     if user is None:
#         raise credentials_exception
#     return user
# def create_new_user(user: User) -> UserInDB:
#     """Create a new user in the database."""
#     user.hashed_password = get_password_hash(user.hashed_password)
#     return create_user(user)

class AuthService:
    """Service for user-related operations."""
    def __init__(self, user_repo = Depends(UserRepository)):
        self.user_repo = user_repo


