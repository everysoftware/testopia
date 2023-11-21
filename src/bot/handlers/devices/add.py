from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.keyboards.service import CANCEL_KB
from src.bot.fsm import MainGroup
from src.bot.fsm.devices import DeviceGroup
from src.bot.handlers.devices.show import show as show_devices
from src.db import Database

router = Router()


@router.callback_query(F.data == 'add', MainGroup.viewing_devices)
async def name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        'Назовите устройство. Например, <code>iPhone 13</code>',
        reply_markup=CANCEL_KB
    )
    await state.set_state(DeviceGroup.adding_device)

    await call.answer()


@router.message(DeviceGroup.adding_device)
async def add(message: types.Message, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        db.device.new(
            user_id=message.from_user.id,
            name=message.text
        )

    await message.answer('Устройство успешно добавлено!')
    await show_devices(message, state, db)
