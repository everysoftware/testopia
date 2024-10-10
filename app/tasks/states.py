from aiogram.fsm.state import StatesGroup, State


class TaskGroup(StatesGroup):
    get = State()
    get_many = State()
    adding_task = State()
    editing_task_status = State()
    editing_comment = State()
    editing_report = State()
