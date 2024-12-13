from typing import Any

from app.base.pagination import Pagination, Page
from app.base.types import UUID
from app.base.use_case import UseCase
from app.projects.models import Project
from app.projects.repositories import UserProjectSpecification
from app.db.dependencies import UOWDep
from app.users.models import User


class ProjectUseCases(UseCase):
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def get_many(
        self, user: User, pagination: Pagination, **kwargs: Any
    ) -> Page[Project]:
        return await self.uow.projects.get_many(
            UserProjectSpecification(user.id), pagination, **kwargs
        )

    async def create(self, **kwargs: Any) -> Project:
        checklist = Project(**kwargs)
        await self.uow.projects.add(checklist)
        await self.uow.commit()
        return checklist

    async def get_one(self, checklist_id: UUID) -> Project:
        return await self.uow.projects.get_one(checklist_id)
