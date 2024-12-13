from dataclasses import dataclass
from typing import Any

from app.base.specification import ISpecification
from app.base.types import UUID
from app.db.repository import SQLAlchemyRepository
from app.projects.models import Project


@dataclass
class UserProjectSpecification(ISpecification):
    user_id: UUID

    def apply(self, stmt: Any) -> Any:
        return stmt.where(Project.user_id == self.user_id)


class ProjectRepository(SQLAlchemyRepository[Project]):
    model_type = Project
