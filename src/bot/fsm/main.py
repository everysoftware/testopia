from aiogram.fsm.state import StatesGroup, State


class MainGroup(StatesGroup):
    viewing_menu = State()
    viewing_products = State()
    viewing_devices = State()
    viewing_stats = State()
    viewing_tasks = State()
    viewing_task_lists = State()
