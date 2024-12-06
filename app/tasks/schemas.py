import enum

from app.db.schemas import TimestampModel, IDModel
from app.db.types import ID


class TaskStatus(enum.StrEnum):
    to_do = enum.auto()
    in_progress = enum.auto()
    done = enum.auto()


class TestStatus(enum.StrEnum):
    no_status = enum.auto()
    passed = enum.auto()
    failed = enum.auto()
    impossible = enum.auto()
    skipped = enum.auto()


class TaskRead(IDModel, TimestampModel):
    user_id: ID
    checklist_id: ID
    name: str
    status: TaskStatus
    test_status: TestStatus
    description: str | None
    report_url: str | None
