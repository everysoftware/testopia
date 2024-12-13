from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.models import Entity
from app.base.types import UUID
from app.tasks.models import Task

if TYPE_CHECKING:
    from app.users.models import User
    from app.workspaces.models import Workspace


class Project(Entity):
    __tablename__ = "projects"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )
    workspace_id: Mapped[UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="cascade")
    )
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="")
    stack: Mapped[str] = mapped_column(default="")

    user: Mapped[User] = relationship(back_populates="projects")
    workspace: Mapped[Workspace] = relationship(back_populates="projects")
    tasks: Mapped[list[Task]] = relationship(back_populates="project")
