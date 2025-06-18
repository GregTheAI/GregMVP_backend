from fastapi import APIRouter, UploadFile, File, Depends

from app.services.dependencies import get_s3_service, get_extractor_service

router = APIRouter(tags=["Uploads"])


@router.post("/")
async def upload_document(request: UploadFile = File(...), s3_service=Depends(get_s3_service), extractor_service=Depends(get_extractor_service)):
    # s3_url = s3_service.upload_file_to_s3(request.file, request.filename)

    raw_text = extractor_service.extract_text_from_file(file=request.file, file_name=request.filename)

    extracted = await extractor_service.extract_info_from_text(raw_text)
    # save_document(s3_url, extracted)
    return {"s3_url": "https://url_here.com", "extracted": extracted}