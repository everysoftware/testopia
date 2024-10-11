from typing import Any

from app.db.schemas import PageParams, Page
from app.db.types import ID
from app.service import Service
from app.tasks.schemas import TaskRead


class TaskService(Service):
    async def get_many(self, checklist_id: ID, params: PageParams) -> Page[TaskRead]:
        return await self.uow.tasks.get_many_by_checklist(params, checklist_id=checklist_id)

    async def create(self, **kwargs: Any) -> TaskRead:
        return await self.uow.tasks.create(**kwargs)

    async def get_one(self, task_id: ID) -> TaskRead:
        return await self.uow.tasks.get_one(task_id)

    async def update(self, task_id: ID, **kwargs: Any) -> TaskRead:
        return await self.uow.tasks.update(task_id, **kwargs)
