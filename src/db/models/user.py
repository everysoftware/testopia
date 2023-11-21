import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import Identity

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Identity(), unique=True)
    user_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    first_name: Mapped[str]

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    last_name: Mapped[Optional[str]]
    language_code: Mapped[Optional[str]]
    username: Mapped[Optional[str]]

    products = relationship(
        'Product',
        back_populates='owner',
        lazy='selectin',
        order_by='Product.name'
    )
    devices = relationship(
        'Device',
        back_populates='user',
        lazy='selectin',
        order_by='Device.name'
    )
    tasks = relationship(
        'Task',
        back_populates='user',
        lazy='selectin',
        order_by='Task.name'
    )
    checklists = relationship(
        'Checklist',
        back_populates='user',
        lazy='selectin'
    )
