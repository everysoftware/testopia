from app.schemas import BaseSettings


class CacheSettings(BaseSettings):
    redis_url: str = "redis://default+changethis@localhost:6379/0"
    state_ttl: int | None = None
    data_ttl: int | None = None
