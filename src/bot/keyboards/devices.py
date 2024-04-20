from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.models import Device

SHOW_DEVICE_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить ❌", callback_data="delete"),
            InlineKeyboardButton(text="Назад ⬅️", callback_data="delete"),
        ]
    ]
)


async def get_devices_kb(
    devices: list[Device], selecting_mode: bool = False
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for device in devices:
        builder.add(
            InlineKeyboardButton(text=device.name, callback_data=f"select_{device.id}")
        )

    builder.adjust(1)

    if not selecting_mode:
        builder.row(InlineKeyboardButton(text="Создать ➕", callback_data="add"))
    if selecting_mode:
        builder.row(InlineKeyboardButton(text="Назад ⬅️", callback_data="back"))

    return builder.as_markup(resize_keyboard=True)
