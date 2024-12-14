from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.base.pagination import LimitOffset
from app.base.types import UUID
from app.keyboards import CANCEL_KB
from app.users.dependencies import UserDep
from app.workspaces.dependencies import WorkspaceServiceDep
from app.workspaces.keyboards import get_workspace_kb, SHOW_WORKSPACE_KB
from app.workspaces.states import WorkspaceGroup

router = Router()


@router.callback_query(F.data == "to_workspaces")
@router.message(Command("workspaces"))
@router.message(F.text == "Мои пространства 📦")
async def get_many(
    event: types.Message | types.CallbackQuery,
    state: FSMContext,
    user: UserDep,
    projects: WorkspaceServiceDep,
) -> None:
    message = (
        event.message if isinstance(event, types.CallbackQuery) else event
    )
    response = await projects.get_many(user, LimitOffset(limit=100))
    kb = get_workspace_kb(response)
    if response.total > 0:
        await message.answer("Ваши пространства", reply_markup=kb)
    else:
        await message.answer("У Вас нет пространств", reply_markup=kb)
    await state.set_state(WorkspaceGroup.get_many)
    if isinstance(event, types.CallbackQuery):
        await event.answer()


@router.callback_query(F.data == "add", WorkspaceGroup.get_many)
async def request_name(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Назовите пространство. Например, `Рабочее`", reply_markup=CANCEL_KB
    )
    await state.set_state(WorkspaceGroup.enter_name)
    await call.answer()


@router.message(WorkspaceGroup.enter_name)
async def request_description(
    message: types.Message, state: FSMContext
) -> None:
    await state.update_data(ws_name=message.text)
    await message.answer(
        "Введите описание пространства. Например, `Пространство для работы над VK`",
        reply_markup=CANCEL_KB,
    )
    await state.set_state(WorkspaceGroup.enter_description)


@router.message(WorkspaceGroup.enter_description)
async def create(
    message: types.Message,
    state: FSMContext,
    user: UserDep,
    service: WorkspaceServiceDep,
) -> None:
    user_data = await state.get_data()
    desc = message.text
    await service.create(
        user_id=user.id,
        name=user_data["ws_name"],
        description=desc,
    )
    await message.answer("Пространство успешно создано!")
    await get_many(message, state, user, service)


@router.callback_query(F.data.startswith("select_"), WorkspaceGroup.get_many)
async def get(
    call: types.CallbackQuery,
    state: FSMContext,
    workspaces: WorkspaceServiceDep,
) -> None:
    workspace_id = UUID(call.data.split("_")[1])
    project = await workspaces.get_one(workspace_id)
    await call.message.answer(
        f"Пространство: {project.name}\n\n"
        f"Описание: {project.description}\n\n"
        f"Создано: {project.created_at}\n"
        f"Обновлено: {project.updated_at}",
        reply_markup=SHOW_WORKSPACE_KB,
    )
    await state.update_data(workspace_id=str(workspace_id))
    await state.set_state(WorkspaceGroup.get)
    await call.answer()
