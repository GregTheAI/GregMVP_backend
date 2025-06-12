from fastapi import APIRouter


router = APIRouter(tags=["Uploads"])


@router.post("/")
def upload_document():
    return {
        "message": "welcome to the upload API"}