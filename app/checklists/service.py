from typing import Any

from app.checklists.schemas import ChecklistRead
from app.db.schemas import Page, PageParams
from app.db.types import ID
from app.service import Service


class ChecklistService(Service):
    async def get_many(
        self, params: PageParams, **kwargs: Any
    ) -> Page[ChecklistRead]:
        return await self.uow.checklists.get_many(params, **kwargs)

    async def create(self, **kwargs: Any) -> ChecklistRead:
        return await self.uow.checklists.create(**kwargs)

    async def get_one(self, checklist_id: ID) -> ChecklistRead:
        return await self.uow.checklists.get_one(checklist_id)
