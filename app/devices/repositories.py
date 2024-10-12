from sqlalchemy import select

from app.db.repository import AlchemyRepository
from app.db.schemas import PageParams, Page
from app.devices.models import DeviceOrm
from app.devices.schemas import DeviceRead
from app.db.types import ID


class DeviceRepository(AlchemyRepository[DeviceOrm, DeviceRead]):
    model_type = DeviceOrm
    schema_type = DeviceRead

    async def get_many(
        self, params: PageParams, *, user_id: ID | None = None
    ) -> Page[DeviceRead]:  # noqa
        stmt = select(self.model_type)
        if user_id is not None:
            stmt = stmt.where(self.model_type.user_id == user_id)
        stmt = self.build_pagination_query(params, stmt)
        result = await self.session.scalars(stmt)
        return self.validate_page(result)
