from typing import AsyncGenerator
from app.core.storage.pg_db_context import DbContext


async def get_pg_database() -> AsyncGenerator:
    async with DbContext() as session:
        yield session
