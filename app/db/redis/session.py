from typing import Optional
import asyncio
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

    async def keys(self, pattern):
        return await self._cached_redis.keys(pattern)

    async def close(self):
        self._cached_redis.close()
        await self._cached_redis.wait_closed()


redis = RedisCache(str(config.REDIS_URL))


def get_redis() -> Redis:
    redis_url = str(config.REDIS_URL)
    redis = RedisCache(redis_url)
    return redis
