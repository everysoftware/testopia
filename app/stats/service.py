import datetime

from app.db.types import ID
from app.service import Service
from app.stats.heat_map import paint_heat_map
from app.stats.pie import paint_pie_plot


class StatsService(Service):
    async def plot_by_statuses(self, user_id: ID) -> str:
        stats = await self.uow.tasks.get_test_stats(user_id)
        return paint_pie_plot(stats, title="Тестов за все время: {count}")

    async def plot_by_days(
        self, user_id: ID, from_dt: datetime.datetime, to_dt: datetime.datetime
    ) -> str:
        stats = await self.uow.tasks.get_stats(user_id, from_dt, to_dt)
        return paint_heat_map(
            stats, title="Выполненных задач за последний год: {count}"
        )
