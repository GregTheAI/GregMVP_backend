from fastapi import APIRouter


router = APIRouter(tags=["conversations"])


@router.post("/")
def start_conversation():
    return {
        "message": "welcome to the conversations API"}