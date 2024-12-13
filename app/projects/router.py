from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.base.pagination import LimitOffset
from app.base.types import UUID as ID, UUID
from app.projects.dependencies import ProjectServiceDep
from app.projects.keyboards import get_project_kb, get_tasks_kb
from app.projects.states import ProjectGroup
from app.tasks.dependencies import TaskServiceDep
from app.tasks.states import TaskGroup
from app.users.dependencies import UserDep
from app.workspaces.dependencies import WorkspaceServiceDep
from app.workspaces.keyboards import get_workspace_kb

router = Router()


@router.callback_query(F.data == "to_projects")
@router.message(Command("projects"))
@router.message(F.text == "Мои задачи 📝")
async def get_many(
    event: types.Message | types.CallbackQuery,
    state: FSMContext,
    user: UserDep,
    projects: ProjectServiceDep,
) -> None:
    message = (
        event.message if isinstance(event, types.CallbackQuery) else event
    )
    response = await projects.get_many(user, LimitOffset(limit=100))
    kb = get_project_kb(response)
    if response.total > 0:
        await message.answer("Проекты:", reply_markup=kb)
    else:
        await message.answer("Нет проектов", reply_markup=kb)
    await state.set_state(ProjectGroup.get_many)
    if isinstance(event, types.CallbackQuery):
        await event.answer()


# GET
@router.callback_query(F.data == "to_project")
@router.callback_query(
    F.data.startswith("show_project:"), ProjectGroup.get_many
)
async def get(
    event: types.CallbackQuery | types.Message,
    state: FSMContext,
    tasks: TaskServiceDep,
    projects: ProjectServiceDep,
    *,
    project_id: ID | None = None,
) -> None:
    if isinstance(event, types.CallbackQuery):
        message = event.message
        if event.data.startswith("show_"):
            project_id = UUID(event.data.split(":")[1])
    else:
        message = event
    if project_id is None:
        user_data = await state.get_data()
        project_id = user_data["project_id"]
    assert project_id is not None

    response = await tasks.get_many(project_id, LimitOffset(limit=100))
    kb = get_tasks_kb(response)
    project = await projects.get_one(project_id)

    cap = (
        f"🗒 Проект {project.name}\n\n"
        f"Описание: {project.description}\n"
        f"Стек технологий: {project.stack}\n"
        f"Создан: {project.created_at}\n"
        f"Изменен: {project.updated_at}\n\n"
    )
    if response.total > 0:
        await message.answer(cap + "Задачи:", reply_markup=kb)
    else:
        await message.answer(cap + "Нет задач", reply_markup=kb)

    await state.update_data(workspace_id=str(project.workspace_id))
    await state.update_data(project_id=str(project.id))
    await state.set_state(TaskGroup.get_many)
    if isinstance(event, types.CallbackQuery):
        await event.answer()


@router.callback_query(F.data == "add", ProjectGroup.get_many)
async def select_project(
    call: types.CallbackQuery,
    state: FSMContext,
    user: UserDep,
    workspaces: WorkspaceServiceDep,
) -> None:
    page = await workspaces.get_many(user, LimitOffset(limit=100))
    await call.message.answer(
        "Выберите пространство", kb=get_workspace_kb(page, action_btns=False)
    )
    await state.set_state(ProjectGroup.select_project)
    await call.answer()


@router.callback_query(
    F.data.startswith("select_"), ProjectGroup.select_project
)
async def enter_name(call: types.CallbackQuery, state: FSMContext) -> None:
    project_id = call.data.split("_")[1]
    await state.update_data(project_id=project_id)
    await call.message.answer("Назовите список задач. Например, `авторизация`")
    await state.set_state(ProjectGroup.enter_name)
    await call.answer()


@router.message(ProjectGroup.enter_name)
async def add(
    message: types.Message,
    state: FSMContext,
    user: UserDep,
    service: WorkspaceServiceDep,
) -> None:
    name = message.text
    product = message.text
    await service.create(user_id=user.id, name=name, product=product)
    await message.answer("Чек-лист успешно создан!")
    await get_many(message, state, user, service)
