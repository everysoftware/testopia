from typing import Any

from app.db.schemas import PageParams, Page
from app.db.types import ID
from app.devices.schemas import DeviceRead
from app.service import Service


class DeviceService(Service):
    async def get_many(
        self, params: PageParams, *, user_id: ID | None = None
    ) -> Page[DeviceRead]:
        return await self.uow.devices.get_many(params, user_id=user_id)

    async def create(self, **kwargs: Any) -> DeviceRead:
        return await self.uow.devices.create(**kwargs)

    async def get_one(self, device_id: ID) -> DeviceRead:
        return await self.uow.devices.get_one(device_id)
