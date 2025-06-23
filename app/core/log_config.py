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
    logger.propagate = True  # Ensure logs propagate to root

    # Add handlers only if not already present
    if not any(isinstance(h, LogtailHandler) for h in logger.handlers):
        handler = LogtailHandler(source_token=settings.LOG_SOURCE_TOKEN, host=settings.LOG_URL)
        formatter = logging.Formatter(f"%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(f"%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

class LogExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logger = logging.getLogger()
            logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
            raise
