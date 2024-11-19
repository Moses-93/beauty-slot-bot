import asyncio
from .base import BaseCache


class UserCache(BaseCache):
    def __init__(self,  cache_name="default"):
        super().__init__(cache_name)

    async def init_user(self, user_id:int):
        if not await self._cache.exists(user_id):
            await self.set_cache(user_id, {})

    async def get_user_cache(self, user_id, *keys):
        user_data = await self.get_cache(key=user_id)
        if not keys:
            return user_data
        return tuple(user_data.get(key) for key in keys)
        
    async def set_user_cache(self, user_id: int, **kwargs):
        await self.init_user(user_id)
        user_data = await self.get_cache(key=user_id)
        user_data.update(kwargs)
        await self.set_cache(user_id, user_data)
    
    async def clear_user_cache(self, user_id: int, *save_keys):
        user_data = await self.get_cache(key=user_id)
        if not user_data:
            return
        if save_keys:
            user_data = {key: value for key, value in user_data.items() if key in save_keys}
            await self.set_cache(user_id, user_data)
        else:
            await self.delete_cache(key=user_id)


class RequestCache(BaseCache):
    def __init__(self, cache_name="default") -> None:
        super().__init__(cache_name)

    async def get_request(self, key:str=None, keys:list[str]=None):
        if key:
            return await self.get_cache(key)
        return await asyncio.gather(*(self.get_cache(k) for k in keys))
        
    async def set_request(self, key:str=None, value=None, **kwargs):
        if kwargs:
            await asyncio.gather(*(self.set_cache(k, v) for k, v in kwargs.items()))
        await self.set_cache(key=key, value=value)
    
    async def clear_request(self, key:str=None, keys:list[str]=None):
        if keys:
            await asyncio.gather(*(self.delete_cache(k) for k in keys))
        await self.delete_cache(key=key)

user_cache = UserCache()
request_cache = RequestCache()