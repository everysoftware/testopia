import datetime
import enum

from sqlalchemy import Identity, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TaskState(enum.IntEnum):
    PASSED = 1
    FAILED = 2
    IMPOSSIBLE = 3
    SKIPPED = 4


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    task_list_id: Mapped[int] = mapped_column(ForeignKey('task_lists.id'))

    name: Mapped[str]
    state: Mapped[TaskState] = mapped_column(Enum(TaskState), default=TaskState.SKIPPED)

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    task_list = relationship(
        'TaskList',
        back_populates='tasks',
        lazy='selectin'
    )
