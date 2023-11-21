from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.enums.task_state import TASK_STATE_EMOJI
from src.db.models import Task

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

SHOW_TASK_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='✏️',
                callback_data='edit'
            ),
            InlineKeyboardButton(
                text='💬',
                callback_data='comment'
            ),
            InlineKeyboardButton(
                text='🔗',
                callback_data='report'
            ),
            InlineKeyboardButton(
                text='❌',
                callback_data='delete'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Назад ⬅️',
                callback_data='back'
            )
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
                text=f'{task.name} {TASK_STATE_EMOJI[task.state]}',
                callback_data=f'show_{task.id}'
            )
        )

    if not is_session_running:
        builder.row(
            InlineKeyboardButton(text='Создать ➕', callback_data='add'),
            InlineKeyboardButton(text='Удалить чек-лист ❌', callback_data='delete')
        )

    builder.row(
        InlineKeyboardButton(text='Назад ⬅️', callback_data='back')
    )

    return builder.as_markup(resize_keyboard=True)
