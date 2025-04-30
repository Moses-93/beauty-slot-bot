import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from functools import lru_cache
import os

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    telegram_token: str
    pg_user: str
    pg_password: str
    pg_db: str
    pg_host: str = "localhost"
    pg_port: str = "5432"

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def database_url(self, driver: Literal["asyncpg", "psycopg2"] = "asyncpg") -> str:
        """Generates a URL to connect to the database."""
        url = f"postgresql+{driver}://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"
        logger.info(f"{url=}")
        return url


@lru_cache()
def get_settings() -> Settings:
    """
    Returns an instance of the settings (Singleton).
    """
    return Settings()
