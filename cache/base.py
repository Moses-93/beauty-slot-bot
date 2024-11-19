from aiocache import caches, Cache
from aiocache.plugins import HitMissRatioPlugin
import logging

logger = logging.getLogger(__name__)

caches.set_config({
    "default": {
        "cache": "aiocache.SimpleMemoryCache",  # Простий кеш
        "ttl": 1800,
        "plugins": [
            {"class": "aiocache.plugins.HitMissRatioPlugin"}
        ]
    }
})


class BaseCache:

    def __init__(self, caches_name="default") -> None:
        self._cache: Cache = caches.get(caches_name)

    async def get_cache(self, key:str):
        if key:
            try:
                return await self._cache.get(key)
            except KeyError:
                logger.error(f"Помилка доступу до кешу: {key}")
        return await self._cache.get("global_dict")

    async def set_cache(self, key:str|int, value):
        await self._cache.set(key, value)
        logger.info(f"Кеш оновлено: {key} -> {value}")
    
    async def delete_cache(self, key:str|int):
        await self._cache.delete(key)
        logger.debug(f"Ключ видалено з кешу: {key}")

            