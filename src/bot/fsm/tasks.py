from aiogram.fsm.state import StatesGroup, State


class TaskGroup(StatesGroup):
    adding_task = State()
    editing_task_status = State()
