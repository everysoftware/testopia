from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm.tasks import TaskGroup
from src.bot.handlers.tasks.show_one import show_task
from src.bot.keyboards.service import CANCEL_KB
from src.db import Database
from src.db.models import Report

router = Router()


@router.callback_query(F.data == 'report', MainGroup.viewing_task)
async def url(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        'Введите ссылку на отчёт об ошибках',
        reply_markup=CANCEL_KB
    )
    await state.set_state(TaskGroup.editing_report)

    await call.answer()


@router.message(TaskGroup.editing_report)
async def edit_report(message: types.Message, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        task = await db.task.get(user_data['task_id'])
        report: Report = task.report
        if report is None:
            task.report = db.report.new(url=message.text)
            await db.task.merge(task)
        else:
            report.url = message.text
            await db.report.merge(report)

    await message.answer('Ссылка на отчёт об ошибках успешно обновлена!')

    await show_task(
        message,
        state,
        db,
        user_data['task_id']
    )
