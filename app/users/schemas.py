from pydantic import (
    Field,
)

from app.base.schemas import BaseModel


class UserCreate(BaseModel):
    telegram_id: int
    first_name: str = Field(examples=["John"])
    last_name: str | None = Field(None, examples=["Doe"])


class UserUpdate(BaseModel):
    telegram_id: int
    first_name: str | None = None
    last_name: str | None = None
