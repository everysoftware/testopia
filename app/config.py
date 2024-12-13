from app.base.schemas import BaseSettings


class BotSettings(BaseSettings):
    bot_token: str


bot_settings = BotSettings()
