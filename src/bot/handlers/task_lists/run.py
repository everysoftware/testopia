from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.products import ProductGroup
from src.bot.fsm.task_lists import TaskListGroup
from src.bot.handlers.activities import RunPassageActivity
from src.bot.keyboards.devices import get_devices_kb
from src.db import Database
from src.bot.handlers.tasks.show import show_ as show_tasks

router = Router(name='task_lists_run')


@router.callback_query(F.data.startswith('run_'), MainGroup.viewing_task_lists)
async def run(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    task_list_id = int(call.data.split('_')[1])
    await state.update_data(task_list_id=task_list_id)

    kb = await get_devices_kb(db, call.from_user.id, add_button=False)

    if kb.inline_keyboard:
        await RunPassageActivity.start_callback(
            call, state,
            new_state=ProductGroup.adding_product,
            text='Выберите устройство, на котором будет проходить тестирование',
            reply_markup=kb
        )
    else:
        await call.message.answer('Добавьте устройство для начала тестирования')

    await state.set_state(TaskListGroup.selecting_device)

    await call.answer()


@router.callback_query(F.data.startswith('select_'), TaskListGroup.selecting_device)
async def select_device(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    device_id = int(call.data.split('_')[1])

    async with db.session.begin():
        device = await db.device.get(device_id)

    await call.message.answer(f'Выбрано устройство: <b>{device.name}</b>')

    user_data = await state.get_data()

    await call.message.answer('Начинаем сессию тестирования')

    await show_tasks(
        call.message,
        state,
        db,
        user_data['task_list_id'],
        True
    )

    await state.set_state(TaskListGroup.in_testing_session)

    await call.answer()
