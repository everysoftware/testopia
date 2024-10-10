from pydantic import (
    Field,
    computed_field,
)

from app.db.schemas import IDModel, TimestampModel
from app.schemas import BackendBase


class UserBase(BackendBase):
    pass


class UserRead(UserBase, IDModel, TimestampModel):
    first_name: str | None = None
    last_name: str | None = None
    telegram_id: int
    is_active: bool
    is_superuser: bool

    @computed_field  # type: ignore[prop-decorator]
    @property
    def display_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        return ""


class UserCreate(UserBase):
    telegram_id: int
    first_name: str = Field(examples=["John"])
    last_name: str | None = Field(None, examples=["Doe"])


class UserUpdate(BackendBase):
    telegram_id: int
    first_name: str | None = None
    last_name: str | None = None
