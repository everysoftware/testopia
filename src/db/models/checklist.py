import datetime

from sqlalchemy import Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Checklist(Base):
    __tablename__ = 'checklists'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True, unique=True)
    name: Mapped[str]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

    product = relationship(
        'Product',
        back_populates='checklists',
        lazy='selectin'
    )
    tasks = relationship(
        'Task',
        back_populates='checklist',
        lazy='joined',
        order_by='desc(Task.created_at)'
    )
