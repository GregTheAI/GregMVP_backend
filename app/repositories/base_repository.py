from typing import Type, TypeVar, Generic, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import as_declarative

from app.dtos.page_result import PageResult

T = TypeVar("T")  # SQLAlchemy model type


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_all(self, filters: Optional[dict] = None, page_index: int = 1, page_size: int = 10) -> PageResult:
        query = select(self.model)
        if filters:
            for field, value in filters.items():
                query = query.where(getattr(self.model, field) == value)
        total_count = (await self.db.execute(select([self.model]).where(
            *(getattr(self.model, field) == value for field, value in (filters or {}).items())
        ))).scalars().count() if filters else (await self.db.execute(select(self.model))).scalars().count()
        result = await self.db.execute(query.offset((page_index - 1) * page_size).limit(page_size))
        data = result.scalars().all()
        pages = (total_count + page_size - 1) // page_size if page_size else 1
        return PageResult(data, page_index, page_size, total_count, pages)

    async def get_by_id(self, _id: Any) -> Optional[T]:
        result = await self.db.get(self.model, id)
        return result

    async def get_by_field(self, field_name: str, value) -> T | None:
        field = getattr(self.model, field_name, None)
        if field is None:
            raise AttributeError(f"{self.model.__name__} has no field '{field_name}'")

        stmt = select(self.model).where(field == value)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def exists_by_field(self, field_name: str, value) -> bool:
        field = getattr(self.model, field_name, None)
        if field is None:
            raise AttributeError(f"{self.model.__name__} has no field '{field_name}'")

        stmt = select(field).where(field == value).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def create(self, entity: dict) -> T:
        db_obj = self.model(**entity)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: T) -> T:
        # for field, value in entity.items():
        #     setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, entity: T) -> None:
        await self.db.delete(entity)
        await self.db.commit()
