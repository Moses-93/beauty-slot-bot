from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.config import get_settings


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    settings = get_settings()
    engine = create_async_engine(settings.database_url())
    return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
