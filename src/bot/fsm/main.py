from aiogram.fsm.state import StatesGroup, State


class MainGroup(StatesGroup):
    viewing_menu = State()
    viewing_products = State()
    viewing_devices = State()
    viewing_stats = State()
    viewing_tasks = State()
    viewing_checklists = State()
    viewing_task = State()
    conducting_testing_session = State()
    viewing_device = State()
