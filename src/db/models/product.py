import datetime

from sqlalchemy import Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True, unique=True)
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey(
        'users.user_id',
        ondelete='cascade'
    ))

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    owner = relationship(
        'User',
        back_populates='products',
        lazy='selectin',
        uselist=False
    )

    checklists = relationship(
        'Checklist',
        back_populates='product',
        lazy='selectin',
        order_by='Checklist.name'
    )
