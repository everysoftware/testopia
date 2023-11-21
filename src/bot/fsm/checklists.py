from aiogram.fsm.state import StatesGroup, State


class ChecklistGroup(StatesGroup):
    adding_checklist = State()
    selecting_device = State()
