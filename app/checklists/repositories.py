from sqlalchemy import select

from app.checklists.models import ChecklistOrm
from app.checklists.schemas import ChecklistRead
from app.db.repository import AlchemyRepository
from app.db.schemas import Page, PageParams
from app.db.types import ID


class ChecklistRepository(AlchemyRepository[ChecklistOrm, ChecklistRead]):
    model_type = ChecklistOrm
    schema_type = ChecklistRead

    async def get_many(
        self, params: PageParams, *, user_id: ID | None = None
    ) -> Page[ChecklistRead]:  # noqa
        stmt = select(self.model_type)
        if user_id is not None:
            stmt = stmt.where(self.model_type.user_id == user_id)
        stmt = self.build_pagination_query(params, stmt)
        result = await self.session.scalars(stmt)
        return self.validate_page(result)
