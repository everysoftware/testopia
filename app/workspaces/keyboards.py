from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.base.pagination import Page
from app.workspaces.models import Workspace

SHOW_WORKSPACE_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить ❌", callback_data="delete"),
            InlineKeyboardButton(
                text="Назад ⬅️", callback_data="to_workspaces"
            ),
        ]
    ]
)


def get_workspace_kb(
    page: Page[Workspace], *, action_btns: bool = True
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in page.items:
        builder.add(
            InlineKeyboardButton(text=i.name, callback_data=f"select_{i.id}")
        )
    builder.adjust(1)
    if action_btns:
        builder.row(
            InlineKeyboardButton(text="Создать ➕", callback_data="add")
        )
    return builder.as_markup(resize_keyboard=True)
