from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
)
from typing import Optional, Dict, TypeVar

from app.dtos.api_response import ApiResponse

T = TypeVar("T")

def api_ok_response(data: T = None, message: str = "Success") -> JSONResponse:
    response = ApiResponse[T](
        message=message,
        code=HTTP_200_OK,
        data=data,
        errors=None
    )
    return JSONResponse(status_code=HTTP_200_OK, content=response.dict())

def api_created_response(data: T = None, message: str = "Created successfully") -> JSONResponse:
    response = ApiResponse[T](
        message=message,
        code=HTTP_201_CREATED,
        data=data,
        errors=None
    )
    return JSONResponse(status_code=HTTP_201_CREATED, content=response.dict())

def api_bad_response(message: str = "Bad request", errors: Optional[Dict] = None) -> JSONResponse:
    response = ApiResponse(
        message=message,
        code=HTTP_400_BAD_REQUEST,
        data=None,
        errors=errors
    )
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=response.dict())

def api_not_found(message: str = "Not found", errors: Optional[Dict] = None) -> JSONResponse:
    response = ApiResponse(
        message=message,
        code=HTTP_404_NOT_FOUND,
        data=None,
        errors=errors
    )
    return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=response.dict())

def api_server_error(message: str = "Internal server error", errors: Optional[Dict] = None) -> JSONResponse:
    response = ApiResponse(
        message=message,
        code=HTTP_500_INTERNAL_SERVER_ERROR,
        data=None,
        errors=errors
    )
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content=response.dict())
