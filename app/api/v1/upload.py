from fastapi import APIRouter, UploadFile, File, Depends
from starlette.background import BackgroundTasks

from app.services.dependencies import get_s3_service, get_extractor_service
from app.services.s3_service import S3Service

router = APIRouter(tags=["Uploads"])


@router.post("/")
async def upload_document(request: UploadFile = File(...), s3_service: S3Service=Depends(get_s3_service), extractor_service=Depends(get_extractor_service), background_tasks: BackgroundTasks = None):
    s3_response = s3_service.upload_file(request.file, request.filename, request.content_type)

    if not s3_response.key:
        return {"error": "Failed to upload file to S3"}

    s3_url = s3_service.generate_presigned_url(key=s3_response.key, expires_in=3600)


    background_tasks.add_task(extractor_service.extract_text_from_file, file=request.file, file_name=request.filename)
    # raw_text = extractor_service.extract_text_from_file(file=request.file, file_name=request.filename)
    #
    #
    # extracted = await extractor_service.extract_info_from_text(raw_text)
    # save_document(s3_url, extracted)
    return {"s3_url": s3_url, "status": "uploaded, processing in background"}