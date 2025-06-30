from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import get_settings
from app.core.log_config import LogExceptionsMiddleware, configure_logger
from app.utils.helpers.api_helpers import api_server_error, api_ok_response
from starlette_session.backends import BackendType

settings = get_settings()
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

    @staticmethod
    def run_database_migrations(alembic_file: str = "alembic.ini"):
        try:
            from alembic import command
            from alembic.config import Config

            alembic_cfg = Config(alembic_file)

            command.upgrade(alembic_cfg, "head")
        except Exception as e:
            raise e

    def _register_middlewares(self):

        self.app.add_middleware(LogExceptionsMiddleware)

        self.app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SESSION_SECRET_KEY,
        backend_type=BackendType.redis,
        backend_client=redis_client,
        cookie_name="session",
        cookie_max_age=3600,
        cookie_https_only=True,
        cookie_same_site="lax"
)
        self.app.add_middleware(
            SessionMiddleware,
            secret_key=settings.SESSION_SECRET_KEY,
            session_cookie="session",
            https_only=True,
            same_site="lax",   # Try "lax" instead of "none" for testing
            max_age=1800,
            path="/",
            domain=None,  # Use None if domain is not set 
    ) # 1 hour)

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
