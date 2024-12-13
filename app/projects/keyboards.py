from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.base.pagination import Page
from app.projects.models import Project
from app.tasks.constants import TASK_STATUSES
from app.tasks.models import Task


def get_project_kb(page: Page[Project]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in page.items:
        builder.row(
            InlineKeyboardButton(
                text=i.name,
                callback_data=f"show_project:{i.id}",
            )
        )
    builder.adjust(1)
    builder.row(
        InlineKeyboardButton(text="Создать ➕", callback_data="add"),
    )
    return builder.as_markup(resize_keyboard=True)


def get_tasks_kb(
    tasks: Page[Task], *, action_btns: bool = True
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for task in tasks.items:
        builder.row(
            InlineKeyboardButton(
                text=f"{task.name} {TASK_STATUSES[task.status]['emoji']}",
                callback_data=f"show_task:{task.id}",
            )
        )
    if action_btns:
        builder.row(
            InlineKeyboardButton(
                text="Создать задачу ➕", callback_data="add"
            ),
            InlineKeyboardButton(
                text="Удалить чек-лист ❌", callback_data="delete"
            ),
        )
    builder.row(
        InlineKeyboardButton(text="Назад ⬅️", callback_data="to_projects")
    )
    return builder.as_markup(resize_keyboard=True)
