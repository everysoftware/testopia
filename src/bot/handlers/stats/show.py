import os

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from src.db import Database
from .heat_map import heat_map
from .pie import pie_plot

router = Router()


@router.message(Command('stats'))
@router.message(F.text == 'Статистика 📊')
async def show(message: types.Message, db: Database) -> None:
    path = await pie_plot(db, message.from_user.id)
    await message.answer_photo(
        photo=FSInputFile(path),
        caption='Статистика прохождения тестов'
    )
    os.remove(path)

    path = await heat_map(db, message.from_user.id)
    await message.answer_photo(
        photo=FSInputFile(path),
        caption='Карта продуктивности'
    )
    os.remove(path)
