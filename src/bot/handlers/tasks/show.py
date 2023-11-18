from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.keyboards.tasks import get_tasks_kb
from src.db import Database

router = Router(name='tasks_show')


async def show_(
        message: types.Message,
        state: FSMContext,
        db: Database,
        task_list_id: int,
        is_session_running: bool = False
) -> None:
    await state.update_data(task_list_id=task_list_id)

    async with db.session.begin():
        task_list = await db.task_list.get(task_list_id)
        kb = await get_tasks_kb(task_list, is_session_running=is_session_running)

        if len(kb.inline_keyboard) == 1:
            await message.answer(f'Чек-лист <b>{task_list.name}</b> ({task_list.product.name}) пуст',
                                 reply_markup=kb)
        else:
            await message.answer(f'Задачи в чек-листе <b>{task_list.name}</b> ({task_list.product.name})',
                                 reply_markup=kb)

    if not is_session_running:
        await state.set_state(MainGroup.viewing_tasks)


@router.callback_query(F.data.startswith('show_'), MainGroup.viewing_task_lists)
async def show(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    task_list_id = int(call.data.split('_')[1])

    await show_(call.message, state, db, task_list_id)

    await call.answer()
