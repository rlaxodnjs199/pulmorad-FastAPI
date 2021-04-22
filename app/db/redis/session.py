from typing import Optional
import asyncio
from typing import AsyncIterator
from aioredis import create_redis_pool, Redis
from app import config


class RedisCache:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self._cached_redis: Optional[Redis] = None

    async def init_redis_pool(self):
        print("Initializing Redis")
        self._cached_redis = await create_redis_pool("redis://localhost:6379/0?encoding=utf-8")

    async def set(self, key: str, value: str):
        if self._cached_redis:
            return await self._cached_redis.set(key, value)
        else:
            AssertionError

    async def get(self, key: str):
        if self._cached_redis:
            return await self._cached_redis.get(key)
        else:
            AssertionError

    async def delete(self, key: str):
        if self._cached_redis:
            return await self._cached_redis.delete(key)
        else:
            AssertionError

    async def keys(self, pattern):
        return await self._cached_redis.keys(pattern)

    async def terminate(self):
        print("Terminating Redis")
        if self._cached_redis is not None:
            self._cached_redis.close()
            await self._cached_redis.wait_closed()
            self._cached_redis = None


redis = RedisCache(str(config.REDIS_URL))
