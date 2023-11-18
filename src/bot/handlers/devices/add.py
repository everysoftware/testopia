from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.devices import DeviceGroup
from src.bot.handlers.activities import AddDeviceActivity
from src.bot.handlers.devices.show import show as show_devices
from src.db import Database

router = Router(name='devices_add')


@router.callback_query(F.data == 'add', MainGroup.viewing_devices)
async def add(call: types.CallbackQuery, state: FSMContext) -> None:
    await AddDeviceActivity.start_callback(
        call, state,
        new_state=DeviceGroup.adding_device,
        text='Назовите устройство. Например, iPhone 13 - iOS 16.1 | Mobile'
    )


@router.message(DeviceGroup.adding_device)
async def type_name(message: types.Message, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        db.device.new(
            user_id=message.from_user.id,
            name=message.text
        )

    await AddDeviceActivity.finish(
        message, state,
        text='Устройство успешно добавлено!'
    )

    await show_devices(message, state, db)
