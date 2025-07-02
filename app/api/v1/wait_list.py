from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends
from starlette.responses import JSONResponse

from app.dtos.register_interest_dto import RegisterInterestDto
from app.services.dependencies import get_wait_list_service
from app.services.wait_list_service import WaitListService
from app.utils.helpers.api_helpers import api_response

router = APIRouter(tags=["wait list"])


@router.post("/register")
async def register_interest(payload: RegisterInterestDto, backgroundTask: BackgroundTasks,
                            wait_list_service: WaitListService = Depends(get_wait_list_service)) -> JSONResponse:
    response = await wait_list_service.create_interest(payload, backgroundTask)
    return api_response(code=response.code, data=response.data, message=response.message)
