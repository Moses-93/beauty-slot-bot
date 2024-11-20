import asyncio
from .base import AioCacheAdapter, ICache


class UserCache:
    def __init__(self, cache: ICache):
        self.cache = cache

    async def init_user(self, user_id: int):
        if not await self.cache.get(user_id):
            await self.cache.set(user_id, {})

    async def get_user_cache(self, user_id:int, *keys):
        user_data = await self.cache.get(key=user_id)
        if not keys:
            return user_data
        return tuple(user_data.get(key) for key in keys)

    async def set_user_cache(self, user_id: int, **kwargs):
        await self.init_user(user_id)
        user_data = await self.cache.get(key=user_id)
        user_data.update(kwargs)
        await self.cache.set(user_id, user_data)

    async def clear_user_cache(self, user_id: int, *save_keys:str):
        if save_keys:
            user_data = await self.cache.get(key=user_id)
            user_data = {
                key: value for key, value in user_data.items() if key in save_keys
            }
            await self.cache.set(user_id, user_data)
        else:
            await self.cache.delete(key=user_id)


class RequestCache:
    def __init__(self, cache: ICache) -> None:
        self.cache = cache

    async def get_request(self, key: str = None, keys: list[str] = None):
        if key:
            return await self.cache.get(key)
        return await asyncio.gather(*(self.cache.get(k) for k in keys))

    async def set_request(self, key: str = None, value=None, **kwargs):
        if kwargs:
            await asyncio.gather(*(self.cache.set(k, v) for k, v in kwargs.items()))
        await self.cache.set(key=key, value=value)

    async def clear_request(self, key: str = None, keys: list[str] = None):
        if keys:
            await asyncio.gather(*(self.cache.delete(k) for k in keys))
        await self.cache.delete(key=key)


cache = AioCacheAdapter()
user_cache = UserCache(cache)
request_cache = RequestCache(cache)
