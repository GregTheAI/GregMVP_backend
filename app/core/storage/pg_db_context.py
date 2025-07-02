from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import get_settings


settings = get_settings()
# DATABASE_URL = settings.sqlalchemy_database_uri

engine = create_async_engine(settings.sqlalchemy_database_uri, echo=True, future=True)

DbContext = async_sessionmaker(engine, expire_on_commit=False)
