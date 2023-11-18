import datetime

from sqlalchemy import Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Report(Base):
    __tablename__ = 'reports'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True, unique=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))

    url: Mapped[str]

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
