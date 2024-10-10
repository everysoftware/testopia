from app.tasks.schemas import TaskStatus

TASK_STATUSES = {
    TaskStatus.passed: {"emoji": "🟢", "name": "passed", "text": "Пройден", "color": "mediumseagreen"},
    TaskStatus.failed: {"emoji": "🔴", "name": "failed", "text": "Не пройден", "color": "lightcoral"},
    TaskStatus.impossible: {"emoji": "🟡", "name": "impossible", "text": "Невозможно пройти", "color": "orange"},
    TaskStatus.skipped: {"emoji": "🔵", "name": "skipped", "text": "Пропущен", "color": "mediumturquoise"},

}

TASK_STATUS_CB_DATA = {
    "passed": TaskStatus.passed,
    "failed": TaskStatus.failed,
    "impossible": TaskStatus.impossible,
    "skipped": TaskStatus.skipped,

}
