from app.cache.connection import redis_client


async def ping_redis() -> None:
    await redis_client.ping()
