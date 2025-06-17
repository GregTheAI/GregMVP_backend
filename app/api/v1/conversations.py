from fastapi import APIRouter
from fastapi.params import Depends

from app.dtos.user_dto import UserResponseDto
from app.middlewares.authenticate import get_current_user
from app.services import UserService

router = APIRouter(tags=["conversations"])


@router.post("/")
def start_conversation():
    return {
        "message": "welcome to the conversations API"}

@router.get("/")
async def get_conversations():

    return {
        "message": "welcome to the conversations API"}