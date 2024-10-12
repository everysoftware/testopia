from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.db.schemas import PageParams
from app.devices.dependencies import DeviceServiceDep
from app.devices.keyboards import get_devices_kb, SHOW_DEVICE_KB
from app.devices.states import DeviceGroup
from app.keyboards import CANCEL_KB
from app.users.dependencies import MeDep

router = Router()


@router.callback_query(F.data == "to_devices")
@router.message(Command("devices"))
@router.message(F.text == "Мои устройства 📱")
async def get_many(
    event: types.Message | types.CallbackQuery,
    state: FSMContext,
    user: MeDep,
    service: DeviceServiceDep,
) -> None:
    message = (
        event.message if isinstance(event, types.CallbackQuery) else event
    )
    response = await service.get_many(PageParams(limit=100), user_id=user.id)
    kb = get_devices_kb(response)
    if response.total > 0:
        await message.answer("Ваши устройства", reply_markup=kb)
    else:
        await message.answer("У Вас нет устройств", reply_markup=kb)
    await state.set_state(DeviceGroup.get_many)
    if isinstance(event, types.CallbackQuery):
        await event.answer()


@router.callback_query(F.data == "add", DeviceGroup.get_many)
async def request_name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Назовите устройство. Например, `iPhone 13`", reply_markup=CANCEL_KB
    )
    await state.set_state(DeviceGroup.enter_name)
    await call.answer()


@router.message(DeviceGroup.enter_name)
async def create(
    message: types.Message,
    state: FSMContext,
    user: MeDep,
    service: DeviceServiceDep,
) -> None:
    name = message.text
    await service.create(user_id=user.id, name=name)
    await message.answer("Устройство успешно добавлено!")
    await get_many(message, state, user, service)


@router.callback_query(F.data.startswith("select_"), DeviceGroup.get_many)
async def get(
    call: types.CallbackQuery, state: FSMContext, service: DeviceServiceDep
) -> None:
    device_id = int(call.data.split("_")[1])
    device = await service.get_one(device_id)
    await call.message.answer(
        f"📱 Устройство: {device.name}\n\n"
        f"Создано: {device.created_at}\n"
        f"Обновлено: {device.updated_at}",
        reply_markup=SHOW_DEVICE_KB,
    )
    await state.update_data(device_id=device_id)
    await state.set_state(DeviceGroup.get)
    await call.answer()
