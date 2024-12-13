from app.base.schemas import BaseSettings


class AISettings(BaseSettings):
    gigachat_client_id: str
    gigachat_client_secret: str


ai_settings = AISettings()
