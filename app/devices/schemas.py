from app.db.schemas import IDModel, TimestampModel
from app.db.types import ID
from app.schemas import BackendBase


class DeviceRead(IDModel, TimestampModel):
    user_id: ID
    name: str
