from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.models import Product


async def get_products_kb(products: list[Product]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for product in products:
        builder.add(
            InlineKeyboardButton(text=product.name, callback_data=f"show_{product.id}")
        )

    builder.adjust(1)

    builder.row(InlineKeyboardButton(text="Создать ➕", callback_data="add"))

    return builder.as_markup(resize_keyboard=True)
