import asyncio
import os
from pathlib import Path

from fastapi import FastAPI
from starlette.requests import Request

from app.core.config import settings
from app.core.log_config import LogExceptionsMiddleware, configure_logger
from app.utils.helpers.api_helpers import api_server_error, api_ok_response


class Bootstrap:
    def __init__(self, app: FastAPI):
        self.app = app
        self.logger = configure_logger(__name__)

    def run(self):
        self.logger.info("Starting application bootstrap process...")
        self._register_exception_handlers()
        self._register_middlewares()
        self._register_routes()
        self.logger.info("Application bootstrap process completed.")

    def run_database_migrations(self):
        self.logger.info("Running database migrations...")
        try:
            from alembic import command
            from alembic.config import Config

            current_working_dir = os.getcwd()
            self.logger.info(f"Current working directory: {current_working_dir}")

            alembic_config_path = os.path.join(current_working_dir, "alembic.ini")

            self.logger.info(f"Attempting to load Alembic config from: {alembic_config_path}")

            if not os.path.exists(alembic_config_path):
                self.logger.error(f"Alembic config file NOT FOUND at: {alembic_config_path}")
                raise FileNotFoundError(f"alembic.ini not found at {alembic_config_path}")

            alembic_cfg = Config(alembic_config_path)

            self.logger.info("Attempting Alembic upgrade command...")
            command.upgrade(alembic_cfg, "head")
            self.logger.info("Database migrations completed successfully.")
        except Exception as e:
            self.logger.exception("Failed to run Alembic migrations")
            raise e

    def _register_middlewares(self):
        from starlette.middleware.sessions import SessionMiddleware

        self.app.add_middleware(LogExceptionsMiddleware)

        self.app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET_KEY)

        if settings.all_cors_origins:
            from starlette.middleware.cors import CORSMiddleware
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=settings.all_cors_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            )
        self.logger.info("Middlewares registered.")

    def _register_routes(self):
        from app.api.v1 import api_router

        @self.app.get("/", tags=["Health"])
        async def root():
            return api_ok_response(message=f"Welcome to the {settings.PROJECT_NAME}API!")

        @self.app.get("/health", tags=["Health"])
        async def health():
            return "healthy"

        self.app.include_router(api_router, prefix=settings.API_V1_STR)
        self.logger.info("Routes registered.")

    def _register_exception_handlers(self):
        @self.app.exception_handler(Exception)
        async def global_exception_handler(request: Request, ex: Exception):
            self.logger.error(f"Unhandled exception: {ex}", exc_info=True)
            return api_server_error(errors={"detail": str(ex)})


        @self.app.on_event("shutdown")
        async def shutdown_event():
            self.logger.info("Application shutdown event triggered.")