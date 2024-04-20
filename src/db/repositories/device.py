from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import Device


class DeviceRepo(Repository[Device]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Device, session=session)

    def new(
        self,
        user_id: int,
        name: str,
    ) -> Device:
        obj = Device(
            user_id=user_id,
            name=name,
        )
        self.session.add(obj)
        return obj
