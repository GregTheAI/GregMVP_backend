from fastapi import APIRouter


router = APIRouter(tags=["auth"])


@router.post("/login")
def login():
    return {
        "access_token": "fake-token"}



@router.post("/password-recovery/{email}")
def recover_password(email: str):
    return { "message": "Password recovery email sent" }


@router.post("/reset-password/")
def reset_password(body: str) :
    return { "message": "Password recovery email sent" }