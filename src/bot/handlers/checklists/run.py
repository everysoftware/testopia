from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.checklists import ChecklistGroup
from src.bot.handlers.tasks.show import show_tasks as show_tasks
from src.bot.keyboards.devices import get_devices_kb
from src.db import Database

router = Router()


@router.callback_query(F.data.startswith('run_'), MainGroup.viewing_tasks)
async def run(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    checklist_id = int(call.data.split('_')[1])
    await state.update_data(checklist_id=checklist_id)

    async with db.session.begin():
        user = await db.user.get(call.from_user.id)
        kb = await get_devices_kb(user.devices, readonly=False)

    if kb.inline_keyboard:
        await call.message.answer(
            'Выберите устройство, на котором будет проходить тестирование',
            reply_markup=kb
        )
        await state.set_state(ChecklistGroup.selecting_device)
    else:
        await call.message.answer('Добавьте устройство для начала тестирования')

    await call.answer()


@router.callback_query(F.data.startswith('select_'), ChecklistGroup.selecting_device)
async def select_device(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    device_id = int(call.data.split('_')[1])

    user_data = await state.get_data()

    async with db.session.begin():
        device = await db.device.get(device_id)
        print(device)
        print(user_data['checklist_id'])
        checklist = await db.checklist.get(user_data['checklist_id'])

        await call.message.answer(
            'Начинаем сессию тестирования\n\n'
            f'Продукт: {checklist.product.name}\n'
            f'Чек-лист: {checklist.name}\n'
            f'Устройство: {device.name}'
        )

    await show_tasks(
        call.message,
        state,
        db,
        user_data['checklist_id'],
        True
    )

    await state.set_state(ChecklistGroup.conducting_testing_session)

    await call.answer()
