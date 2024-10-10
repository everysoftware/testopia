from app.schemas import BaseSettings


class AuthSettings(BaseSettings):
    admin_telegram_id: int | None = None
