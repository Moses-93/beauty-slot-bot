from typing import List, Optional, Type, Union, TypeVar, Generic
from sqlalchemy import Delete, Select, Update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):

    def __init__(
        self, factory_session: async_sessionmaker[AsyncSession], model: Type[ModelType]
    ):
        """Base repository for CRUD operations.

        Args:
            factory_session (async_sessionmaker[AsyncSession]): Asynchronous factory_session to perform the operation
            model (DeclarativeBase): SQLAlchemy model class
        """
        self.factory_session = factory_session
        self.model = model

    async def create(self, **kwargs) -> ModelType:
        """
        Creates a new entry in the database.

        Returns:
            ModelType: Created model object.
        """
        async with self.factory_session() as session:
            obj = self.model(**kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)

        return obj

    async def read(
        self, query: Select, single: bool = False
    ) -> Union[Optional[ModelType], List[ModelType]]:
        """
        Executes a SELECT query to the database.

        Args:
            query (Select): SQLAlchemy Select-query.
            single (bool, optional): If True, returns a single object (or None), otherwise a list. Defaults to False.

        Returns:
            Union[Optional[ModelType], List[ModelType]]: One model object (single=True) or a list of objects (single=False).
        """
        async with self.factory_session() as session:
            result = await session.execute(query)

        return result.scalars().first() if single else result.scalars().all()

    async def read_by_id(self, id: int) -> Optional[ModelType]:
        """
        Retrieves a single object by its ID.

        Args:
            id (int): The ID of the object to retrieve.

        Returns:
            Optional[ModelType]: The object with the specified ID, or None if not found.
        """
        async with self.factory_session() as session:
            return await session.get(self.model, id)

    async def update(self, query: Update) -> bool:
        """
        Executes an UPDATE query to the database.

        Args:
            query (Update): SQLAlchemy Update-query.

        Returns:
            bool: A Boolean value indicating whether changes have occurred in the database.
        """
        async with self.factory_session() as session:
            result = await session.execute(query)
            await session.commit()

        return result.rowcount > 0

    async def delete(self, query: Delete) -> bool:
        """
        Executes a DELETE query to the database.

        Args:
            query (Delete): SQLAlchemy Delete-query.

        Returns:
            bool: A Boolean value indicating whether changes have occurred in the database.
        """
        async with self.factory_session() as session:
            result = await session.execute(query)
            await session.commit()

        return result.rowcount > 0

    async def delete_by_id(self, id: int) -> bool:
        """
        Deletes an object by its ID.

        Args:
            id (int): The ID of the object to delete.

        Returns:
            bool: A Boolean value indicating whether changes have occurred in the database.
        """
        async with self.factory_session() as session:
            obj = await session.get(self.model, id)
            if obj is None:
                return False
            await session.delete(obj)
            await session.commit()
            return True
