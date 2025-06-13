from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

DATABASE_URL = settings.sqlalchemy_database_uri

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

DbContext = async_sessionmaker(engine, expire_on_commit=False)
