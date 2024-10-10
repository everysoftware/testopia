import enum

from app.db.schemas import TimestampModel, IDModel
from app.db.types import ID


class TaskStatus(enum.StrEnum):
    passed = enum.auto()
    failed = enum.auto()
    impossible = enum.auto()
    skipped = enum.auto()


class TaskRead(IDModel, TimestampModel):
    user_id: ID
    checklist_id: ID
    name: str
    status: TaskStatus
    report_url: str | None
    comment: str | None
