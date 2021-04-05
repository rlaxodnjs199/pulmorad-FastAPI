from typing import AsyncIterator
import asyncio
from aioredis import create_redis_pool, Redis
from app import config


async def init_redis_pool(host: str) -> AsyncIterator[Redis]:
    host = str(config.REDIS_URL)
    pool = await create_redis_pool(f'redis://{host}')
    yield pool
    pool.close()
    await pool.wait_closed()


async def insert_key(redis_conn: Redis, key: str, value: str):
    await redis_conn.set(key, value)
    return await redis_conn.get(key, encoding='utf-8')


async def get_key(redis_conn: Redis, key: str):
    return await redis_conn.get(key, encoding='utf-8')
