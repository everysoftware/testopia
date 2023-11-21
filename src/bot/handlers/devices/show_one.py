from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.devices import SHOW_DEVICE_KB
from src.bot.fsm import MainGroup
from src.db import Database

router = Router()


async def show_device(
        message: types.Message,
        state: FSMContext,
        db: Database,
        device_id: int
) -> None:
    await state.update_data(device_id=device_id)

    async with db.session.begin():
        device = await db.device.get(device_id)

        await message.answer(
            f'📱 Устройство: {device.name}\n\n'
            f'Дата создания: {device.created_at}',
            reply_markup=SHOW_DEVICE_KB
        )

    await state.set_state(MainGroup.viewing_device)


@router.callback_query(F.data.startswith('select_'), MainGroup.viewing_devices)
async def show_one(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    device_id = int(call.data.split('_')[1])
    await show_device(call.message, state, db, device_id)
    await call.answer()
