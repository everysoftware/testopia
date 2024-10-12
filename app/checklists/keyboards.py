from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.checklists.schemas import ChecklistRead
from app.db.schemas import Page


def get_checklist_kb(checklists: Page[ChecklistRead]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for checklist in checklists.items:
        builder.row(
            InlineKeyboardButton(
                text=checklist.name, callback_data=f"show_{checklist.id}"
            )
        )
    builder.adjust(1)
    builder.row(
        InlineKeyboardButton(text="Создать ➕", callback_data="add"),
    )
    return builder.as_markup(resize_keyboard=True)
