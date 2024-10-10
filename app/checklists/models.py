from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseOrm
from app.db.mixins import TimestampMixin, IDMixin


class ChecklistOrm(BaseOrm, IDMixin, TimestampMixin):
    __tablename__ = "checklists"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )
    name: Mapped[str]
    product: Mapped[str]
