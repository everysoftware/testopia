from app.db.schemas import IDModel, TimestampModel
from app.db.types import ID


class ChecklistRead(IDModel, TimestampModel):
    user_id: ID
    product: str
    name: str
