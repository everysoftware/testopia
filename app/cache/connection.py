from redis.asyncio import Redis

from app.cache.config import cache_settings

redis_client = Redis.from_url(cache_settings.redis_url)
