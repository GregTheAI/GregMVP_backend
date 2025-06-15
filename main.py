from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute

import asyncio

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1 import api_router
from app.core.bootstrap import Bootstrap
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    swagger_ui_init_oauth={},
    swagger_ui_oauth_scope=["persistAuthorization", True]
)

Bootstrap(app).run()

# @app.on_event("startup")
# async def on_startup():
#     await asyncio.run(Bootstrap(app).run_database_migrations())