import datetime
from typing import Any

from app.db.schemas import PageParams, Page
from app.db.types import ID
from app.service import Service
from app.stats.heat_map import paint_heat_map
from app.stats.pie import paint_pie_plot
from app.tasks.schemas import TaskRead


class TaskService(Service):
    async def get_many(
        self, checklist_id: ID, params: PageParams
    ) -> Page[TaskRead]:
        return await self.uow.tasks.get_many_by_checklist(
            params, checklist_id=checklist_id
        )

    async def create(self, **kwargs: Any) -> TaskRead:
        return await self.uow.tasks.create(**kwargs)

    async def get_one(self, task_id: ID) -> TaskRead:
        return await self.uow.tasks.get_one(task_id)

    async def update(self, task_id: ID, **kwargs: Any) -> TaskRead:
        return await self.uow.tasks.update(task_id, **kwargs)

    async def plot_by_statuses(self, user_id: ID) -> str:
        stats = await self.uow.tasks.get_status_stats(user_id)
        return paint_pie_plot(stats, title="Всего задач: {count}")

    async def plot_by_days(
        self, user_id: ID, from_dt: datetime.datetime, to_dt: datetime.datetime
    ) -> str:
        stats = await self.uow.tasks.get_date_stats(user_id, from_dt, to_dt)
        return paint_heat_map(stats, title="Всего выполненных: {count}")
