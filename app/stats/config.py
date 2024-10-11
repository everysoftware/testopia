from app.schemas import BaseSettings


class StatsSettings(BaseSettings):
    stats_dir: str = "stats"
