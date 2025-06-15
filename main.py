from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute

import asyncio

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1 import api_router
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

app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET_KEY)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


def run_migrations():
    """Run Alembic migrations in async context"""
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


run_migrations()
