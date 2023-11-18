from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db import Database


async def get_devices_kb(
        db: Database,
        user_id: int,
        add_button: bool = True
) -> InlineKeyboardMarkup:
    async with db.session.begin():
        builder = InlineKeyboardBuilder()
        user = await db.user.get(user_id)

        for device in user.devices:
            builder.add(InlineKeyboardButton(
                text=device.name,
                callback_data=f'select_{device.id}'
            ))

    builder.adjust(1)

    if add_button:
        builder.row(
            InlineKeyboardButton(text='Добавить ⏬', callback_data='add')
        )

    return builder.as_markup(resize_keyboard=True)
