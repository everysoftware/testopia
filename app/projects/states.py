from aiogram.fsm.state import StatesGroup, State


class ProjectGroup(StatesGroup):
    get_many = State()
    enter_name = State()
    select_project = State()
    get = State()
