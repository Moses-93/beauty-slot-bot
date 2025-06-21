from punq import Container
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .persistence.repositories import container as di_repo
from .persistence.db_config import get_sessionmaker


def register(container: Container) -> None:
    """
    Register all repositories in the container.
    """
    container.register(async_sessionmaker[AsyncSession], instance=get_sessionmaker())
    di_repo.register(container)
