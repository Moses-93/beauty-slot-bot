from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from os import getenv

load_dotenv()

PG_USER = getenv("POSTGRES_USER")
PG_PASSWORD = getenv("POSTGRES_PASSWORD")
PG_DB = getenv("POSTGRES_DB")
PG_HOST = getenv("POSTGRES_HOST")
PG_PORT = getenv("POSTGRES_PORT")

DATABASE_URL = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)

engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
