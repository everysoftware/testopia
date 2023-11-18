from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.models import Product


async def get_task_lists_kb(
        product: Product
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for task_list in product.task_lists:
        builder.row(
            InlineKeyboardButton(
                text=task_list.name,
                callback_data=f'show_{task_list.id}'
            ),
            InlineKeyboardButton(
                text='▶️',
                callback_data=f'run_{task_list.id}'
            ),
        )

    builder.adjust(2)

    builder.row(
        InlineKeyboardButton(text='Создать ⏬', callback_data='add')
    )

    return builder.as_markup(resize_keyboard=True)
