from html import escape

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.enums.task_state import TASK_STATE_TRANSLATIONS, TASK_STATE_EMOJI
from src.bot.fsm import MainGroup
from src.bot.keyboards.tasks import SHOW_TASK_KB
from src.db import Database

router = Router()


async def show_task(
    message: types.Message, state: FSMContext, db: Database, task_id: int
) -> None:
    async with db.session.begin():
        task = await db.task.get(task_id)
        report_url = escape(task.report.url if task.report else "нет")
        comment_text = escape(task.comment.text if task.comment else "нет")

        await message.answer(
            f"📌 <b>Задача: {task.name}</b>\n\n"
            f"Статус: {TASK_STATE_TRANSLATIONS[task.state]} {TASK_STATE_EMOJI[task.state]}\n"
            f"Продукт: {task.checklist.product.name}\n"
            f"Чек-лист: {task.checklist.name}\n"
            f"Отчёт об ошибках: {report_url}\n"
            f"Комментарий: {comment_text}\n"
            f"Создано: {task.user.first_name} {task.user.last_name} (#{task.user_id})\n"
            f"Дата создания: {task.created_at}",
            reply_markup=SHOW_TASK_KB,
        )

    await state.set_state(MainGroup.viewing_task)


@router.callback_query(F.data.startswith("show_"), MainGroup.viewing_tasks)
@router.callback_query(F.data.startswith("show_"), MainGroup.conducting_testing_session)
async def show_one(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    task_id = int(call.data.split("_")[1])
    await state.update_data(task_id=task_id)

    await show_task(call.message, state, db, task_id)

    await call.answer()
