from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.core.bootstrap import Bootstrap
from app.core.config import get_settings

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

Bootstrap.run_database_migrations()

Bootstrap(app).run()
