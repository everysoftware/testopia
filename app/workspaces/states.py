from aiogram.fsm.state import StatesGroup, State


class WorkspaceGroup(StatesGroup):
    get_many = State()
    get = State()
    enter_name = State()
    enter_description = State()
    enter_stack = State()
