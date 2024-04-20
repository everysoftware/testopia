from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.keyboards.devices import get_devices_kb
from src.db import Database

router = Router()


@router.message(Command("devices"))
@router.message(F.text == "Мои устройства 📱")
async def show(message: types.Message, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        user = await db.user.get(message.from_user.id)
        kb = await get_devices_kb(user.devices)

    if len(kb.inline_keyboard) == 1:
        await message.answer("У Вас нет устройств", reply_markup=kb)
    else:
        await message.answer("Ваши устройства", reply_markup=kb)

    await state.set_state(MainGroup.viewing_devices)
