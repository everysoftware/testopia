from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseOrm
from app.db.mixins import IDMixin, TimestampMixin


class DeviceOrm(BaseOrm, IDMixin, TimestampMixin):
    __tablename__ = "devices"

    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )
