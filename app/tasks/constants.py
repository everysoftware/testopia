from app.tasks.schemas import TaskStatus, TestStatus

TASK_STATUSES = {
    TaskStatus.to_do: {
        "emoji": "🔵",
        "name": "to_do",
        "text": "К выполнению",
        "color": "mediumturquoise",
    },
    TaskStatus.in_progress: {
        "emoji": "🟡",
        "name": "in_progress",
        "text": "Выполняется",
        "color": "orange",
    },
    TaskStatus.done: {
        "emoji": "🟢",
        "name": "done",
        "text": "Выполнено",
        "color": "mediumseagreen",
    },
}

TEST_STATUSES = {
    TestStatus.no_status: {
        "emoji": "⚪",
        "name": "no_status",
        "text": "Нет статуса",
        "color": "mediumturquoise",
    },
    TestStatus.passed: {
        "emoji": "🟢",
        "name": "passed",
        "text": "Пройден",
        "color": "mediumseagreen",
    },
    TestStatus.failed: {
        "emoji": "🔴",
        "name": "failed",
        "text": "Не пройден",
        "color": "lightcoral",
    },
    TestStatus.impossible: {
        "emoji": "🟡",
        "name": "impossible",
        "text": "Невозможно пройти",
        "color": "orange",
    },
    TestStatus.skipped: {
        "emoji": "🔵",
        "name": "skipped",
        "text": "Пропущен",
        "color": "mediumturquoise",
    },
}

TASK_STATUS_CB_DATA = {
    "to_do": TaskStatus.to_do,
    "in_progress": TaskStatus.in_progress,
    "done": TaskStatus.done,
}

TEST_STATUSES_CB_DATA = {
    "passed": TestStatus.passed,
    "failed": TestStatus.failed,
    "impossible": TestStatus.impossible,
    "skipped": TestStatus.skipped,
    "no_status": TestStatus.no_status,
}
