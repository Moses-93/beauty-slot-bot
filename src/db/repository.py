import logging

from typing import Type

from sqlalchemy import and_, delete, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.declarative import DeclarativeMeta

from .config import AsyncSession, async_sessionmaker
from .interfaces import BaseCRUD

from src.decorators.cache_tools import clear_cache


logger = logging.getLogger(__name__)


class ImplementationCRUD(BaseCRUD):

    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session = session

    @clear_cache
    async def create(self, model: Type[DeclarativeMeta], **kwargs: dict):
        logger.info(f"Запис даних в модель {model.__name__}, аргументи: {kwargs}")
        async with self.session() as session:
            new_item = model(**kwargs)
            session.add(new_item)
            await session.commit()
            await session.refresh(new_item)
            return new_item

    async def read(
        self,
        model: Type[DeclarativeMeta],
        relations: tuple = None,
        expressions: tuple = None,
        **filters,
    ):
        logger.info(f"Читання даних з моделі {model.__name__}, фільтри: {filters}")
        async with self.session() as session:
            query = select(model)
            if relations:
                query = query.options(*[selectinload(rel) for rel in relations])
            if expressions is not None:
                print(expressions)
                query = query.filter(and_(*expressions))
            if filters:
                query = query.filter_by(**filters)
            try:
                result = await session.execute(query)
            except Exception as e:
                logger.error(f"Помилка під час читання з моделі {model.__name__}: {e}")
                return []
            return result.scalars().all()

    @clear_cache
    async def update(self, model: Type[DeclarativeMeta], *expressions, **kwargs):
        logger.info(f"Оновлення даних в моделі: {model.__name__}, аргументи: {kwargs}")
        async with self.session() as session:
            stmt = update(model).where(*expressions).values(**kwargs)
            await session.execute(stmt)
            await session.commit()
            return True

    @clear_cache
    async def delete(self, model: Type[DeclarativeMeta], **kwargs):
        logger.info(f"Видалення даних з моделі: {model.__name__}, аргументи: {kwargs}.")
        async with self.session() as session:
            stmt = delete(model).filter_by(**kwargs)
            await session.execute(stmt)
            await session.commit()
            return True
