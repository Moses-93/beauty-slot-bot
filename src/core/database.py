from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.config import get_settings

engine = create_async_engine(get_settings().database_url())
Session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
