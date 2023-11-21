from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.keyboards.tasks import get_tasks_kb
from src.db import Database

router = Router()


async def show_tasks(
        message: types.Message,
        state: FSMContext,
        db: Database,
        checklist_id: int,
        is_session_running: bool = False
) -> None:
    await state.update_data(checklist_id=checklist_id)

    async with db.session.begin():
        checklist = await db.checklist.get(checklist_id)
        kb = await get_tasks_kb(checklist.tasks, is_session_running=is_session_running)

        cap = f'🗒 Чек-лист {checklist.name}\n\n' \
              f'Продукт: {checklist.product.name}\n' \
              f'Дата создания: {checklist.created_at}\n'

        if len(kb.inline_keyboard) == 2:
            await message.answer(
                cap + 'Нет задач',
                reply_markup=kb
            )
        else:
            await message.answer(
                cap + 'Задачи:',
                reply_markup=kb
            )

    if not is_session_running:
        await state.set_state(MainGroup.viewing_tasks)


@router.callback_query(F.data.startswith('show_'), MainGroup.viewing_checklists)
async def show(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    checklist_id = int(call.data.split('_')[1])

    await show_tasks(call.message, state, db, checklist_id)

    await call.answer()
