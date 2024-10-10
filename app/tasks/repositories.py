from sqlalchemy import select

from app.db.repository import AlchemyRepository
from app.db.schemas import PageParams, Page
from app.db.types import ID
from app.tasks.models import TaskOrm
from app.tasks.schemas import TaskRead


class TaskRepository(AlchemyRepository[TaskOrm, TaskRead]):
    model_type = TaskOrm
    schema_type = TaskRead

    async def get_many_by_checklist(self, params: PageParams, *, checklist_id: ID) -> Page[TaskRead]:
        stmt = select(self.model_type).where(self.model_type.checklist_id == checklist_id)
        stmt = self.build_pagination_query(params, stmt)
        result = await self.session.scalars(stmt)
        return self.validate_page(result)
