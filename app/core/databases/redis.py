from functools import lru_cache
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import redis.asyncio as redis
from app.core.settings import get_settings

settings = get_settings()


@lru_cache()
def get_redis_pool() -> redis.ConnectionPool:
    return redis.ConnectionPool.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
        max_connections=10,
    )


@asynccontextmanager
async def acquire_redis() -> AsyncGenerator[redis.Redis, None]:
    client = redis.Redis(connection_pool=get_redis_pool())
    try:
        yield client
    finally:
        await client.close()
