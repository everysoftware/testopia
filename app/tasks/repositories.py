import datetime

from sqlalchemy import select, func

from app.db.repository import AlchemyRepository
from app.db.schemas import PageParams, Page
from app.db.types import ID
from app.tasks.models import TaskOrm
from app.tasks.schemas import TaskRead, TaskStatus


class TaskRepository(AlchemyRepository[TaskOrm, TaskRead]):
    model_type = TaskOrm
    schema_type = TaskRead

    async def get_many_by_checklist(self, params: PageParams, *, checklist_id: ID) -> Page[TaskRead]:
        stmt = select(self.model_type).where(self.model_type.checklist_id == checklist_id)
        stmt = self.build_pagination_query(params, stmt)
        result = await self.session.scalars(stmt)
        return self.validate_page(result)

    async def get_status_stats(self, user_id: ID) -> dict[TaskStatus, int]:
        stmt = (
            select(self.model_type.status, func.count(self.model_type.status))
            .where(self.model_type.user_id == user_id)
            .group_by(self.model_type.status)
        )
        result = await self.session.execute(stmt)
        return {status: count for status, count in result.all()}

    async def get_date_stats(self, user_id: ID, from_dt: datetime.datetime, to_dt: datetime.datetime) -> dict[
        datetime.datetime, int]:
        # Получаем дату года назад от текущей даты
        # now = datetime.datetime.utcnow()
        # year_ago = now - datetime.timedelta(days=365)

        # Запрос на получение количества выполненных задач по дням за последний год
        stmt = (
            select(
                func.count(self.model_type.id),  # Считаем количество задач
                func.date(self.model_type.updated_at),
            )
            .where(
                self.model_type.user_id == user_id,  # Фильтруем по ID пользователя
                self.model_type.status == TaskStatus.passed,  # Фильтруем по состоянию задачи
                (from_dt >= self.model_type.updated_at) &
                (self.model_type.updated_at >= to_dt),  # Фильтруем задачи, обновленные за период
            )
            .group_by(func.date(self.model_type.updated_at))  # Группируем по дню обновления
        )
        result = await self.session.execute(stmt)
        return {date: count for count, date in result.all()}
