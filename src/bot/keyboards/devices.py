from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Device


async def get_devices_kb(
        devices: list[Device],
        readonly: bool = True
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for device in devices:
        builder.add(InlineKeyboardButton(
            text=device.name,
            callback_data=f'select_{device.id}'
        ))

    builder.adjust(1)

    if readonly:
        builder.row(
            InlineKeyboardButton(text='Добавить ⏬', callback_data='add')
        )

    return builder.as_markup(resize_keyboard=True)
