import datetime

from sqlalchemy import Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Device(Base):
    __tablename__ = 'devices'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    name: Mapped[str]

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    user = relationship(
        'User',
        back_populates='devices',
        lazy='selectin',
        uselist=False
    )
