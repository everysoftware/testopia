from app.base.schemas import BaseSettings


class StatsSettings(BaseSettings):
    stats_dir: str = "temp"


stats_settings = StatsSettings()
