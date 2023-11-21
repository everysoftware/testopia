from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.models import Checklist


async def get_checklist_kb(
        checklists: list[Checklist]
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for checklist in checklists:
        builder.row(
            InlineKeyboardButton(
                text=checklist.name,
                callback_data=f'show_{checklist.id}'
            )
        )

    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(text='Создать ➕', callback_data='add'),
        InlineKeyboardButton(text='Удалить продукт ❌', callback_data='delete')
    )
    builder.row(
        InlineKeyboardButton(text='Назад ⬅️', callback_data='back')
    )

    return builder.as_markup(resize_keyboard=True)
