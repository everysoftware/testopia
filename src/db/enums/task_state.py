import enum


class TaskState(enum.IntEnum):
    PASSED = 1
    FAILED = 2
    IMPOSSIBLE = 3
    SKIPPED = 4
