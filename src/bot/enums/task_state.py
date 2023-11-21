from db.enums import TaskState

TASK_STATE_EMOJI = {
    TaskState.SKIPPED: '🔵',
    TaskState.FAILED: '🔴',
    TaskState.PASSED: '🟢',
    TaskState.IMPOSSIBLE: '🟡',
}

TASK_STATE_TRANSLATIONS = {
    TaskState.SKIPPED: 'Пропущен',
    TaskState.FAILED: 'Не пройден',
    TaskState.IMPOSSIBLE: 'Невозможно пройти',
    TaskState.PASSED: 'Пройден'
}

TASK_STATE_COLORS = {
    TaskState.PASSED: 'mediumseagreen',
    TaskState.IMPOSSIBLE: 'orange',
    TaskState.FAILED: 'lightcoral',
    TaskState.SKIPPED: 'mediumturquoise'
}

TASK_STATE_CB_DATA = {
    'skipped': TaskState.SKIPPED,
    'failed': TaskState.FAILED,
    'passed': TaskState.PASSED,
    'impossible': TaskState.IMPOSSIBLE
}
