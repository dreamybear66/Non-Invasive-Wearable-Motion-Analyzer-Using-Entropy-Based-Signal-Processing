import redis.asyncio as redis
import os
import json

redis_client = None

async def init_redis():
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

async def close_redis():
    if redis_client:
        await redis_client.close()

def get_redis():
    return redis_client
