from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseOrm
from app.db.mixins import IDMixin, TimestampMixin
from app.tasks.schemas import TaskStatus


class TaskOrm(BaseOrm, IDMixin, TimestampMixin):
    __tablename__ = "tasks"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )
    checklist_id: Mapped[int] = mapped_column(
        ForeignKey("checklists.id", ondelete="cascade")
    )
    name: Mapped[str]
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.skipped)
    report_url: Mapped[str | None]
    comment: Mapped[str | None]
