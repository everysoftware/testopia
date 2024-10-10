from sqlalchemy import Boolean
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import BaseOrm
from app.db.mixins import TimestampMixin, IDMixin


class UserOrm(BaseOrm, IDMixin, TimestampMixin):
    __tablename__ = "users"

    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    telegram_id: Mapped[int] = mapped_column(index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
