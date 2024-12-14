from aiogram.fsm.state import StatesGroup, State


class ProjectGroup(StatesGroup):
    get_many = State()
    get = State()
    select_project = State()
    enter_name = State()
    enter_description = State()
    enter_stack = State()
