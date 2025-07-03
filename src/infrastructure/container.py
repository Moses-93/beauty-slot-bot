from punq import Container
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .persistence.repositories import container as di_repo
from .event_bus import container as di_event_bus
from .telegram import container as di_telegram
from .persistence.db_config import get_sessionmaker


def register(container: Container) -> None:
    """
    Register all repositories in the container.
    """
    container.register(async_sessionmaker[AsyncSession], instance=get_sessionmaker())
    di_repo.register(container)
    di_event_bus.register(container)
    di_telegram.register(container)
