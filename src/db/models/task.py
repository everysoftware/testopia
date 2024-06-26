import datetime

from sqlalchemy import Identity, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..enums.task_state import TaskState


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="cascade")
    )
    checklist_id: Mapped[int] = mapped_column(
        ForeignKey("checklists.id", ondelete="cascade")
    )

    name: Mapped[str]
    state: Mapped[TaskState] = mapped_column(Enum(TaskState), default=TaskState.SKIPPED)

    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    checklist = relationship(
        "Checklist", back_populates="tasks", lazy="selectin", uselist=False
    )
    user = relationship("User", back_populates="tasks", lazy="selectin", uselist=False)
    report = relationship(
        "Report", back_populates="task", lazy="selectin", uselist=False
    )
    comment = relationship(
        "Comment", back_populates="task", lazy="selectin", uselist=False
    )
