import os

from dotenv import load_dotenv

from app.cache.config import CacheSettings
from app.db.config import DBSettings
from app.schemas import BaseSettings
from app.users.config import AuthSettings

if not os.getenv("DOCKER_MODE"):
    load_dotenv(".env")


class AppSettings(BaseSettings):
    bot_token: str

    auth: AuthSettings = AuthSettings()
    db: DBSettings = DBSettings()
    cache: CacheSettings = CacheSettings()


settings = AppSettings()
