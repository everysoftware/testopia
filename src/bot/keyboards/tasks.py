from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.enums import TaskState
from src.db.models import Task

TASK_STATES_COLORS = {
    TaskState.SKIPPED: '🔵',
    TaskState.FAILED: '🔴',
    TaskState.PASSED: '🟢',
    TaskState.IMPOSSIBLE: '🟡',
}

TASK_STATES_CB_DATA = {
    'skipped': TaskState.SKIPPED,
    'failed': TaskState.FAILED,
    'passed': TaskState.PASSED,
    'impossible': TaskState.IMPOSSIBLE
}

TASK_STATES_TRANSLATIONS = {
    'SKIPPED': 'Пропущен',
    'FAILED': 'Не пройден',
    'IMPOSSIBLE': 'Невозможно пройти',
    'PASSED': 'Пройден'
}

EDIT_TASK_STATUS_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пройден 🟢', callback_data='set_passed'),
            InlineKeyboardButton(text='Не пройден 🔴', callback_data='set_failed')
        ],
        [
            InlineKeyboardButton(text='Невозможно пройти 🟡', callback_data='set_impossible'),
            InlineKeyboardButton(text='Пропущен 🔵', callback_data='set_skipped'),
        ]
    ]
)


async def get_tasks_kb(
        tasks: list[Task],
        is_session_running: bool = False
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for task in tasks:
        builder.row(
            InlineKeyboardButton(
                text=f'{task.name} {TASK_STATES_COLORS[task.state]}',
                callback_data=f'show_{task.id}'
            )
        )

        if is_session_running:
            builder.row(
                InlineKeyboardButton(
                    text='✏️',
                    callback_data=f'edit_{task.id}'
                ),
                InlineKeyboardButton(
                    text='💬',
                    callback_data=f'comment_{task.id}'
                ),
                InlineKeyboardButton(
                    text='🔗',
                    callback_data=f'report_{task.id}'
                ),
            )

    if not is_session_running:
        builder.row(
            InlineKeyboardButton(text='Создать задачу ⏬', callback_data='add')
        )
        if tasks:
            builder.row(
                InlineKeyboardButton(text='Начать сессию ▶️', callback_data=f'run_{tasks[0].checklist.id}')
            )

    return builder.as_markup(resize_keyboard=True)
