from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import get_settings
from app.core.log_config import LogExceptionsMiddleware
from app.utils.constants.constants import AuthConstants
from app.utils.helpers.api_helpers import api_ok_response

settings = get_settings()


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    swagger_ui_init_oauth={},
    swagger_ui_oauth_scope=["persistAuthorization", True]
)

app.add_middleware(LogExceptionsMiddleware)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY
)

if settings.all_cors_origins:
    from starlette.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

from app.api.v1 import api_router


@app.get("/", tags=["Health"])
async def root():
    return api_ok_response(message=f"Welcome to the {settings.PROJECT_NAME}API!")


@app.get("/health", tags=["Health"])
async def health():
    return "healthy"


app.include_router(api_router, prefix=settings.API_V1_STR)
# Bootstrap.run_database_migrations()

# Bootstrap(app).run()
