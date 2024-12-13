import enum


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
