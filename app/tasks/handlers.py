from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from app.checklists.dependencies import ChecklistServiceDep
from app.checklists.states import ChecklistGroup
from app.db.schemas import PageParams
from app.tasks.constants import TASK_STATUSES
from app.tasks.dependencies import TaskServiceDep
from app.tasks.keyboards import get_tasks_kb, SHOW_TASK_KB
from app.tasks.states import TaskGroup

router = Router()


@router.callback_query(F.data.startswith("show_"), ChecklistGroup.get_many)
async def get_many(
        call: types.CallbackQuery,
        state: FSMContext,
        service: TaskServiceDep,
        checklist_service: ChecklistServiceDep,
) -> None:
    checklist_id = int(call.data.split("_")[1])
    response = await service.get_many(checklist_id, PageParams(limit=100))
    kb = get_tasks_kb(response)
    checklist = await checklist_service.get_one(checklist_id)

    cap = (
        f"🗒 Чек-лист {checklist.name}\n\n"
        f"Продукт: {checklist.product}\n"
        f"Создан: {checklist.created_at}\n"
        f"Изменен: {checklist.updated_at}\n\n"
    )
    if response.total > 0:
        await call.message.answer(cap + "Задачи:", reply_markup=kb)
    else:
        await call.message.answer(cap + "Нет задач", reply_markup=kb)

    await state.update_data(checklist_id=checklist_id)
    await state.set_state(TaskGroup.get_many)
    await call.answer()


@router.callback_query(F.data.startswith("show_"), TaskGroup.get_many)
async def get(
        call: types.CallbackQuery, state: FSMContext, service: TaskServiceDep, checklist_service: ChecklistServiceDep,
) -> None:
    task_id = int(call.data.split("_")[1])
    task = await service.get_one(task_id)
    report_url = task.report_url if task.report_url else "нет"
    comment = task.comment if task.comment else "нет"

    user_data = await state.get_data()
    checklist_id = user_data["checklist_id"]
    checklist = await checklist_service.get_one(checklist_id)

    await call.message.answer(
        f"📌 *Задача: {task.name}*\n\n"
        f"Статус: {TASK_STATUSES[task.status]["text"]} {TASK_STATUSES[task.status]["emoji"]}\n"
        f"Чек-лист: {checklist.name}\n"
        f"Отчёт об ошибках: {report_url}\n"
        f"Комментарий: {comment}\n"
        f"Создана: {task.created_at}\n"
        f"Изменена: {task.updated_at}",
        reply_markup=SHOW_TASK_KB,
    )

    await state.set_state(TaskGroup.get)
    await state.update_data(task_id=task_id)
    await call.answer()
