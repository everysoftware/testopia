from aiogram.fsm.state import StatesGroup, State


class TaskListGroup(StatesGroup):
    adding_list = State()
    selecting_device = State()
    in_testing_session = State()
