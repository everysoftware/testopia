import datetime

from sqlalchemy import Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True, unique=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="cascade"))

    text: Mapped[str]

    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    task = relationship(
        "Task", back_populates="comment", lazy="selectin", uselist=False
    )
