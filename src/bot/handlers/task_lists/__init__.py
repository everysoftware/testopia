from aiogram import Router

from .add import router as add_router
from .run import router as run_router
from .show import router as show_router
from ...middlewares import DatabaseMd

routers = (
    add_router,
    show_router,
    run_router
)

router = Router(name='task_lists')
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())
