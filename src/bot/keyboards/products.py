from aiogram.types import User, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db import Database


async def get_products_kb(
        from_user: User,
        db: Database
) -> InlineKeyboardMarkup:
    async with db.session.begin():
        builder = InlineKeyboardBuilder()
        user = await db.user.get(from_user.id)

        for product in user.products:
            builder.add(InlineKeyboardButton(
                text=product.name,
                callback_data=f'show_{product.id}'
            ))

    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(text='Создать ⏬', callback_data='add')
    )

    return builder.as_markup(resize_keyboard=True)
