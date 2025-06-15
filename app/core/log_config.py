import logging
from logtail import LogtailHandler

import traceback

from logging import Logger

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


def configure_logger(logger_name: str | None = None) -> Logger:
    import logging

    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    handler = LogtailHandler(source_token=settings.LOG_SOURCE_TOKEN, host=settings.LOG_URL)
    # formatter = logging.Formatter(json.dumps({
    #     "message": "%(message)s",
    #     "level": "%(levelname)s",
    #     "logger": "%(name)s",
    #     "time": "%(asctime)s",
    #     "module": "%(module)s",
    #     "function": "%(funcName)s",
    #     "line": "%(lineno)d"
    # }))

    formatter = logging.Formatter(f"%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logging.getLogger("alembic.runtime.migration").addHandler(handler)
    logging.getLogger("uvicorn.access").addHandler(handler)
    logging.getLogger("uvicorn.error").addHandler(handler)
    logger.addHandler(handler)
    return logger

class LogExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logger = logging.getLogger()
            logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
            raise
