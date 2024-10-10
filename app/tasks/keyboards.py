from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.schemas import Page
from app.tasks.constants import TASK_STATUSES
from app.tasks.schemas import TaskRead


def get_edit_task_status_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for status in TASK_STATUSES.values():
        builder.row(
            InlineKeyboardButton(
                text=f"{status["text"]} {status["emoji"]}",
                callback_data=f"set_{status["name"]}",
            )
        )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


EDIT_TASK_STATUS_KB = get_edit_task_status_kb()

SHOW_TASK_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️", callback_data="edit"),
            InlineKeyboardButton(text="💬", callback_data="comment"),
            InlineKeyboardButton(text="🔗", callback_data="report"),
            InlineKeyboardButton(text="❌", callback_data="delete"),
        ],
        [InlineKeyboardButton(text="Назад ⬅️", callback_data="back")],
    ]
)


def get_tasks_kb(
        tasks: Page[TaskRead], *, action_btns: bool = True
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for task in tasks.items:
        builder.row(
            InlineKeyboardButton(
                text=f"{task.name} {TASK_STATUSES[task.status]['emoji']}",
                callback_data=f"show_{task.id}",
            )
        )
    if action_btns:
        builder.row(
            InlineKeyboardButton(text="Создать задачу ➕", callback_data="add"),
            InlineKeyboardButton(text="Удалить чек-лист ❌", callback_data="delete"),
        )
    builder.row(InlineKeyboardButton(text="Назад ⬅️", callback_data="back"))
    return builder.as_markup(resize_keyboard=True)
